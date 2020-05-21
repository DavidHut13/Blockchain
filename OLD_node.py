from blockchain import Blockchain
from uuid import uuid4
from utility.verifivation import Verification
from wallet import Wallet
class Node:
    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.blockchain = None
        self.blockchain = Blockchain(self.wallet.public_key)
        

    def get_transaction_value(self):
        tx_recipient = input('Enter the recipient of the transaction:')
        tx_amount = float(input('Your transaction amount please: '))
        return (tx_recipient,tx_amount)

    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain. """
        # Output the blockchain list to the console
        for block in self.blockchain.get_chain():
            print('Outputting Block')
            print(block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('Please Choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check transaction validity')
            print('5: Create Wallet')
            print('6: Load Wallet')
            print('7: Save Keys')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key,recipient,amount)
                if self.blockchain.add_transaction(recipient,self.wallet.public_key,signature,amount=amount):
                    print("Added transaction")
                else:
                    print('Transaction Failed')
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
               if not self.blockchain.mine_block():
                   print('Mining failed. You might be missing a wallet.')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.__open_transactions,self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                waiting_for_input = False
            
            else:
                print('Input was invalid, please pick a value from the list!')
            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blockchain_elements()
                print('Inavalid blockchain!')
                break
            print('Balance of {}: {:6.2f}'.format('David',self.blockchain.get_balance('David')))
        else:
            print('User left!')
    
    def get_user_choice(self):
        user_input = input('Your Choice:')
        return user_input


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()