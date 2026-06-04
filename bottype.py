from dataclasses import dataclass

@dataclass
class Context:
    args: list[str]
    rargs: list[str]
    msg: str
    user: str
    prefix: str
    wins: str
    cmd: dict