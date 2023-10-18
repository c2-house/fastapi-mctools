from typing import TypeVar, Generic

T = TypeVar("T")


class ORMBase(Generic[T]):
    """
    ORMBase들은 Sqlalchemy의 Base를 넣어주는 역할을 합니다.
    - model: Sqlalchemy의 Base를 상속받은 클래스
    """

    def __init__(self, model: T):
        self.model = model
