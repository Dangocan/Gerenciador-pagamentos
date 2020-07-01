from __future__ import annotations
import typing
from datetime import datetime
import database.utils
import database
import settings
import utils
import database.objects
from errors import KnownError


class BillError(KnownError):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message, status)


class BillIDNotFoundError(BillError):
    def __init__(self, *, con_id):
        self.con_id = con_id
        super().__init__("Conta não encontrada", 404)


class BillNotEnoughPartsError(BillError):
    def __init__(self):
        super().__init__("Conta não tem divisões", 400)


class ValueNaNError(BillError):
    def __init__(self, *, div_valor):
        self.div_valor = div_valor
        super().__init__("Valor da divisão deve ser um número real", 400)


class EmptyTitleError(BillError):
    def __init__(self):
        super().__init__("Título da conta não pode ser vazio", 400)


class Conta:
    def __init__(self, con_id, usu_id, con_titulo, con_descricao, con_datahora):
        self.con_id = con_id
        self.usu_id = usu_id
        self.con_titulo = con_titulo
        self.con_descricao = con_descricao
        self.con_datahora = con_datahora

    def __repr__(self):
        return f"""<Conta {self.con_id} {self.usu_id} {self.con_titulo} {self.con_descricao} {self.con_datahora}>"""

    def __eq__(self, other: typing.Union[int, str, Conta]):
        if type(other) is Conta:
            return self.con_id == other.con_id
        else:
            return str(self.con_id) == str(other)

    @property
    def usu_object(self) -> database.objects.Usuario:
        return database.objects.Usuario.get_by_id(self.usu_id)

    @property
    def con_divisions(self) -> typing.List[database.objects.divisao.Divisao]:
        sql_select = database.utils.make_select("con_id", t_name="divisao")
        values = {"con_id": self.con_id}
        with database.Database() as db:
            return [database.objects.divisao.Divisao(**objct_dict) for objct_dict in db.select(sql_select, **values)]

    def json(self) -> dict:
        return {
            "con_id": self.con_id,
            "usu_id": self.usu_id,
            "con_titulo": self.con_titulo,
            "con_descricao": self.con_descricao,
            "con_datahora": self.con_datahora,
            "con_divisoes": self.con_divisions,
            "usu_object": self.usu_object
        }

    @classmethod
    def new_conta(cls, *, con_titulo, con_descricao, usu_id, con_divisoes) -> Conta:
        logger.debug("New bill")
        con_datahora = datetime.utcnow().strftime(settings.STDDATETIMEFORMAT)
        if con_titulo == "":
            raise EmptyTitleError()
        conta_dict = {"usu_id": usu_id, "con_titulo": con_titulo, "con_descricao": con_descricao, "con_datahora": con_datahora}
        if len(con_divisoes) == 0:
            raise BillNotEnoughPartsError()

        with database.database.Database() as db:
            sql_insert = database.utils.make_insert("usu_id", "con_titulo", "con_descricao", "con_datahora", t_name="conta")
            con_id = db.insert(sql_insert, **conta_dict)

            divisao_dicts = [{"con_id": con_id, "usu_id": div["usu_id"], "div_valor": div["div_valor"]} for div in con_divisoes]
            for divisao_dict in divisao_dicts:
                try:
                    divisao_dict["div_valor"] = float(divisao_dict["div_valor"])
                except ValueError:
                    raise ValueNaNError(div_valor=divisao_dict["div_valor"])

                sql_insert = database.utils.make_insert("con_id", "usu_id", "div_valor", t_name="divisao")
                db.insert(sql_insert, **divisao_dict)

            sql_select = database.utils.make_select("con_id", t_name="conta")
            return cls(**db.select(sql_select, con_id=con_id)[0])

    @classmethod
    def get_by_id(cls, con_id) -> Conta:
        try:
            return cls.get(sql_select=database.utils.make_select("con_id", t_name="conta"), values={"con_id": con_id})[0]
        except IndexError:
            raise BillIDNotFoundError(con_id=con_id)

    @classmethod
    def get_by_user_id(cls, usu_id: typing.Union[int, str]) -> typing.List[Conta]:
        contas = cls.get(sql_select=database.utils.make_select("usu_id", t_name="conta"), values={"usu_id": usu_id})
        divisoes = database.objects.Divisao.get_by_user_id(usu_id)
        for divisao in divisoes:
            if divisao.con_id not in contas:
                contas.append(divisao.con_object)
        return contas

    @classmethod
    def get(cls, *, sql_select: str, values: dict) -> typing.List[Conta]:
        with database.Database() as db:
            return [cls(**objct_dict) for objct_dict in db.select(sql_select, **values)]


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    pass
    c = Conta.new_conta(con_titulo="titulo", con_descricao="descricao", usu_id="1", con_divisoes=[{"usu_id": "1", "div_valor": "17.50"}, {"usu_id": "2", "div_valor": "17.50"}])
    print(c.json())
