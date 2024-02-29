from typing import TypeVar, Generic

T = TypeVar("T")


class ORMBase(Generic[T]):
    """
    ORMBase classes serve the purpose of providing Sqlalchemy's Base.
    - model: A class that inherits from Sqlalchemy's Base.
    """

    def __init__(self, model: T):
        self.model = model

    def get_columns(self, columns: list[str] | None = None) -> list:
        """
        Retrieves the columns specified in the 'columns' parameter.
        """
        if columns:
            return [getattr(self.model, column) for column in columns]
        return [self.model]

    def get_result(self, result: T, columns: list) -> T:
        """
        When all columns (*) are selected, use scalar_one_or_none(),
        When selecting a few columns, use mappings().first().
        """
        if len(columns) == 1:
            return result.scalar_one_or_none()
        return result.mappings().first()

    def get_results(self, results: list[T], columns: list) -> list[T]:
        """
        When all columns (*) are selected, use scalars().all(),
        When selecting a few columns, use mappings().all().
        """

        if len(columns) == 1:
            return results.scalars().all()
        return results.mappings().all()

    def get_filters_by_operator(self, kwargs: dict, operator: str) -> list:
        """
        Creates filters based on the 'kwargs' parameter and the specified 'operator'.
        """
        match operator:
            case "eq":
                return [(getattr(self.model, k) == v) for k, v in kwargs.items() if hasattr(self.model, k)]
            case "ne":
                return [(getattr(self.model, k) != v) for k, v in kwargs.items() if hasattr(self.model, k)]
            case "lt":
                return [(getattr(self.model, k) < v) for k, v in kwargs.items() if hasattr(self.model, k)]
            case "lte":
                return [(getattr(self.model, k) <= v) for k, v in kwargs.items() if hasattr(self.model, k)]
            case "gt":
                return [(getattr(self.model, k) > v) for k, v in kwargs.items() if hasattr(self.model, k)]
            case "gte":
                return [(getattr(self.model, k) >= v) for k, v in kwargs.items() if hasattr(self.model, k)]
            case _:
                raise ValueError("Invalid operator")
