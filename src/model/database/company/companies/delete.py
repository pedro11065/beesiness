import psycopg2
from colorama import Fore, Style

from ...connect import connect_database

def db_delete_company(delete_data):

    print(Fore.CYAN + '[Banco de dados] ' + Style.RESET_ALL + 'Deletando empresa - delete_company')

    db_login = connect_database() # Coleta os dados para conexão

    # Conecta ao banco de dados
    conn = psycopg2.connect(
        host=db_login[0],
        database=db_login[1],
        user=db_login[2],
        password=db_login[3]
    )
    # Cria um cursor
    cur = conn.cursor()

    # Deleta os dados encontrados naquele e-mail.
    cur.execute("DELETE FROM table_companies WHERE company_cnpj = %s", (delete_data))
    cur.execute("DELETE FROM table_user_companies WHERE company_cnpj = %s", (delete_data))
    # Atualiza as informações.
    conn.commit()

    # Fecha o cursor e encerra a conexão.
    cur.close()
    conn.close()

    print(Fore.CYAN + '[Banco de dados] ' + Style.RESET_ALL + 'Empresa registrada com sucesso!')
