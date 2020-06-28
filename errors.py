import utils


class KnownError(Exception):
    def __init__(self, message: str, status: int = 400):
        self.message = message
        self.status = status
        logger.debug(F"New error: {self!r}")

    def __repr__(self) -> str:
        return F"<{self.error_name} {self.status} {self.message}>"

    def __str__(self):
        return self.message

    @property
    def error_name(self):
        return type(self).__name__

    @property
    def json_data(self) -> dict:
        return self.__dict__

    def json(self) -> dict:
        return {
            "error_name": type(self).__name__,
            **self.json_data
        }


class UserNotLoggedInError(KnownError):
    def __init__(self):
        super().__init__(f"Acesso negado: usuário não está logado", 401)


class MissingParamsError(KnownError):
    def __init__(self):
        super().__init__(f"Parâmetros faltando", 400)


logger = utils.get_logger(__file__)
if __name__ == "__main__":
    pass
    # print(isinstance(Teste("teste"), KnownError))
