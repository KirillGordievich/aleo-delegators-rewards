import requests
from typing import List, Union
from dto.block import Block, TransactionModel


class AleoNetworkApiClient:
    def __init__(self, host: str):
        self.host = host + "/testnet3"

    def makeRequest(self, url: str = "/"):
        try:
            response = requests.get(self.host + url)
            response.raise_for_status()
            return response.json()
        except Exception as error:
            raise Exception("Error getting data")

    def getBlock(self, height: int) -> Union[Block, Exception]:
        try:
            block = self.makeRequest("/block/" + str(height))
            return block
        except Exception as error:
            raise Exception("Error getting block")

    def getBlockRange(self, start: int, end: int) -> Union[List[Block], Exception]:
        try:
            return self.makeRequest("/blocks?start=" + str(start) + "&end=" + str(end))
        except Exception as error:
            error_message = f"Error getting blocks between {start} and {end}"
            raise Exception(error_message)

    def getLatestBlock(self) -> Union[Block, Exception]:
        try:
            return self.makeRequest("/latest/block")
        except Exception as error:
            raise Exception("Error getting latest block")

    def getLatestHeight(self) -> Union[int, Exception]:
        try:
            return self.makeRequest("/latest/height")
        except Exception as error:
            raise Exception("Error getting latest height")

    def getProgramMappingValue(self, programId: str, mappingName: str, key: str) -> Union[str, Exception]:
        try:
            return self.makeRequest("/program/" + programId + "/mapping/" + mappingName + "/" + key)
        except Exception as error:
            raise Exception("Error getting mapping value - ensure the mapping exists and the key is correct")

    def getTransactions(self, height: int) -> Union[List[TransactionModel], Exception]:
        try:
            return self.makeRequest("/block/" + str(height) + "/transactions")
        except Exception as error:
            raise Exception("Error getting transactions")
