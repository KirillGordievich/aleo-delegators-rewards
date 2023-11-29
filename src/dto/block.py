from typing import List, Optional


class Input:
    def __init__(self, type: str, id: str, value: str):
        self.type = type
        self.id = id
        self.value = value


class Output:
    def __init__(self, type: str, id: str, value: str):
        self.type = type
        self.id = id
        self.value = value


class Transition:
    def __init__(self, id: str, program: str, function: str,
                 inputs: Optional[List[Input]] = None,
                 outputs: Optional[List[Output]] = None,
                 proof: str = '', tpk: str = '', tcm: str = '', fee: int = 0):
        self.id = id
        self.program = program
        self.function = function
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.proof = proof
        self.tpk = tpk
        self.tcm = tcm
        self.fee = fee


class Execution:
    def __init__(self, edition: int, transitions: Optional[List[Transition]] = None):
        self.edition = edition
        self.transitions = transitions or []


class TransactionModel:
    def __init__(self, type: str, id: str, execution: Execution):
        self.type = type
        self.id = id
        self.execution = execution


class ConfirmedTransaction:
    def __init__(self, type: str, id: str, transaction: TransactionModel):
        self.type = type
        self.id = id
        self.transaction = transaction


class Metadata:
    def __init__(self, network: int, round: int, height: int, coinbase_target: int,
                 proof_target: int, timestamp: int):
        self.network = network
        self.round = round
        self.height = height
        self.coinbase_target = coinbase_target
        self.proof_target = proof_target
        self.timestamp = timestamp


class Header:
    def __init__(self, previous_state_root: str, transactions_root: str, metadata: Metadata):
        self.previous_state_root = previous_state_root
        self.transactions_root = transactions_root
        self.metadata = metadata


class Block:
    def __init__(self, block_hash: str, previous_hash: str, header: Header, signature: str,
                 transactions: Optional[List[ConfirmedTransaction]] = None):
        self.block_hash = block_hash
        self.previous_hash = previous_hash
        self.header = header
        self.transactions = transactions or []
        self.signature = signature
