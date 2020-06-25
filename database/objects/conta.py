from __future__ import annotations
import typing
from datetime import datetime, timedelta
import database.utils
import database
import settings
import utils
import database.objects


class Conta:
    def __init__(self, con_id, usu_id, con_titulo, con_descricao, con_datahora):
        self.con_id = con_id
        self.usu_id = usu_id
        self.con_titulo = con_titulo
        self.con_descricao = con_descricao
        self.con_datahora = con_datahora

    def __repr__(self):
        return f"""<Conta {self.con_id} {self.usu_id} {self.con_titulo} {self.con_descricao} {self.con_datahora}>"""

    @property
    def usu_object(self) -> database.objects.Usuario:
        return database.objects.Usuario.get_by_id(self.usu_id)

    @property
    def con_divisions(self) -> typing.List[database.objects.divisao.Divisao]:
        sql_select = database.utils.make_select("con_id", t_name="divisao")
        values = {"con_id": self.con_id}
        with database.Database() as db:
            logger.debug(f"SQL Select: {sql_select}")
            logger.debug(f"SQL Values: {values}")
            return [database.objects.divisao.Divisao(**objct_dict) for objct_dict in db.select(sql_select, **values)]

    def json(self) -> dict:
        return {
            "con_id": self.con_id,
            "usu_object": self.usu_object,
            "con_titulo": self.con_titulo,
            "con_descricao": self.con_descricao,
            "con_datahora": self.con_datahora,
            "con_divisions": self.con_divisions
        }

    # @classmethod
    # def new(cls, *, usu_id, con_titulo, con_descricao) -> Conta:
    #     logger.debug("New bill")
    #     con_datahora = (datetime.now() + timedelta(hours=3)).strftime(settings.STDDATETIMEFORMAT)
    #     object_dict = {"usu_id": usu_id, "con_titulo": con_titulo, "con_descricao": con_descricao, "con_datahora": con_datahora}
    #     with database.Database() as db:
    #         sql_insert = database.utils.make_insert("usu_id", "con_titulo", "con_descricao", "con_datahora", t_name="conta")
    #         logger.debug(f"SQL Insert: {sql_insert}")
    #         logger.debug(f"SQL Values: {object_dict}")
    #         con_id = db.insert(sql_insert, **object_dict)
    #
    #         sql_select = database.utils.make_select("con_id", t_name="conta")
    #         logger.debug(f"SQL Select: {sql_select}")
    #         return cls(**db.select(sql_select, con_id=con_id)[0])

    @classmethod
    def get_by_id(cls, con_id):
        return cls.get(sql_select=database.utils.make_select("con_id", t_name="conta"), values={"con_id": con_id})[0]

    @classmethod
    def get(cls, *, sql_select: str, values: dict) -> typing.List[Conta]:
        with database.Database() as db:
            logger.debug(f"SQL Select: {sql_select}")
            logger.debug(f"SQL Values: {values}")
            return [cls(**objct_dict) for objct_dict in db.select(sql_select, **values)]

    @classmethod
    def new_conta(cls, *, con_titulo, con_descricao, usu_id, con_divisoes) -> Conta:
        logger.debug("New bill")
        con_datahora = (datetime.now() + timedelta(hours=3)).strftime(settings.STDDATETIMEFORMAT)
        conta_dict = {"usu_id": usu_id, "con_titulo": con_titulo, "con_descricao": con_descricao, "con_datahora": con_datahora}
        if len(con_divisoes) == 0:
            raise Exception("Not enough divisions")

        with database.database.Database() as db:
            sql_insert = database.utils.make_insert("usu_id", "con_titulo", "con_descricao", "con_datahora", t_name="conta")
            logger.debug(f"SQL Insert: {sql_insert}")
            logger.debug(f"SQL Values: {conta_dict}")
            con_id = db.insert(sql_insert, **conta_dict)

            divisao_dicts = [{"con_id": con_id, "usu_id": div["usu_id"], "div_valor": div["div_valor"]} for div in con_divisoes]
            for divisao_dict in divisao_dicts:
                logger.debug("New division")
                sql_insert = database.utils.make_insert("con_id", "usu_id", "div_valor", t_name="divisao")
                logger.debug(f"SQL Insert: {sql_insert}")
                logger.debug(f"SQL Values: {divisao_dict}")
                db.insert(sql_insert, **divisao_dict)

            sql_select = database.utils.make_select("con_id", t_name="conta")
            logger.debug(f"SQL Select: {sql_select}")
            return cls(**db.select(sql_select, con_id=con_id)[0])


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    import json
    c = Conta.get_by_id(7)
    print(json.dumps(c, default=lambda x: x.json(), indent=4))
    # c = Conta.new_conta(con_titulo="titulo", con_descricao="descricao", usu_id="1", con_divisoes=[{"usu_id": "1", "div_valor": "17.50"}, {"usu_id": "2", "div_valor": "17.50"}])
    # c = Conta.new(usu_id="1", con_titulo="meutitulo", con_descricao="minhadescricao")
    #

    #
    # # print(c.json())

