from __future__ import annotations
from flask import Response
import json
import typing
from database.objects import *
from errors import KnownError


def resposta(mensagem: typing.Union[str, KnownError, Conta, Usuario, Pagamento, Divisao, typing.List[Conta], typing.List[Usuario], typing.List[Pagamento], typing.List[Divisao]], status: int = 200) -> Response:
    if isinstance(mensagem, KnownError):
        response = mensagem
        status = mensagem.status
    elif type(mensagem) is str:
        response = {"mensagem": mensagem}
    else:
        response = mensagem
    return Response(response=json.dumps(response, default=lambda x: x.json(), indent=4), status=status, mimetype="application/json")
