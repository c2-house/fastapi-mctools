from typing import List
from sqlalchemy import and_, or_
from fastapi_mctools.orms import T


class FilterBackend:
    def __init__(self) -> None:
        self.filters: List = []
        self.model: T = None

    def set_model(self, model: T) -> None:
        self.model = model

    def add_filter(self, condition: dict, operator: str = "eq", is_and: bool = True) -> None:
        """
        Adds a filter to the filter list.

        :param condition: dict
            - column: value, ex) {"name": "James"}
        :param operator: str
            - eq: equal =
            - ne: not equal !=
            - lt: less than <
            - lte: less than or equal <=
            - gt: greater than >
            - gte: greater than or equal >=
            - like: like
            - not_like: not like
            - in: in
            - not_in: not in
        :param is_and: bool
        """
        for column, value in condition.items():
            match operator:
                case "eq":
                    filter = getattr(self.model, column) == value
                case "ne":
                    filter = getattr(self.model, column) != value
                case "lt":
                    filter = getattr(self.model, column) < value
                case "lte":
                    filter = getattr(self.model, column) <= value
                case "gt":
                    filter = getattr(self.model, column) > value
                case "gte":
                    filter = getattr(self.model, column) >= value
                case "like":
                    filter = getattr(self.model, column).like(value)
                case "not_like":
                    filter = ~(getattr(self.model, column).like(value))
                case "in":
                    filter = getattr(self.model, column).in_(value)
                case "not_in":
                    filter = ~(getattr(self.model, column).in_(value))
                case _:
                    raise ValueError("Invalid operator")

            self.filters.append((filter, is_and))

    def compile(self):
        if not self.filters:
            raise ValueError("No filter added")

        compiled_filter, is_and = self.filters[0]

        for condition, next_is_and in self.filters[1:]:
            if is_and:
                compiled_filter = and_(compiled_filter, condition)
            else:
                compiled_filter = or_(compiled_filter, condition)
            is_and = next_is_and

        return compiled_filter
