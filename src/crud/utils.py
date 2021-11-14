class ExistenceException(Exception):
    """Exception raised when the specified value already exist in the table
    Attributes:
        field: The field that specifies the value
    """

    def __init__(self, field: str):
        self.message = f"{field} refers to a value that already exists in the table"


class NonExistenceException(Exception):
    """Exception raised when the specified value does not exist in the table
    Attributes:
        field: The field that specifies the value
    """

    def __init__(self, field: str):
        self.message = f"{field} refers to a value that does not exist in the table"