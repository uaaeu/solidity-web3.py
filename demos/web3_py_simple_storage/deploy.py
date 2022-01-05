from solcx import compile_standard
from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Our Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    }
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get Bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get Abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# For Connecting to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

# Create the Contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the Latest Transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a Transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# 2. Sign a Transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying contract...")
# 3. Send a Transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Deployed!")

# Working with the Contract
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and return value
# Transact -> Actually make a state change

# Initial value of favotire number
print(simple_storage.functions.retrieve().call())
print("Updating contract...")

store_transaction = simple_storage.functions.store(8).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
store_signed_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
store_tx_hash = w3.eth.send_raw_transaction(store_signed_txn.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print("Updated!")

print(simple_storage.functions.retrieve().call())
