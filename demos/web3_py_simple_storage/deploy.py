from solcx import compile_standard
import json
from web3 import Web3

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
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 5777
my_address = "0xc14fc1ECa33B18FEBF994B7847CdD615415BEB40"
private_key = "0x635962a9c407f7efde903f7699f236d0fc9ed194ad80100a91181e14ce40c2e9"

# Create the Contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the Latest Transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a Transaction
# 2. Sign a Transaction
# 3. Send a Transaction
