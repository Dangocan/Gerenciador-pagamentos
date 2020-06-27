from __future__ import annotations
import typing
from datetime import datetime
import database.utils
import database
import settings
import utils
import secrets
import hashlib


def hash_password(password: str, salt: str = None) -> typing.Tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(20)
    hashed_password = hashlib.sha256((salt + password).encode("UTF-8")).hexdigest()
    return hashed_password, salt


def is_valid_email(email: str) -> bool:
    return email != ""


def is_valid_password(password: str) -> bool:
    return type(password) is str and len(password) > 0


def is_valid_name(name: str) -> bool:
    return type(name) is str and len(name) > 0


class Usuario:
    def __init__(self, usu_id: int, usu_email: str, usu_nome: str, usu_senha: str, usu_salt: str, usu_datahora: str):
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
    def new(cls, *, usu_email: str, usu_nome: str, usu_senha: str) -> Usuario:
        logger.debug("New user")
        if not (is_valid_email(usu_email) and is_valid_name(usu_nome) and is_valid_password(usu_senha)):
            logger.debug(f"Invalid field(s)")
            raise Exception("Campos inválidos")
        usu_datahora = datetime.utcnow().strftime(settings.STDDATETIMEFORMAT)
        usu_senha, usu_salt = hash_password(usu_senha)
        object_dict = {"usu_email": usu_email, "usu_nome": usu_nome, "usu_senha": usu_senha, "usu_datahora": usu_datahora, "usu_salt": usu_salt}
        with database.Database() as db:
            sql_insert = database.utils.make_insert("usu_email", "usu_nome", "usu_senha", "usu_salt", "usu_datahora", t_name="usuario")
            logger.debug(f"SQL Insert: {sql_insert}")
            logger.debug(f"SQL Values: {object_dict}")
            usu_id = db.insert(sql_insert, **object_dict)

            sql_select = database.utils.make_select("usu_id", t_name="usuario")
            logger.debug(f"SQL Select: {sql_select}")
            print(db.select(sql_select, usu_id=usu_id)[0])
            return cls(**db.select(sql_select, usu_id=usu_id)[0])

    @classmethod
    def update(cls, *, usu_id: typing.Union[int, str], usu_email: str = None, usu_nome: str = None, usu_senha: str = None) -> Usuario:
        logger.debug("Update user")
        updates = {"usu_id": usu_id}
        if usu_email is not None:
            if is_valid_email(usu_email):
                updates["usu_email"] = usu_email
            else:
                logger.debug("Invalid email")
                raise Exception("Campo inválido")
        if usu_nome is not None:
            if is_valid_name(usu_nome):
                updates["usu_nome"] = usu_nome
            else:
                logger.debug("Invalid name")
                raise Exception("Campo inválido")
        if usu_senha is not None:
            if is_valid_password(usu_senha):
                updates["usu_senha"], updates["usu_salt"] = hash_password(usu_senha)
            else:
                logger.debug("Invalid password")
                raise Exception("Campo inválido")

        with database.Database() as db:
            sql_update = database.utils.make_update(where_list=["usu_id"], set_list=list(updates.keys()), t_name="usuario")
            logger.debug(f"SQL Update: {sql_update}")
            logger.debug(f"SQL Values: {updates}")
            db.update(sql_update, **updates)

            sql_select = database.utils.make_select("usu_id", t_name="usuario")
            logger.debug(f"SQL Select: {sql_select}")
            logger.debug(f"ID: {usu_id}")
            return cls(**db.select(sql_select, usu_id=usu_id)[0])

    @classmethod
    def get_by_id(cls, usu_id):
        return cls.get(sql_select=database.utils.make_select("usu_id", t_name="usuario"), values={"usu_id": usu_id})[0]

    @classmethod
    def get_all(cls):
        return cls.get(sql_select=F"""SELECT * FROM `usuario`""", values={})

    @classmethod
    def get_by_email(cls, usu_email):
        return cls.get(sql_select=database.utils.make_select("usu_email", t_name="usuario"), values={"usu_email": usu_email})[0]

    @classmethod
    def get(cls, *, sql_select: str, values: dict) -> typing.List[Usuario]:
        with database.Database() as db:
            logger.debug(f"SQL Select: {sql_select}")
            logger.debug(f"SQL Values: {values}")
            return [cls(**objct_dict) for objct_dict in db.select(sql_select, **values)]

    @classmethod
    def authenticate(cls, usu_email: str, usu_senha: str) -> Usuario:
        logger.debug(f"Authenticate user with email: {usu_email}")
        try:
            user = cls.get_by_email(usu_email=usu_email)
        except IndexError:
            logger.debug("User not found")
        except Exception as e:
            logger.exception(e)
            raise Exception("Um erro desconhecido ocorreu ao autenticar o usuário")
        else:
            if user.usu_senha == hash_password(usu_senha, user.usu_salt)[0]:
                logger.debug("Authenticated")
                return user
            else:
                logger.debug("Wrong password")
        raise Exception("Email ou senha inválido")


logger = utils.get_logger(__file__)

if __name__ == "__main__":
    pass
    # u = Usuario.new(usu_email="a@a.com", usu_nome="a", usu_senha="senha")
    # u = Usuario.new(usu_email="b@b.com", usu_nome="b", usu_senha="senhb")
    # u = Usuario.get_by_id("1")
    # u = Usuario.update(usu_id=1, usu_nome="jonasi")
    # print(u)
    # print(hash_password("alex", "039df246fbdb0a54611af4a5411188d729c8d7d5")[0] == "180f7811021dad67cffefc1155f0e0a41167d910d749ad5d48927f4b5894fe19")
