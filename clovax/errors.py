class UnauthorizedError(Exception):
    """Unauthorized error"""

    def __str__(self):
        return "Unauthorized error. Maybe invalid cookie or Not registered CLOVA X yet."


class NoTokenSetError(Exception):
    """No token set error"""

    def __str__(self):
        return "No token provided yet. Please set token with get_cookie() method."


class TooManyRequestsError(Exception):
    """Too many requests error"""

    def __str__(self):
        return "Too many requests. Please try again later."
