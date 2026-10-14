# Controle Financeiro

Aplicação de controle financeiro desenvolvida com Python, Flask, SQLite, HTML, CSS e JavaScript.

## Funcionalidades

- Dashboard com totais de receitas, despesas e saldo.
- Gráfico comparativo de receitas e despesas.
- Cadastro de lançamentos em um modal.
- Edição de lançamentos no mesmo modal.
- Exclusão de lançamentos com confirmação.
- Persistência dos dados em SQLite.
- Resumo financeiro filtrado por mês e ano.
- Validação básica dos dados enviados pelos formulários.
- Interface com navegação entre Dashboard, Lançamentos e Resumo mensal.

## Requisitos

- Python 3.10 ou superior
- Flask

## Como executar no Windows

1. Extraia o ZIP.
2. Abra a pasta `Controle_Financeiro` no VS Code.
3. Abra o terminal integrado nessa pasta.
4. (Opcional, recomendado) crie e ative um ambiente virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Instale a dependência:

   ```powershell
   py -m pip install -r requirements.txt
   ```

6. Inicie a aplicação:

   ```powershell
   py app.py
   ```

7. Acesse no navegador: http://127.0.0.1:5000

Se o comando `py` não funcionar, tente `python` no lugar dele.

## Estrutura

```text
CRUD/
├── app.py
├── database.py
├── lancamentos.py
├── main.py
├── financeiro.db
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── index.html
    ├── lancamentos.html
    └── resumo_mensal.html
```

## Observações

- `financeiro.db` contém os registros locais existentes. Faça uma cópia de segurança antes de apagar ou substituir esse arquivo.
- Registros antigos sem data receberam a data do dia em que a migração de banco foi executada; essa data pode não representar o dia real da movimentação.
- A aplicação foi pensada para uso local e aprendizado. Antes de disponibilizar publicamente, adicione proteção CSRF, autenticação quando necessária e uma configuração de servidor adequada.
- O gráfico usa Chart.js por CDN, então a página do dashboard precisa de conexão à internet para carregar essa biblioteca.
