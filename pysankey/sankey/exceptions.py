class PySankeyException(Exception):
    """Generic PySankey Exception."""


class NullsInFrame(PySankeyException):
    pass


class LabelMismatch(PySankeyException):
    pass
