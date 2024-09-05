from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from colorama import Fore, Style

from src.model.database.db_users.create_user import db_create_user
from src.model.verifications.new_account.new_user_account_verify import verify_all

api_new_user_account = Blueprint('api_new_user_account', __name__)

@api_new_user_account.route('/create_user_account', methods=['POST'])
def create_account():
    try:
        create_data = request.get_json()

        nome = create_data.get('nome')
        cpf = create_data.get('cpf')
        email = create_data.get('email')
        senha = create_data.get('senha')
        data_nascimento = create_data.get('data_de_nascimento')

        hashed_password = generate_password_hash(senha)

        print(Fore.GREEN + '\n[API Usuário - Registro] ' + Style.RESET_ALL + f'Dados recebidos:\nNome: {nome}\nCPF: {cpf}\nEmail: {email}\nSenha: {senha}\nData de Nascimento: {data_nascimento}\n')


        verified, errors, errors_classes = verify_all(cpf, email, senha)
        if verified:
            db_create_user(nome, cpf, email, hashed_password, data_nascimento)
            print(Fore.GREEN + '[API Usuário - Registro] ' + Style.RESET_ALL + 'Registrado com sucesso!')
            return jsonify({"register": True}), 200
        
        else:
            print(Fore.GREEN + '\n[API Usuário - Registro] ' + Fore.RED + f'Erro(s):{errors} + Style.RESET_ALL') 
            return jsonify({"register": False, "error":errors, "classe":errors_classes}), 400

    except Exception as e:
        print(Fore.RED + f'\nErro durante o registro: {str(e)}' + Style.RESET_ALL)
        return jsonify({"error": "Ocorreu um erro no servidor."}), 500
