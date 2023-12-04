from aleo_api_client import AleoNetworkApiClient
from aleo_staking_syncer import AleoStakingSyncerClient
from db import AleoRewardsDbClient
from configs import db_config

def main():
    print('Start aleo network syncer')

    db_client = AleoRewardsDbClient(**db_config)
    db_client.connect()
    api_client = AleoNetworkApiClient('http://65.108.104.123:3033')
    syncer_client = AleoStakingSyncerClient(api_client, db_client)

    syncer_client.start_sync()

if __name__ == '__main__':
    main()
