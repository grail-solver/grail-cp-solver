class CustomError(Exception):
    pass


class EmailSyntaxeError(CustomError):
    """A specific error"""
    pass


def process():
    raise EmailSyntaxeError("The email address is not valid!")


def caller():
    try:
        process()
    except Exception:
        pass
