from app.core.config import PROJECT_NAME, VERSION
from app.services.bybit.client import BybitClient


def main():
    print(PROJECT_NAME)
    print(VERSION)

    client = BybitClient()

    print(client.get_status())

    server_time = client.get_server_time()
    print(server_time)
