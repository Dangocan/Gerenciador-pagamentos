from flask import Response
import json
import typing
from database.objects import *


def resposta(dado: typing.Union[str, list, dict, Conta, Usuario, Pagamento, Divisao], status: int = 200, *, msg: str = None) -> Response:
    if type(msg) is str:
        data = {
            "message": dado
        }
    else:
        data = dado
    if msg is not None:
        data.update({"message": msg})
    return Response(response=json.dumps(data, default=lambda x: x.json(), indent=4), status=status, mimetype="application/json")
