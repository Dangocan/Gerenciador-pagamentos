from flask import Flask, render_template, redirect, url_for, g, session, request
import settings
import utils
from responses import resposta
from database.objects import Conta, Pagamento, Usuario
from authentication import authenticate, unauthenticate, authenticate_api
from errors import KnownError, MissingParamsError, UserNotLoggedInError

app = Flask(__name__, static_folder=settings.STATIC_FOLDER, template_folder=settings.TEMPLATES_FOLDER)
app.secret_key = utils.get_keys()["APP_SECRET_KEY"]


# import os; print(os.urandom(16))

@app.errorhandler(500)
def handle_server_error(e):
    logger.exception(e)
    return "Um erro ocorreu no servidor"


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
    try:
        request_data = request.form.to_dict() or request.get_json(force=True, silent=True) or {}

        usu_nome = request_data.get("usu_nome", None)
        usu_email = request_data.get("usu_email", None)
        usu_senha = request_data.get("usu_senha", None)
        if usu_email and usu_senha and usu_nome:
            usuario = Usuario.new(usu_nome=usu_nome, usu_email=usu_email, usu_senha=usu_senha)
            session["usu_id"] = usuario.usu_id
            return resposta(usuario, 201)
        else:
            raise MissingParamsError()
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/entrar", methods=["POST"])
@unauthenticate
def api_entrar():
    try:
        request_data = request.form.to_dict() or request.get_json(force=True, silent=True) or {}

        usu_email = request_data.get("usu_email", None)
        usu_senha = request_data.get("usu_senha", None)
        if usu_email and usu_senha:
            usuario = Usuario.authenticate_login(usu_email, usu_senha)
            session["usu_id"] = usuario.usu_id
            return resposta(usuario)
        else:
            raise MissingParamsError()
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/sair")
@unauthenticate
def api_sair():
    try:
        logger.debug("Logged out")
        return resposta("Sucesso ao sair")
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/get/me")
@authenticate_api
def api_get_me():
    try:
        return resposta(g.usuario)
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/get/usuarios")
@authenticate_api
def api_get_usuarios():
    try:
        return resposta(Usuario.get_all())
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/get/usuario/<string:usu_id>")
@authenticate_api
def api_get_usuario(usu_id):
    try:
        return resposta(Usuario.get_by_id(usu_id))
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/get/contas")
@authenticate_api
def api_get_contas():
    try:
        return resposta(Conta.get_by_user_id(g.usuario.usu_id))
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/get/pagamentos")
@authenticate_api
def api_get_pagamentos():
    try:
        return resposta(Pagamento.get_by_user_id(g.usuario.usu_id))
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/cadastrar/conta", methods=["POST"])
@authenticate_api
def api_cadastrar_conta():
    try:
        request_data = request.form.to_dict() or request.get_json(force=True, silent=True) or {}
        return resposta(Conta.new_conta(**request_data), 201)
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/cadastrar/pagamento", methods=["POST"])
@authenticate_api
def api_cadastrar_pagamento():
    try:
        request_data = request.form.to_dict() or request.get_json(force=True, silent=True) or {}
        return resposta(Pagamento.new(**request_data), 201)
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


@app.route("/api/atualizar/usuario", methods=["POST"])
@authenticate_api
def api_atualizar_usuario():
    try:
        request_data = request.form.to_dict() or request.get_json(force=True, silent=True) or {}
        return resposta(Usuario.update(usuario=g.usuario, **request_data), 202)
    except KnownError as e:
        return resposta(e)
    except Exception as e:
        logger.exception(e)
        return resposta("Um erro desconhecido ocorreu", 400)


logger = utils.get_logger(__file__)
if __name__ == "__main__":
    utils.get_logger(__file__, log_name="werkzeug")
    app.run("0.0.0.0", debug=settings.DEVELOPMENT, port=(5000 if settings.DEVELOPMENT else 8888))
