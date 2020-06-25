from __future__ import annotations
import typing
from datetime import datetime, timedelta
import database.utils
import database
import settings
import utils


class Usuario:
    def __init__(self, usu_id, usu_email, usu_nome, usu_senha, usu_salt, usu_datahora):
        self.usu_id = usu_id
        self.usu_email = usu_email
        self.usu_nome = usu_nome
        self.usu_senha = usu_senha
        self.usu_salt = usu_salt
        self.usu_datahora = usu_datahora

    def __repr__(self):
        return f"""<Usuario {self.usu_id} {self.usu_email} {self.usu_nome} {self.usu_datahora}>"""

    def json(self) -> dict:
        return {
            "usu_id": self.usu_id,
            "usu_email": self.usu_email,
            "usu_nome": self.usu_nome,
            "usu_datahora": self.usu_datahora
        }

    @classmethod
    def new(cls, *, usu_email, usu_nome, usu_senha) -> Usuario:
        logger.debug("New user")
        usu_datahora = (datetime.now() + timedelta(hours=3)).strftime(settings.STDDATETIMEFORMAT)
        usu_salt = "SALT"
        object_dict = {"usu_email": usu_email, "usu_nome": usu_nome, "usu_senha": usu_senha, "usu_datahora": usu_datahora, "usu_salt": usu_salt}
        with database.Database() as db:
            sql_insert = database.utils.make_insert("usu_email", "usu_nome", "usu_senha", "usu_salt", "usu_datahora", t_name="usuario")
            logger.debug(f"SQL Insert: {sql_insert}")
            logger.debug(f"SQL Values: {object_dict}")
            usu_id = db.insert(sql_insert, **object_dict)

            sql_select = database.utils.make_select("usu_id", t_name="usuario")
            logger.debug(f"SQL Select: {sql_select}")
            return cls(**db.select(sql_select, usu_id=usu_id)[0])

    @classmethod
    def get_by_id(cls, usu_id):
        return cls.get(sql_select=database.utils.make_select("usu_id", t_name="usuario"), values={"usu_id": usu_id})[0]

    @classmethod
    def get_all(cls):
        return cls.get(sql_select=F"""SELECT * FROM `usuario`""")

    @classmethod
    def get_by_email(cls, usu_email):
        return cls.get(sql_select=database.utils.make_select("usu_email", t_name="usuario"), values={"usu_email": usu_email})[0]

    @classmethod
    def get(cls, *, sql_select: str, values: dict) -> typing.List[Usuario]:
        with database.Database() as db:
            logger.debug(f"SQL Select: {sql_select}")
            logger.debug(f"SQL Values: {values}")
            return [cls(**objct_dict) for objct_dict in db.select(sql_select, **values)]


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    # u = Usuario.new(usu_email="a@a.com", usu_nome="a", usu_senha="senha")
    # u = Usuario.new(usu_email="b@b.com", usu_nome="b", usu_senha="senhb")
    print(u)
