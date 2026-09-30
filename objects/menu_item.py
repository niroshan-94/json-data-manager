from collections.abc import Callable
class MenuItem[TReq,TRes]:
    # The __init__ method sets up the initial state/attributes of the object
    def __init__(self, title: str, action: Callable[[TReq], TRes]):
        self.title = title    # Instance attribute
        self.action = action  # Instance attribute