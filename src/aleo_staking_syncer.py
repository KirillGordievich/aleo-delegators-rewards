import time
from aleo_api_client import AleoNetworkApiClient
from dto.block import Block


class AleoStakingSyncerClient:
    def __init__(self, aleoClient: AleoNetworkApiClient, dbClient, blockRangeSyncLimit=50, iterationTimeout=0):
        self.aleo_client = aleoClient
        self.db_client = dbClient
        self.last_synced_height = None
        self.block_range_sync_limit = blockRangeSyncLimit
        self.iteration_timeout = iterationTimeout

    def get_last_synced_height(self):
        if self.last_synced_height is None:
            # get info from DB when init
            self.last_synced_height = self.db_client.get_last_synced_height()

            print(f'Aleo network last synced block is {self.last_synced_height}')

        return self.last_synced_height or 0

    def get_arguments_from_outputs(self, outputs):
        # example value ='{\n  program_id: credits.aleo,\n  function_name: bond_public,\n  arguments: [\n    aleo1nlwtlzch6c6qunqya5l2gf7d0t6msq34szspj763jgecuv2j7qxs7tva2s,\n    aleo1q6qstg8q8shwqf5m6q5fcenuwsdqsvp4hhsgfnx5chzjm3secyzqt9mxm8,\n    100000000u64\n  ]\n}'
        value = outputs[0]['value']
        arguments = value[value.find('[') + 1:value.find(']')]

        return [a.strip() for a in arguments.split(',')]

    def log_stake_transaction(self, transaction, height):
        outputs = transaction['transaction']['execution']['transitions'][0]['outputs']
        function = transaction['transaction']['execution']['transitions'][0]['function']
        arguments = self.get_arguments_from_outputs(outputs)

        if function == 'bond_public':
            validator = arguments[1]
            delegator = arguments[0]
            amount = arguments[2].replace('u64', '')
            print(f'delegator {delegator} stake {amount} to {validator} (block {height})')

        elif function == 'unbond_public':
            delegator = arguments[0]
            amount = arguments[1].replace('u64', '')
            print(f'delegator {delegator} unstake {amount} from validator (block {height})')
        else:
            delegator = arguments[0]
            amount = arguments[1].replace('u64', '')
            print(f'delegator {delegator} claim unstake {amount} from validator (block {height})')

    def save_stake_transaction(self, transaction, height, round):
        transaction_db_format = {
            'tx_id': transaction['transaction']['id'],
            'height': height,
            'round': round,
            'payload': transaction
        }

        self.db_client.save_stake_transaction(transaction_db_format)

    def is_stake_transaction(self, transaction):
        # if not execute transaction than just skip
        if transaction['transaction']['type'] != 'execute':
            return False

        is_credits_aleo = transaction['transaction']['execution']['transitions'][0]['program'] == 'credits.aleo'

        if not is_credits_aleo:
            return False

        function = transaction['transaction']['execution']['transitions'][0]['function']

        return function in ['bond_public', 'unbond_public', 'claim_unbond_public']

    def handle_stake_transaction(self, transaction, block_height, block_round):
        self.save_stake_transaction(transaction, block_height, block_round)
        self.log_stake_transaction(transaction, block_height)

    def handle_block(self, block: Block):
        transactions = block['transactions']
        metadata = block['header']['metadata']
        [block_height, block_round] = metadata['height'], metadata['round']

        for transaction in transactions:
            if self.is_stake_transaction(transaction):
                self.handle_stake_transaction(transaction, block_height, block_round)

    def start_sync(self):
        while True:
            start_height = self.get_last_synced_height()
            end_height = start_height + self.block_range_sync_limit

            print(f'Aleo network sync block from {start_height} to {end_height}')

            blocks = self.aleo_client.getBlockRange(start_height, end_height)

            for block in blocks:
                self.handle_block(block)

            # increment height
            self.last_synced_height = self.last_synced_height + self.block_range_sync_limit
            self.db_client.update_height(self.last_synced_height)
            time.sleep(self.iteration_timeout)
