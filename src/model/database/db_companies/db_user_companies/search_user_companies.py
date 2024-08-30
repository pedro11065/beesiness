#Pesquisa um valor na tabela "table_user_companies" que registra as relações entre os demais usuários de uma empresa, além do criador

# Responsável por retornar a linha onde o email foi inserido.

import psycopg2
from ...json_db import json_db_read # Importação da função que lê os dados que armazenam as informações do servidor.
from ...db_log.create_log import db_create_log

def db_search_user_companies(search_data):

    db_login = json_db_read()

    #Conecta ao banco de dados.
    conn = psycopg2.connect(
        host=db_login[0],
        database=db_login[1],
        user=db_login[2],
        password=db_login[3]
    )
    cur = conn.cursor() # Cria um cursor no PostGreSQL
    
    cur.execute("SELECT * FROM table_user_companies WHERE user_id = %s OR company_id = %s", (search_data, search_data))

    message = (f"Pesquisa em table_user_companies por '{search_data}'")
    db_create_log(message)
    
    #---------------------------------------------------------------INDICES---------------------
                                                    #0         1             2     
    db_data = cur.fetchall() #valores da linha: #company_id, user_id, user_access_level

    conn.commit()
    cur.close() # Fecha o cursor
    conn.close() # Fecha a conexão geral
    
    return db_data #Retorna o resultado para a função login_verify