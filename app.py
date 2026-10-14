from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from database import cursor
from lancamentos import (
    carregar_lancamentos,
    resumo_financeiro,
    lancamentos,
    salvar_lancamento,
    resumo_mensal,
    atualizar_lancamento_web,
    excluir_lancamento_web,
)

app = Flask(__name__)


@app.route("/")
def inicio():
    # Recarrega os dados para que os indicadores sempre reflitam o banco.
    carregar_lancamentos()
    total_receitas, total_despesas, saldo_atual = resumo_financeiro()

    return render_template(
        "index.html",
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo_atual=saldo_atual,
    )


@app.route("/lancamentos", methods=["GET", "POST"])
def pagina_lancamentos():
    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        categoria = request.form.get("categoria", "").strip()
        tipo = request.form.get("tipo", "").strip()
        valor_texto = request.form.get("valor", "").strip()
        id_lancamento_texto = request.form.get("id_lancamento", "").strip()

        try:
            valor = float(valor_texto)
        except (TypeError, ValueError):
            return "O valor informado é inválido.", 400

        if (
            not descricao
            or len(descricao) > 100
            or not categoria
            or len(categoria) > 50
            or valor <= 0
            or tipo not in ["Receita", "Despesa"]
        ):
            return "Dados inválidos. Volte e confira o formulário.", 400

        if id_lancamento_texto:
            try:
                id_lancamento = int(id_lancamento_texto)
                if id_lancamento <= 0:
                    raise ValueError
            except ValueError:
                return "ID de lançamento inválido.", 400

            if not atualizar_lancamento_web(
                id_lancamento, descricao, valor, categoria, tipo
            ):
                return "Lançamento não encontrado.", 404
        else:
            salvar_lancamento(descricao, valor, categoria, tipo)

        return redirect(url_for("pagina_lancamentos"))

    carregar_lancamentos()
    return render_template("lancamentos.html", lancamentos=lancamentos)


@app.route("/lancamentos/excluir/<int:id_lancamento>", methods=["POST"])
def rota_excluir_lancamento(id_lancamento):
    if id_lancamento <= 0:
        return "ID de lançamento inválido.", 400

    if not excluir_lancamento_web(id_lancamento):
        return "Lançamento não encontrado.", 404

    return redirect(url_for("pagina_lancamentos"))


@app.route("/resumo-mensal")
def pagina_resumo_mensal():
    mes = request.args.get("mes", datetime.now().strftime("%m"))
    ano = request.args.get("ano", datetime.now().strftime("%Y"))

    try:
        mes_numero = int(mes)
        ano_numero = int(ano)
        if not 1 <= mes_numero <= 12 or not 2000 <= ano_numero <= 2100:
            raise ValueError
    except (TypeError, ValueError):
        return "Mês ou ano inválido.", 400

    total_receitas, total_despesas, saldo_mensal = resumo_mensal(
        f"{mes_numero:02d}", str(ano_numero)
    )

    return render_template(
        "resumo_mensal.html",
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo_mensal=saldo_mensal,
        mes=mes_numero,
        ano=ano_numero,
    )


if __name__ == "__main__":
    app.run(debug=True)
