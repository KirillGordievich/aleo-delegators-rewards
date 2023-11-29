from aleo_api_client import AleoNetworkApiClient


def main():
    aleo = AleoNetworkApiClient('http://65.108.104.123:3033')

    print(aleo.getLatestBlock())


if __name__ == '__main__':
    main()
