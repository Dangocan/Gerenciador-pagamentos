from __future__ import annotations
import typing
from datetime import datetime, timedelta
import database.utils
import database
import settings
import utils
import database.objects


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

    # @classmethod
    # def new(cls, *, con_id, usu_id, div_valor) -> Divisao:
    #     logger.debug("New division")
    #     object_dict = {"con_id": con_id, "usu_id": usu_id, "div_valor": div_valor}
    #     with database.Database() as db:
    #         sql_insert = database.utils.make_insert("con_id", "usu_id", "div_valor", t_name="divisao")
    #         logger.debug(f"SQL Insert: {sql_insert}")
    #         logger.debug(f"SQL Values: {object_dict}")
    #         div_id = db.insert(sql_insert, **object_dict)
    #
    #         sql_select = database.utils.make_select("div_id", t_name="divisao")
    #         logger.debug(f"SQL Select: {sql_select}")
    #         return cls(**db.select(sql_select, div_id=div_id)[0])

    @classmethod
    def get_by_id(cls, div_id):
        return cls.get(sql_select=database.utils.make_select("div_id", t_name="divisao"), values={"div_id": div_id})[0]

    @classmethod
    def get(cls, *, sql_select: str, values: dict) -> typing.List[Divisao]:
        with database.Database() as db:
            logger.debug(f"SQL Select: {sql_select}")
            logger.debug(f"SQL Values: {values}")
            return [cls(**objct_dict) for objct_dict in db.select(sql_select, **values)]


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    d = Divisao.new(con_id="1", usu_id="1", div_valor="17.5")
    print(d)
