from fastapi.middleware.trustedhost import (
    TrustedHostMiddleware as BaseTrustedHostMiddleware,
)
from starlette.datastructures import Headers
from starlette.types import Receive, Scope, Send


class TrustedHostMiddleware(BaseTrustedHostMiddleware):
    """
    Middleware for load balancer health checks.
    A temporary measure for passing the health check of a target group when using AWS's ALB.
    Adds the VPC IP to the allowed_hosts.

    : allowed_hosts, list[str]
    : first_two_vpc_ip, str, example: "10.0"
    ----------------------------
    """

    def __init__(self, app, allowed_hosts: list[str], first_two_vpc_ip: str = "10.0"):
        self.first_two_vpc_ip = first_two_vpc_ip
        super().__init__(app, allowed_hosts=allowed_hosts)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        try:
            headers = Headers(scope=scope)
            host = headers.get("host", "").split(":")[0]
            if host.startswith(self.first_two_vpc_ip):
                self.allowed_hosts.append(host)
        except Exception as e:
            print("Error!", e)
        return await super().__call__(scope, receive, send)
