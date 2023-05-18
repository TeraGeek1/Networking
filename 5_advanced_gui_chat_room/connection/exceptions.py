class NoNameError(Exception):
    """Raised when you try to connect without a name"""

    def __init__(
        self, message="Name entry cannot be Empty when trying to connect"
    ) -> None:
        self.message = message
        super().__init__(self.message)
