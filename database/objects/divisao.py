from __future__ import annotations
import typing
import database.utils
import database
import utils
import database.objects
from errors import KnownError


class BillPartError(KnownError):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message, status)


class BillPartIDNotFoundError(BillPartError):
    def __init__(self, *, div_id):
        self.div_id = div_id
        super().__init__("Divisão não encontrada", 404)


class Divisao:
    def __init__(self, div_id, con_id, usu_id, div_valor):
        self.div_id = div_id
        self.con_id = con_id
        self.usu_id = usu_id
        self.div_valor = div_valor

    def __repr__(self):
        return f"""<Divisao {self.div_id} {self.con_id} {self.usu_id} {self.div_valor}>"""

    @property
    def con_object(self) -> database.objects.Conta:
        return database.objects.Conta.get_by_id(self.con_id)

    @property
    def usu_object(self) -> database.objects.Usuario:
        return database.objects.Usuario.get_by_id(self.usu_id)

    def json(self) -> dict:
        return {
            "div_id": self.div_id,
            "con_id": self.con_id,
            "usu_object": self.usu_object,
            "div_valor": self.div_valor
        }

    @classmethod
    def get_by_id(cls, div_id: typing.Union[int, str]) -> Divisao:
        try:
            return cls.get(sql_select=database.utils.make_select("div_id", t_name="divisao"), values={"div_id": div_id})[0]
        except IndexError:
            raise BillPartIDNotFoundError(div_id=div_id)

    @classmethod
    def get_by_user_id(cls, usu_id: typing.Union[int, str]) -> typing.List[Divisao]:
        return cls.get(sql_select=database.utils.make_select("usu_id", t_name="divisao"), values={"usu_id": usu_id})

    @classmethod
    def get(cls, *, sql_select: str, values: dict) -> typing.List[Divisao]:
        with database.Database() as db:
            return [cls(**objct_dict) for objct_dict in db.select(sql_select, **values)]


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    pass
