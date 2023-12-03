from typing import TypeVar, Generic

T = TypeVar("T")


class ORMBase(Generic[T]):
    """
    ORMBase들은 Sqlalchemy의 Base를 넣어주는 역할을 합니다.
    - model: Sqlalchemy의 Base를 상속받은 클래스
    """

    def __init__(self, model: T):
        self.model = model

    def get_columns(self, columns: list[str] | None = None) -> list:
        """
        columns에 해당하는 컬럼들을 가져옵니다.
        """
        if columns:
            return [getattr(self.model, column) for column in columns]
        return [self.model]

    def get_result(self, result: T, columns: list) -> T:
        """
        Column 전체 일 때(*)는 scalar_one()을 사용하고,
        몇 개의 Column을 선택할 때는 mappings().first()를 사용합니다.
        """
        if len(columns) == 1:
            return result.scalar_one()
        return result.mappings().first()

    def get_results(self, results: list[T], columns: list) -> list[T]:
        """
        Column 전체 일 때(*)는 scalars().all()을 사용하고,
        몇 개의 Column을 선택할 때는 mappings().all()를 사용합니다.
        """

        if len(columns) == 1:
            return results.scalars().all()
        return results.mappings().all()
