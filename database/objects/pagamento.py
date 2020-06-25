from __future__ import annotations
import typing
from datetime import datetime, timedelta
import database.utils
import database
import settings
import utils
import database.objects


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

    @property
    def usu_pagador_object(self) -> database.objects.Usuario:
        return database.objects.Usuario.get_by_id(self.usu_pagador_id)

    @property
    def usu_receptor_object(self) -> database.objects.Usuario:
        return database.objects.Usuario.get_by_id(self.usu_receptor_id)

    def json(self) -> dict:
        return {
            "pag_id": self.pag_id,
            "usu_pagador_object": self.usu_pagador_object,
            "usu_receptor_object": self.usu_receptor_object,
            "pag_valor": self.pag_valor,
            "pag_mensagem": self.pag_mensagem,
            "pag_datahora": self.pag_datahora,
        }

    @classmethod
    def new(cls, *, usu_pagador_id, usu_receptor_id, pag_valor, pag_mensagem) -> Pagamento:
        logger.debug("New payment")
        pag_datahora = (datetime.now() + timedelta(hours=3)).strftime(settings.STDDATETIMEFORMAT)
        object_dict = {"usu_pagador_id": usu_pagador_id, "usu_receptor_id": usu_receptor_id, "pag_valor": pag_valor, "pag_mensagem": pag_mensagem, "pag_datahora": pag_datahora}
        with database.Database() as db:
            sql_insert = database.utils.make_insert("usu_pagador_id", "usu_receptor_id", "pag_valor", "pag_mensagem", "pag_datahora", t_name="pagamento")
            logger.debug(f"SQL Insert: {sql_insert}")
            logger.debug(f"SQL Values: {object_dict}")
            pag_id = db.insert(sql_insert, **object_dict)

            sql_select = database.utils.make_select("pag_id", t_name="pagamento")
            logger.debug(f"SQL Select: {sql_select}")
            return cls(**db.select(sql_select, pag_id=pag_id)[0])

    @classmethod
    def get_by_id(cls, pag_id) -> cls:
        return cls.get(sql_select=database.utils.make_select("pag_id", t_name="pagamento"), values={"pag_id": pag_id})[0]

    @classmethod
    def get(cls, *, sql_select: str, values: dict) -> typing.List[Pagamento]:
        with database.Database() as db:
            logger.debug(f"SQL Select: {sql_select}")
            logger.debug(f"SQL Values: {values}")
            return [cls(**objct_dict) for objct_dict in db.select(sql_select, **values)]

    # @property
    # def usu_pagador_object(self):
    #     pass

    # @property
    # def usu_receptor_object(self):
    #     pass

    # @classmethod
    # def get(cls, pag_id, usu_pagador_id, usu_receptor_id, pag_valor, pag_mensagem, pag_datahora):
    #     pass


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    p = Pagamento.new(usu_pagador_id="1", usu_receptor_id="1", pag_valor="17.54", pag_mensagem="mensagem_minha")
    print(p)
