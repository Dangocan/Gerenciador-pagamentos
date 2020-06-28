from flask import Response
import json
import typing
from database.objects import *


def resposta(mensagem: typing.Union[str, Conta, Usuario, Pagamento, Divisao, typing.List[Conta], typing.List[Usuario], typing.List[Pagamento], typing.List[Divisao]], status: int = 200) -> Response:
    if type(mensagem) is str:
        response = {"mensagem": mensagem}
    else:
        response = mensagem
    return Response(response=json.dumps(response, default=lambda x: x.json(), indent=4), status=status, mimetype="application/json")
