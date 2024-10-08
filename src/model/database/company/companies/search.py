import psycopg2
from colorama import Fore, Style
from src import cache

from ...connect import connect_database

def db_search_company(search_data):
    cached_company = cache.get(f'company_{search_data}')
    if cached_company:
        return cached_company
    
    # Caso não esteja no cache, busca no banco de dados
    db_login = connect_database() # Coleta os dados para conexão
    conn = psycopg2.connect(
        host=db_login[0],
        database=db_login[1],
        user=db_login[2],
        password=db_login[3]
    )
    cur = conn.cursor() # Cria um cursor no PostGreSQL
    data = search_data
    
    if len(data) == 14 and data.isdigit(): # CNPJ
        print(Fore.CYAN + '[Banco de dados] ' + Style.RESET_ALL + f'Pesquisando dados da empresa com cnpj: {search_data}')
        cur.execute(f"SELECT * from table_companies WHERE company_cnpj = '{data}';")
    elif '@' in data: # E-mail
        print(Fore.CYAN + '[Banco de dados] ' + Style.RESET_ALL + f'Pesquisando dados da empresa com email: {search_data}')
        cur.execute(f"SELECT * from table_companies WHERE company_email = '{data}';")
    else: # Company_id
        print(Fore.CYAN + '[Banco de dados] ' + Style.RESET_ALL + f'Pesquisando dados da empresa com id: {search_data}')
        cur.execute(f"SELECT * from table_companies WHERE company_id = '{data}';")
    
    db_data = cur.fetchall()

    #---------------------------------------------------------------INDICES---------------------
                   #                         0         1            2            3             4             5
    conn.commit(); # Valores da linha: #company_id, user_id, company_name, company_email, company_cnpj, company_password
    cur.close();
    conn.close()

    try:
        if db_data:
            print(Fore.CYAN + '[Banco de dados] ' + Fore.GREEN + 'Dados da empresa encontrados com sucesso!' + Style.RESET_ALL)

            cache.set(f'company_{search_data}', db_data, timeout=600) # Armazena a empresa no cache
            return db_data
        else:
            print(Fore.CYAN + '[Banco de dados] ' + Fore.RED + 'Dados da empresa não foram encontrados!' + Style.RESET_ALL)
            return None
    
    except:
        print(Fore.CYAN + '[Banco de dados] ' + Fore.RED  + f'Erro ao responder dados solicitados.' + Style.RESET_ALL)
        return False
