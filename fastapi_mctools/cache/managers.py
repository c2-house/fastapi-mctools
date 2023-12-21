from typing import Any, Optional
from fastapi_mctools.cache.base import CacheStrategy


class CacheManager:
    """
    캐시 관리 클래스.
    다양한 캐싱 전략을 관리합니다.

    Attributes:
        strategy (CacheStrategy): 사용할 캐싱 전략.

    Methods:
        get: 키에 해당하는 캐시 값을 가져옵니다.
        set: 키와 값을 캐시에 설정합니다.
        delete: 키에 해당하는 캐시를 삭제합니다.
    """

    def __init__(self, strategy: CacheStrategy) -> None:
        self.strategy = strategy

    async def get(self, key: str) -> Any:
        """
        주어진 키에 해당하는 값을 캐시에서 가져옵니다.

        Args:
            key (str): 캐시에서 조회할 키.

        Returns:
            Any: 키에 해당하는 캐시 값.
        """
        return await self.strategy.get(key)

    async def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """
        주어진 키와 값을 캐시에 설정합니다.

        Args:
            key (str): 캐시에 저장할 키.
            value (Any): 캐시에 저장할 값.
            timeout (Optional[int]): 캐시의 만료 시간(초). 기본값은 None입니다.
        """
        await self.strategy.set(key, value, timeout)

    async def delete(self, key: str) -> None:
        """
        주어진 키에 해당하는 캐시를 삭제합니다.

        Args:
            key (str): 삭제할 캐시의 키.
        """
        await self.strategy.delete(key)
