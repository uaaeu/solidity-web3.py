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
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xCeb65ce05Dd48b3ddDEd0Af9d16E3E26DF7d0fA2"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)

# Create the Contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the Latest Transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a Transaction
# 2. Sign a Transaction
# 3. Send a Transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
