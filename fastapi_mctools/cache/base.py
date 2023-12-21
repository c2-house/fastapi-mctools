from typing import Protocol, Any, Optional, runtime_checkable


@runtime_checkable
class CacheStrategy(Protocol):
    """
    캐싱 전략을 정의하기 위한 프로토콜.
    캐시 관리를 위한 기본적인 메서드들을 정의합니다.

    Methods:
        get: 캐시에서 키에 해당하는 값을 가져옵니다.
        set: 캐시에 키와 값을 설정합니다.
        delete: 캐시에서 키에 해당하는 값을 삭제합니다.
    """

    async def get(self, key: str) -> Any:
        """
        캐시에서 주어진 키에 해당하는 값을 비동기적으로 가져옵니다.

        Args:
            key (str): 캐시에서 조회할 키.

        Returns:
            Any: 키에 해당하는 캐시 값.
        """
        ...

    async def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """
        캐시에 주어진 키와 값을 비동기적으로 설정합니다.

        Args:
            key (str): 캐시에 저장할 키.
            value (Any): 캐시에 저장할 값.
            timeout (Optional[int]): 캐시의 만료 시간(초). 기본값은 None입니다.
        """
        ...

    async def delete(self, key: str) -> None:
        """
        캐시에서 주어진 키에 해당하는 값을 비동기적으로 삭제합니다.

        Args:
            key (str): 삭제할 캐시의 키.
        """
        ...
