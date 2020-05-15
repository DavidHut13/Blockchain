from functools import reduce
import json
from utility.hash_util import hash_block
from utility.verifivation import Verification
import pickle
from block import Block
from transaction import Transaction
from wallet import Wallet

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
MINING_REWARD = 10
blockchain = [genesis_block]
participants = {'David'}


class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0,'',[],100, 0)
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id
    
    def get_chain(self):
        return self.__chain[:]
    
    def get_open_transactions(self):
        return self.__open_transactions[:]

    def save_data(self):
        try:
            with open('blockchain.txt',mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index,block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions],block_el.proof,block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx =  [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                # for using pickle
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(blockchain))
        except IOError:
            print('Saving Failed')

    def load_data(self):
        try:
            with open('blockchain.txt',mode='r') as f:
                file_content = f.readlines()
                # for using pickle
                # file_content = pickle.loads(f.read())
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                print(file_content)
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'],tx['receipient'],tx['signature'],tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'],converted_tx,block['proof'],block['timestamp'])
                    updated_block = {
                        'previous_hash': block['previous_hash'],
                        'index': block['index'],
                        'proof': block['proof'],
                        'transactions': [OrderedDict({[('sender',tx['sender']),('recipient',tx['recipient']), ('amount',tx['amount'])]})for tx in block['transactions']]
                    }
                    updated_blockchain.append(updated_block)
                    self.__chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transactions = Transaction(tx['sender'],tx['receipient'],tx['signature'],tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError,IndexError):
            print('Handled Exception.......')
        except ValueError:
            print("Value error")
        except:
            print('Wildcard')
        finally:
            print('Cleanup')

    def add_transaction(self,recipient,sender,signature,amount=1.0):
        if self.hosting_node == None:
            return False
        transaction = Transaction(sender,recipient,signature,amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block) 
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash,proof):
            proof += 1
        return proof


    def get_balance(self,participant):
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        amount_sent = 0
        #this is the old way of getting the amount_sent
        #for tx in tx_sender:
        #   if len(tx) > 0:
        #      amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        #this is the old way of getting the amount_received
        #for tx in tx_recipient:
        #   if len(tx) > 0:
        #       amount_sent += tx[0]
        return amount_received - amount_sent

    def mine_block(self):
        if self.hosting_node == None:
            return False
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient':owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction('MINING',self.hosting_node,'',MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return False
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain),hashed_block,copied_transactions,proof)
        self.__chain.append(block)
        self.save_data()
        self.__open_transactions = []
        self.save_data()
        return True





