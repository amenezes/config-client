class RequestTokenException(Exception):
    def __init__(self, message: str = "Faield to retrieve oauth2 access_token") -> None:
        super().__init__(message)


class RequestFailedException(Exception):
    def __init__(
        self, url: str, message: str = "Failed to perform request: [URL='{url}']"
    ) -> None:
        super().__init__(message.format(url=url))
