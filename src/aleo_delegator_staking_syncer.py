import time
from aleo_api_client import AleoNetworkApiClient
from dto.block import Block


class AleoDelegatorStakingSyncerClient:
    def __init__(self, aleoClient: AleoNetworkApiClient, blockRangeSyncLimit=50, syncTimeout=0.5):
        self.aleoClient = aleoClient
        self.lastSyncedHeight = 0
        self.blockRangeSyncLimit = blockRangeSyncLimit
        self.syncTimeout = syncTimeout

    def getLastSyncedHeight(self):
        # get info from DB
        return self.lastSyncedHeight

    def getFunctionArgumentsFromOutputs(self, outputs):
        # example value ='{\n  program_id: credits.aleo,\n  function_name: bond_public,\n  arguments: [\n    aleo1nlwtlzch6c6qunqya5l2gf7d0t6msq34szspj763jgecuv2j7qxs7tva2s,\n    aleo1q6qstg8q8shwqf5m6q5fcenuwsdqsvp4hhsgfnx5chzjm3secyzqt9mxm8,\n    100000000u64\n  ]\n}'
        value = outputs[0]['value']
        arguments = value[value.find('[') + 1:value.find(']')]

        return [a.strip() for a in arguments.split(',')]

    def saveStakeTransaction(self, transaction, action):
        outputs = transaction['transaction']['execution']['transitions'][0]['outputs']
        arguments = self.getFunctionArgumentsFromOutputs(outputs)
        validator = arguments[1]
        delegator = arguments[0]
        amount = arguments[2].replace('u64', '')

        print(f'delegator {delegator} {action} {amount} to {validator}')

    def isStakeTransaction(self, transaction):
        # if not execute transaction than just skip
        if transaction['transaction']['type'] != 'execute':
            return False

        is_credits_aleo = transaction['transaction']['execution']['transitions'][0]['program'] == 'credits.aleo'
        function = transaction['transaction']['execution']['transitions'][0]['function']
        is_stake_transaction = function in ['bond_public', 'unbond_public', 'claim_unbond_public']

        return is_credits_aleo and is_stake_transaction

    def handleStakeTransaction(self, transaction):
        function = transaction['transaction']['execution']['transitions'][0]['function']

        if function == 'bond_public':
            self.saveStakeTransaction(transaction, 'stake')
        elif function == 'unbond_public':
            self.saveStakeTransaction(transaction, 'unstake')
        else:
            self.saveStakeTransaction(transaction, 'claim unstake')

    def handleBlock(self, block: Block):
        transactions = block['transactions']

        for transaction in transactions:
            if self.isStakeTransaction(transaction):
                self.handleStakeTransaction(transaction)

    def startSync(self):
        while True:
            start_height = self.getLastSyncedHeight()
            end_height = start_height + self.blockRangeSyncLimit

            print(f'Aleo network sync block from {start_height} to {end_height}')

            blocks = self.aleoClient.getBlockRange(start_height, end_height)

            for block in blocks:
                self.handleBlock(block)

            # increment height
            self.lastSyncedHeight = self.lastSyncedHeight + self.blockRangeSyncLimit
            time.sleep(self.syncTimeout)
