import hashlib
import json

from time import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database.models import Block, Transaction


class Blockchain:
    def __init__(self, database: AsyncSession):
        self.database = database
        self.current_transactions = []

    async def load_chain(self):
        result = await self.database.execute(select(Block).order_by(Block.id))
        blocks = result.scalars().all()
        chain = []

        for block in blocks:
            chain.append({
                "index": block.id,
                "block_hash": block.hash,
                "previous_hash": block.parent_hash,
                "proof": block.proof,
                "timestamp": block.timestamp,
                "merkle_root": block.merkle_root,
                "transactions": [
                    {
                        "tx_hash": tx.hash,
                        "sender": tx.sender,
                        "recipient": tx.recipient,
                        "amount": tx.amount,
                        "timestamp": tx.timestamp
                    } for tx in block.transactions
                ]
            })
        return chain

    async def new_block(self, proof: int, previous_hash: str = None):
        chain = await self.load_chain()
        last_block = chain[-1] if chain else None

        block = {
            "index": len(chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(last_block),
            "merkle_root": self.compute_merkle_root(self.current_transactions)
        }

        self.current_transactions = []

        block_model = Block(
            block_hash=self.hash(block),
            previous_hash=block["previous_hash"],
            proof=block["proof"],
            timestamp=block["timestamp"],
            merkle_root=block["merkle_root"]
        )

        self.database.add(block_model)
        await self.database.commit()

        for tx in block["transactions"]:
            tx_model = Transaction(
                block_id=block_model.id,
                tx_hash=tx["tx_hash"],
                sender=tx["sender"],
                recipient=tx["recipient"],
                amount=tx["amount"]
            )

            self.database.add(tx_model)

        await self.database.commit()

        return block

    async def new_transaction(self, sender: str, recipient: str, amount: float):
        if not sender == "0":
            balance = await self.get_balance(sender)
            if balance < amount:
                raise ValueError("Not enough coins")

        tx = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "tx_hash": self.compute_transaction_hash(sender, recipient, amount)
        }

        self.current_transactions.append(tx)

        chain = await self.load_chain()

        return chain[-1]["index"] + 1 if chain else 1

    async def get_balance(self, address: str):
        chain = await self.load_chain()

        balance = 0
        for block in chain:
            for tx in block["transactions"]:
                if tx["sender"] == address:
                    balance -= tx["amount"]
                if tx["recipient"] == address:
                    balance += tx["amount"]

        return balance

    @property
    async def last_block(self):
        chain = await self.load_chain()
        return chain[-1] if chain else None

    async def proof_of_work(self, last_proof: int):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:3] == "000"

    @staticmethod
    def hash(block: dict):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def compute_transaction_hash(sender: str, recipient: str, amount: float):
        tx_string = f"{sender}{recipient}{amount}".encode()
        return hashlib.sha256(tx_string).hexdigest()

    @staticmethod
    def compute_merkle_root(transactions):
        if not transactions:
            return ""
        tx_hashes = [tx["tx_hash"] for tx in transactions]
        while len(tx_hashes) > 1:
            if not len(tx_hashes) % 2 == 0:
                tx_hashes.append(tx_hashes[-1])

            new_level = []
            for i in range(0, len(tx_hashes), 2):
                new_level.append(hashlib.sha256((tx_hashes[i] + tx_hashes[i+1]).encode()).hexdigest())

            tx_hashes = new_level

        return tx_hashes[0]
