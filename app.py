from flask import Flask, render_template, redirect, url_for, Response
import os
import settings
import utils
from responses import Error
from database.objects import Divisao, Conta, Pagamento, Usuario
import json

app = Flask(__name__, static_folder=os.path.join(settings.ROOT_DIRPATH, "static"), template_folder=os.path.join(settings.ROOT_DIRPATH, "templates"))


@app.route("/")
def page_index():
    return redirect(url_for("page_resumo"))


@app.route("/entrar")
def page_entrar():
    return render_template("login.html")


@app.route("/cadastrar")
def page_cadastrar():
    return render_template("signup.html")


@app.route("/conta")
def page_conta():
    return render_template("adicionar_conta.html")


@app.route("/pagamento")
def page_pagamento():
    return render_template("pagamento.html")


@app.route("/resumo")
def page_resumo():
    return render_template("resumo.html")


@app.route("/configuracoes")
def page_configuracoes():
    return render_template("configuracoes.html")


@app.route("/api/usuarios")
def api_usuarios():
    try:
        return Response(response=json.dumps(Usuario.get_all(), default=lambda x: x.json(), indent=4), mimetype="application/json")
    except Exception as e:
        logger.exception(e)
        return Response(response=json.dumps(Error("Um erro ocorreu ao retornar usuarios"), default=lambda x: x.json(), indent=4), status=400, mimetype="application/json")


@app.route("/api/entrar")
def api_entrar():
    pass


@app.route("/api/contas")
def api_contas():
    pass


@app.route("/api/pagamentos")
def api_pagamentos():
    pass


@app.route("/api/cadastrar/usuario")
def api_cadastrar_usuario():
    pass


@app.route("/api/cadastrar/conta")
def api_cadastrar_conta():
    pass


@app.route("/api/cadastrar/pagamento")
def api_cadastrar_pagamento():
    pass


logger = utils.get_logger(__file__)
if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
