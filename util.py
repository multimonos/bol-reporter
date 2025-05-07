from datetime import datetime, timezone
import socket
import ssl


def ssl_valid_days(hostname: str, port: int = 443) -> int:
    """get the number of days a certificate is valid for"""
    ctx = ssl.create_default_context()

    with socket.create_connection((hostname, port), timeout=10) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()

            if cert is None:
                return 0

            not_after_str = cert["notAfter"]

            expires = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(
                tzinfo=timezone.utc
            )
            now = datetime.now(timezone.utc)

            days_remaining = (expires - now).days

            print(f"certificate valid for {days_remaining} days")
            return days_remaining
