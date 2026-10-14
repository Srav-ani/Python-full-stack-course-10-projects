
class Account:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance
        self.ministatement_list = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Amount credited: {amount}")
            print(f"Total balance: {self.balance}")
            self.ministatement_list.append(f"Deposited: {amount}")
        else:
            print("Enter a valid amount....")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                print(f"Amount withdrawn: {amount}")
                print(f"Balance: {self.balance}")
                self.ministatement_list.append(f"Withdrawn: {amount}")
            else:
                print("Insufficient balance....")
        else:
            print("Enter a valid amount....")

    def get_balance(self):
        return self.balance

    def get_ministatement(self):
        print("\nMinistatement:")
        print(f"Username: {self.username}")
        print(f"Current balance: {self.balance}")

        if len(self.ministatement_list) == 0:
            print("No transactions yet.")
        else:
            for transaction in self.ministatement_list:
                print(transaction)


class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, username, password):
        if username in self.accounts:
            print("Username already exists....")
        else:
            self.accounts[username] = Account(username, password)
            print("Account created successfully....")

    def login(self, username, password):
        if username in self.accounts:
            account = self.accounts[username]

            if account.password == password:
                print("Login success")
                return account
            else:
                print("Invalid password")
        else:
            print("Invalid username")

        return None


bank = BankingSystem()

while True:
    print("\n")
    print("1. Create account")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")

        bank.create_account(username, password)

    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")

        account = bank.login(username, password)

        if account is not None:

            while True:
                print("\n----- Welcome to PYTHON Bank -----")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check balance")
                print("4. Ministatement")
                print("5. Logout")

                choice = input("Enter choice (1-5): ")

                if choice == "1":
                    amount = int(input("Enter amount: "))
                    account.deposit(amount)

                elif choice == "2":
                    amount = int(input("Enter amount: "))
                    account.withdraw(amount)

                elif choice == "3":
                    print(f"Current balance: {account.get_balance()}")

                elif choice == "4":
                    account.get_ministatement()

                elif choice == "5":
                    print("------ THANK YOU, VISIT AGAIN ------")
                    break

                else:
                    print("Invalid choice...")

    elif choice == "3":
        print("---- THANK YOU ----")
        break

    else:
        print("Invalid choice...")




