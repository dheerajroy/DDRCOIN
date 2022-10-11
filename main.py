from typing import List,Dict
from fastapi import FastAPI
from DDRCoin import DDRCoin
from uuid import uuid4

app = FastAPI()
ddrcoin = DDRCoin()

@app.post('/set_name')
def set_name(name):
    return ddrcoin.set_name(name)

@app.post('/add_transaction')
def add_transaction(sender, receiver, amount:float):
    return ddrcoin.add_transaction(sender=sender, receiver=receiver, amount=amount)

@app.post('/mine')
def mine():
    previous_block = ddrcoin.get_previous_block()
    add_transaction(sender=str(uuid4()).replace('-', ''), receiver=ddrcoin.name, amount=1)
    return ddrcoin.create_block(proof=ddrcoin.proof_of_work(previous_block['proof']), previous_hash=ddrcoin.hash(previous_block))

@app.get('/chain')
def chain():
    return ddrcoin.chain

@app.get('/is_chain_valid')
def is_chain_valid():
    return ddrcoin.is_chain_valid()

@app.post('/connect_node')
def connect_node(address):
    return ddrcoin.add_node(address=address)

@app.post('/nodes')
def nodes():
    return ddrcoin.nodes

@app.post('/replace_chain')
def replace_chain():
    return ddrcoin.replace_chain()
