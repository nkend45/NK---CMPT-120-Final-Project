from ATMGUI import *

class BankSystem:
    def __init__(self, data_file):
        self.data_file = data_file
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = {}
        file = open(self.data_file, "r")
        lines = file.readlines()
        file.close()
        for line in lines:
            card_type, card_number, pin, balance = line.strip().split(",")
            accounts[card_number] = {
                "type": card_type,
                "pin": pin,
                "balance": float(balance),
            }
        return accounts

    def update_file(self):
        file = open(self.data_file, "w")
        for card_number, details in self.accounts.items():
            file.write(f"{details['type']},{card_number},{details['pin']},{details['balance']}\n")
        file.close()

if __name__ == "__main__":
    data_file = "bank.txt"
    bank_system = BankSystem(data_file)
    atm_gui = ATMGUI(bank_system)
    atm_gui.start()
