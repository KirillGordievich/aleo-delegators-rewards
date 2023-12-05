from .default_db_client import DefaultDbClient
import json

sql_queries = {
    'save_stake_transaction': """
            INSERT INTO aleo_rewards.stake_transaction (tx_id, height, round, payload) 
            VALUES (%s, %s, %s, %s) 
            ON CONFLICT (tx_id)
            DO NOTHING
        """,
    'update_height': """
            INSERT INTO aleo_rewards.block_height (height) 
            VALUES (%s)
            ON CONFLICT (height)
            DO NOTHING
        """,
    'get_last_synced_height': """
            SELECT * FROM aleo_rewards.block_height ORDER BY height DESC LIMIT 1;
        """
}


class AleoRewardsDbClient(DefaultDbClient):
    def __init__(self, dbname, user, password, host, port):
        super().__init__(dbname, user, password, host, port)

    def save_stake_transaction(self, transaction_data):
        query_insert = sql_queries['save_stake_transaction']

        values_insert = (
            transaction_data['tx_id'],
            transaction_data['height'],
            transaction_data['round'],
            json.dumps(transaction_data['payload'])
        )

        self.execute_query(query_insert, values_insert)
        self.commit_transaction()

    def update_height(self, height):
        query_insert = sql_queries['update_height']
        values_insert = (height,)

        self.execute_query(query_insert, values_insert)
        self.commit_transaction()

    def get_last_synced_height(self):
        query_insert = sql_queries['get_last_synced_height']

        result = self.execute_query(query_insert)
        self.commit_transaction()

        if len(result) == 0:
            result = 0
        else:
            result = result[0]['height']

        return result
