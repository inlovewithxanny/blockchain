from faker import Faker
from random import randint
from src.blockchain import storage, Block, Transaction
from time import sleep

faker = Faker()


def main():
    while True:
        sleep(2)
        transactions = []
        for _ in range(randint(1, 14)):
            transactions.append(
                Transaction(
                    sender_name=faker.name(),
                    reciever_name=faker.name(),
                    amount=randint(1, 100000000),
                )
            )

        if len(storage) == 0:
            block = Block(transactions=transactions)
        else:
            block = Block(
                transactions=transactions, previous_block_hash=storage[-1]["hash"]
            )

        storage.append(block.as_dict)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("STORAGE:\n", storage, "\n")
        input("Press enter to exit")
