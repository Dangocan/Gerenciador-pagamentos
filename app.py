from functools import wraps
from flask import Flask, render_template, redirect, url_for, g, session, request
import os
import settings
import utils
from responses import resposta
from database.objects import Conta, Pagamento, Usuario

app = Flask(__name__, static_folder=os.path.join(settings.ROOT_DIRPATH, "static"), template_folder=os.path.join(settings.ROOT_DIRPATH, "templates"))
app.secret_key = utils.get_keys()["APP_SECRET_KEY"]


# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# import os; print(os.urandom(16))

def authenticate(f):
    @wraps(f)
    def auth_wrapper(*args, **kwargs):
        if "usu_id" in session:
            try:
                g.usuario = Usuario.get_by_id(session["usu_id"])
            except IndexError:
                logger.debug("User not found")
            except Exception as e:
                logger.exception(e)
                return resposta("Um erro desconhecido ocorreu", 400)
            else:
                return f(*args, **kwargs)
        return redirect(url_for("page_entrar"))

    return auth_wrapper


def unauthenticate(f):
    @wraps(f)
    def unauth_wrapper(*args, **kwargs):
        session.pop("usu_id", None)
        g.usuario = None
        return f(*args, **kwargs)

    return unauth_wrapper


def authenticate_api(f):
    @wraps(f)
    def auth_api_wrapper(*args, **kwargs):
        if "usu_id" in session:
            try:
                g.usuario = Usuario.get_by_id(session["usu_id"])
            except IndexError:
                logger.debug("User not found")
            else:
                return f(*args, **kwargs)
        return resposta("Authorization required", 401)

    return auth_api_wrapper


@app.route("/")
@authenticate
def page_index():
    return redirect(url_for("page_resumo"))


@app.route("/entrar")
@unauthenticate
def page_entrar():
    return render_template("login.html")


@app.route("/cadastrar")
@unauthenticate
def page_cadastrar():
    return render_template("signup.html")


@app.route("/conta")
@authenticate
def page_conta():
    return render_template("adicionar_conta.html")


@app.route("/pagamento")
@authenticate
def page_pagamento():
    return render_template("pagamento.html")


@app.route("/resumo")
@authenticate
def page_resumo():
    return render_template("resumo.html")


@app.route("/configuracoes")
@authenticate
def page_configuracoes():
    return render_template("configurações.html")


@app.route("/api/cadastrar/usuario", methods=["POST"])
@unauthenticate
def api_cadastrar_usuario():
    request_data = request.form.to_dict() or request.get_json(force=True, silent=True) or {}

    usu_nome = request_data.get("usu_nome", None)
    usu_email = request_data.get("usu_email", None)
    usu_senha = request_data.get("usu_senha", None)
    if usu_email and usu_senha and usu_nome:
        try:
            usuario = Usuario.new(usu_nome=usu_nome, usu_email=usu_email, usu_senha=usu_senha)
        except Exception as e:
            logger.debug(e)
            return resposta("Não foi possivel cadastrar o usuario", 400)
        else:
            session["usu_id"] = usuario.usu_id
            return resposta(usuario, 201)
    else:
        return resposta("Dados faltando para cadastro", 400)


@app.route("/api/entrar", methods=["POST"])
@unauthenticate
def api_entrar():
    request_data = request.form.to_dict() or request.get_json(force=True, silent=True) or {}

    usu_email = request_data.get("usu_email", None)
    usu_senha = request_data.get("usu_senha", None)
    if usu_email and usu_senha:
        try:
            usuario = Usuario.authenticate(usu_email, usu_senha)
        except Exception as e:
            logger.debug(e)
            return resposta("Não foi possivel autenticar o usuario", 400)
        else:
            session["usu_id"] = usuario.usu_id
            return resposta(usuario)
    else:
        return resposta("Dados faltando para login", 400)


@app.route("/api/sair")
@unauthenticate
def api_sair():
    logger.debug("Logged out")
    return resposta("Sucesso ao sair")


@app.route("/api/usuarios")
@authenticate_api
def api_usuarios():
    try:
        return resposta(Usuario.get_all())
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro ocorreu ao retornar usuarios", 400)


@app.route("/api/contas")
@authenticate_api
def api_contas():
    try:
        return Conta.get_by_user_id(g.usuario.usu_id)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro ocorreu ao buscar contas", 400)


@app.route("/api/pagamentos")
@authenticate_api
def api_pagamentos():
    try:
        return Pagamento.get_by_user_id(g.usuario.usu_id)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro ocorreu ao buscar pagamentos", 400)


@app.route("/api/cadastrar/conta", methods=["POST"])
@authenticate_api
def api_cadastrar_conta():
    request_data = request.form.to_dict() or request.get_json(force=True, silent=True) or {}
    try:
        return resposta(Conta.new_conta(**request_data), 201)
    except Exception as e:
        logger.debug(e)
        return resposta("Não foi possivel cadastrar a conta", 400)


@app.route("/api/cadastrar/pagamento", methods=["POST"])
@authenticate_api
def api_cadastrar_pagamento():
    request_data = request.form.to_dict() or request.get_json(force=True, silent=True) or {}
    try:
        return resposta(Pagamento.new(**request_data), 201)
    except Exception as e:
        logger.debug(e)
        return resposta("Não foi possivel cadastrar o pagamento", 400)


logger = utils.get_logger(__file__)
if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
