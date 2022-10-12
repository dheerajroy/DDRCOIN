import requests
import hashlib
import json
from datetime import datetime
from urllib.parse import urlparse
from uuid import uuid4

class DDRCoin:
    def __init__(self):
        self.name = None
        self.uuid = str(uuid4()).replace('-', '')
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.validated = False
        self.create_block(1, '0')

    def set_name(self, name):
        self.name = name
        return True

    def add_node(self, address):
        try:
            self.nodes.add(urlparse(address).netloc)
            return True
        except Exception:
            return False

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain)+1,
            'timestamp': str(datetime.now()),
            'proof': proof,
            'transaction': self.transactions,
            'previous_hash': previous_hash
        }
        self.transactions = []
        self.chain.append(block)
        self.validated = False
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        proof = 1
        check_proof = False
        while not check_proof:
            hash_code = hashlib.sha256(str(previous_proof**2 - proof**2).encode()).hexdigest()
            if hash_code[:4] == '0000':
                check_proof = True
            else:
                proof += 1
        return proof

    def replace_chain(self):
        chain_length = len(self.chain)
        chain = None
        for node in self.nodes:
            try:
                content = requests.get(f'http://{node}/chain')
                if content.status_code == 200:
                    temp_chain = content.json()
                    temp_chain_length = len(temp_chain)
                    if temp_chain_length > chain_length:
                        chain = self.chain = temp_chain
                        self.validated = False
            except Exception:
                continue
        return bool(chain)

    def add_transaction(self, sender, receiver, amount):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        self.transactions.append(transaction)
        return transaction

    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def is_chain_valid(self):
        self.validated = True
        previous_block = self.chain[0]
        for block in self.chain[1:]:
            if (block['previous_hash'] != self.hash(previous_block)) or (block['proof'] != self.proof_of_work(previous_block['proof'])):
                return False
            previous_block = block
        return True
    
    def is_validated(self):
        return self.validated

    def is_first_validator(self):
        validation_of_nodes = []
        for node in self.nodes:
            try:
                validation_of_nodes.append(requests.get(f'http://{node}/is_validated').json())
            except Exception:
                continue
        if self.validated and not all(validation_of_nodes):
            return True
        return False
