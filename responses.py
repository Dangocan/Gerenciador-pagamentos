class Error:
    def __init__(self, msg: str):
        self.message = msg

    def json(self):
        return {
            "message": self.message
        }

