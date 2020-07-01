from __future__ import annotations
import typing
from datetime import datetime
import database.utils
import database
import settings
import utils
import database.objects
from errors import KnownError


class PaymentError(KnownError):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message, status)


class PaymentIDNotFoundError(PaymentError):
    def __init__(self, *, pag_id):
        self.pag_id = pag_id
        super().__init__("Pagamento não encontrado", 404)


class SameUserError(PaymentError):
    def __init__(self, *, usu_pagador_id, usu_receptor_id):
        self.usu_pagador_id = usu_pagador_id
        self.usu_receptor_id = usu_receptor_id
        super().__init__("Usuário não pode pagar para ele mesmo", 400)


class NaNError(PaymentError):
    def __init__(self, *, usu_pagador_id, usu_receptor_id):
        self.usu_pagador_id = usu_pagador_id
        self.usu_receptor_id = usu_receptor_id
        super().__init__("Usuários devem ser números", 400)


class Pagamento:
    def __init__(self, pag_id, usu_pagador_id, usu_receptor_id, pag_valor, pag_mensagem, pag_datahora):
        self.pag_id = pag_id
        self.usu_pagador_id = usu_pagador_id
        self.usu_receptor_id = usu_receptor_id
        self.pag_valor = pag_valor
        self.pag_mensagem = pag_mensagem
        self.pag_datahora = pag_datahora

    def __repr__(self):
        return f"""<Pagamento {self.pag_id} {self.usu_pagador_id} {self.usu_receptor_id} {self.pag_valor} {self.pag_datahora}>"""

    def __eq__(self, other: typing.Union[int, str, Pagamento]):
        if type(other) is Pagamento:
            return self.pag_id == other.pag_id
        else:
            return str(self.pag_id) == str(other)

    @property
    def usu_pagador_object(self) -> database.objects.Usuario:
        return database.objects.Usuario.get_by_id(self.usu_pagador_id)

    @property
    def usu_receptor_object(self) -> database.objects.Usuario:
        return database.objects.Usuario.get_by_id(self.usu_receptor_id)

    def json(self) -> dict:
        return {
            "pag_id": self.pag_id,
            "usu_pagador_id": self.usu_pagador_id,
            "usu_receptor_id": self.usu_receptor_id,
            "pag_valor": self.pag_valor,
            "pag_mensagem": self.pag_mensagem,
            "pag_datahora": self.pag_datahora,
            "usu_pagador_object": self.usu_pagador_object,
            "usu_receptor_object": self.usu_receptor_object
        }

    @classmethod
    def new(cls, *, usu_pagador_id: typing.Union[str, int], usu_receptor_id: typing.Union[str, int], pag_valor: typing.Union[str, float, int], pag_mensagem: str) -> Pagamento:
        logger.debug("New payment")
        pag_datahora = datetime.utcnow().strftime(settings.STDDATETIMEFORMAT)
        object_dict = {"usu_pagador_id": usu_pagador_id, "usu_receptor_id": usu_receptor_id, "pag_valor": pag_valor, "pag_mensagem": pag_mensagem, "pag_datahora": pag_datahora}
        try:
            if int(usu_pagador_id) == int(usu_receptor_id):
                raise SameUserError(usu_pagador_id=usu_pagador_id, usu_receptor_id=usu_receptor_id)
        except ValueError:
            raise NaNError(usu_pagador_id=usu_pagador_id, usu_receptor_id=usu_receptor_id)

        with database.Database() as db:
            sql_insert = database.utils.make_insert("usu_pagador_id", "usu_receptor_id", "pag_valor", "pag_mensagem", "pag_datahora", t_name="pagamento")
            pag_id = db.insert(sql_insert, **object_dict)

            sql_select = database.utils.make_select("pag_id", t_name="pagamento")
            return cls(**db.select(sql_select, pag_id=pag_id)[0])

    @classmethod
    def get_by_id(cls, pag_id: typing.Union[str, int]) -> Pagamento:
        try:
            return cls.get(sql_select=database.utils.make_select("pag_id", t_name="pagamento"), values={"pag_id": pag_id})[0]
        except IndexError:
            raise PaymentIDNotFoundError(pag_id=pag_id)

    @classmethod
    def get_by_user_id(cls, usu_id: typing.Union[str, int]) -> typing.List[Pagamento]:
        pagamentos = cls.get(sql_select=database.utils.make_select("usu_pagador_id", t_name="pagamento"), values={"usu_pagador_id": usu_id})
        for pagamento in cls.get(sql_select=database.utils.make_select("usu_receptor_id", t_name="pagamento"), values={"usu_receptor_id": usu_id}):
            if pagamento not in pagamentos:
                pagamentos.append(pagamento)
        return pagamentos

    @classmethod
    def get(cls, *, sql_select: str, values: dict) -> typing.List[Pagamento]:
        with database.Database() as db:
            return [cls(**objct_dict) for objct_dict in db.select(sql_select, **values)]


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    pass
    # p = Pagamento.new(usu_pagador_id="1", usu_receptor_id="1", pag_valor="17", pag_mensagem="mensagem_minha")
    # print(p)
