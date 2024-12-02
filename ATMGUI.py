from graphics import *

class ATMGUI:
    def __init__(self, bank_system):
        self.bank_system = bank_system
        self.current_card = None
        self.window = None

    def start(self):
        self.show_account_entry()

    def show_account_entry(self):
        self.window = GraphWin("ATM - Enter Account Number", 400, 300)
        self.window.setBackground("lightblue")

        title = Text(Point(200, 50), "Enter Your Account Number")
        title.setSize(16)
        title.setStyle("bold")
        title.draw(self.window)

        account_entry_box = Entry(Point(200, 150), 15)
        account_entry_box.setFill("white")
        account_entry_box.draw(self.window)

        submit_button = Rectangle(Point(150, 200), Point(250, 230))
        submit_button.setFill("white")
        submit_button.draw(self.window)
        submit_label = Text(Point(200, 215), "Submit")
        submit_label.draw(self.window)

        while True:
            click = self.window.getMouse()
            if 150 <= click.getX() <= 250 and 200 <= click.getY() <= 230:
                account_number = account_entry_box.getText()
                if account_number in self.bank_system.accounts:
                    self.current_card = account_number
                    self.window.close()
                    self.show_pin_entry()
                    return
                else:
                    error_message = Text(Point(200, 250), "Account not found. Try again.")
                    error_message.setFill("red")
                    error_message.draw(self.window)

    def show_pin_entry(self):
        self.window = GraphWin("ATM - Enter PIN", 400, 300)
        self.window.setBackground("lightblue")

        title = Text(Point(200, 50), "Enter Your 4-Digit PIN")
        title.setSize(16)
        title.setStyle("bold")
        title.draw(self.window)

        pin_entry_box = Entry(Point(200, 150), 4)
        pin_entry_box.setFill("white")
        pin_entry_box.draw(self.window)

        submit_button = Rectangle(Point(150, 200), Point(250, 230))
        submit_button.setFill("white")
        submit_button.draw(self.window)
        submit_label = Text(Point(200, 215), "Submit")
        submit_label.draw(self.window)

        while True:
            click = self.window.getMouse()
            if 150 <= click.getX() <= 250 and 200 <= click.getY() <= 230:
                pin = pin_entry_box.getText()
                if self.bank_system.accounts[self.current_card]["pin"] == pin:
                    self.window.close()
                    self.show_transaction_menu()
                    return
                else:
                    error_message = Text(Point(200, 250), "Incorrect PIN. Try Again.")
                    error_message.setFill("red")
                    error_message.draw(self.window)

    def show_transaction_menu(self):
        self.window = GraphWin("ATM - Transaction Menu", 400, 300)
        self.window.setBackground("lightblue")

        title = Text(Point(200, 50), "Transaction Menu")
        title.setSize(16)
        title.setStyle("bold")
        title.draw(self.window)

        options = [("Withdraw", 100), ("Deposit", 150), ("Check Balance", 200), ("Quit", 250)]
        for label, y_pos in options:
            button = Rectangle(Point(150, y_pos), Point(250, y_pos + 30))
            button.setFill("white")
            button.draw(self.window)
            option_label = Text(Point(200, y_pos + 15), label)
            option_label.draw(self.window)

        while True:
            click = self.window.getMouse()
            for label, y_pos in options:
                if 150 <= click.getX() <= 250 and y_pos <= click.getY() <= y_pos + 30:
                    if label == "Withdraw":
                        self.window.close()
                        self.show_withdraw_deposit("Withdraw")
                        return
                    elif label == "Deposit":
                        self.window.close()
                        self.show_withdraw_deposit("Deposit")
                        return
                    elif label == "Check Balance":
                        self.show_balance()
                    elif label == "Quit":
                        self.window.close()
                        return

    def show_withdraw_deposit(self, operation):
        self.window = GraphWin(f"ATM - {operation}", 400, 300)
        self.window.setBackground("lightblue")

        title = Text(Point(200, 50), f"Enter Amount to {operation}")
        title.setSize(16)
        title.setStyle("bold")
        title.draw(self.window)

        amount_entry_box = Entry(Point(200, 150), 10)
        amount_entry_box.setFill("white")
        amount_entry_box.draw(self.window)

        submit_button = Rectangle(Point(150, 200), Point(250, 230))
        submit_button.setFill("white")
        submit_button.draw(self.window)
        submit_label = Text(Point(200, 215), "Submit")
        submit_label.draw(self.window)

        while True:
            click = self.window.getMouse()
            if 150 <= click.getX() <= 250 and 200 <= click.getY() <= 230:
                try:
                    amount = float(amount_entry_box.getText())
                    account = self.bank_system.accounts[self.current_card]
                    if operation == "Withdraw":
                        if amount > account["balance"]:
                            raise ValueError("Insufficient funds")
                        account["balance"] -= amount
                    elif operation == "Deposit":
                        account["balance"] += amount
                    self.bank_system.update_file()
                    self.window.close()
                    self.show_transaction_menu()
                    return
                except ValueError as e:
                    error_message = Text(Point(200, 250), str(e))
                    error_message.setFill("red")
                    error_message.draw(self.window)

    def show_balance(self):
        account = self.bank_system.accounts[self.current_card]
        balance_message = Text(Point(200, 75), f"Current Balance: {account['balance']:.2f}")
        balance_message.setFill("green")
        balance_message.draw(self.window)
