from .default_db_client import DefaultDbClient
import json


class AleoRewardsDbClient(DefaultDbClient):
    def __init__(self, dbname, user, password, host, port):
        super().__init__(dbname, user, password, host, port)

    def save_stake_transaction(self, transaction_data):
        query_insert = """
            INSERT INTO aleo_rewards.stake_transaction (validator, delegator, function, height, round, amount, payload) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            ON CONFLICT (validator, delegator, function, height)
            DO UPDATE SET amount = EXCLUDED.amount, updated_at = now()
        """
        values_insert = (
            transaction_data['validator'],
            transaction_data['delegator'],
            transaction_data['function'],
            transaction_data['height'],
            transaction_data['round'],
            transaction_data['amount'],
            json.dumps(transaction_data['payload'])
        )

        self.execute_query(query_insert, values_insert)
        self.commit_transaction()

    def update_height(self, height):
        query_insert = """
            INSERT INTO aleo_rewards.block_height (height) 
            VALUES (%s)
        """
        values_insert = (height,)

        self.execute_query(query_insert, values_insert)
        self.commit_transaction()

    def get_last_synced_height(self):
        query_insert = """
            SELECT * FROM aleo_rewards.block_height ORDER BY height DESC LIMIT 1;
        """

        result = self.execute_query(query_insert)
        self.commit_transaction()

        if len(result) == 0:
            result = 0
        else:
            result = result[0]['height']

        return result
