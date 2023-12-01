from aleo_api_client import AleoNetworkApiClient
from aleo_delegator_staking_syncer import AleoDelegatorStakingSyncerClient


def main():
    print('Start aleo network syncer')
    aleo_client = AleoNetworkApiClient('http://65.108.104.123:3033')
    syncer = AleoDelegatorStakingSyncerClient(aleo_client)

    syncer.startSync()

if __name__ == '__main__':
    main()
