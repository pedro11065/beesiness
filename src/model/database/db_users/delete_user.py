import psycopg2
from ..json_db import json_db_read

def delete_user(user_data):
    db_login = json_db_read()

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
    cur.execute("DELETE FROM table_users WHERE user_email = %s", (f'{user_data}',))
    
    # Atualiza as informações.
    conn.commit()

    # Fecha o cursor e encerra a conexão.
    cur.close()
    conn.close()
