balance=500
mini_statement=[]

def credit():
    global balance
    amount=float(input("enter amount to credit:"))
    if amount<=0:
        print("enter a postive amount:")
    else:
        balance+=amount
        print(f"{amount:}/- credited to your account")

def debit():
    global balance
    amount=float(input("enter amount to debit:"))
    if amount<=0:
        print("enter a postive amount:")
    elif amount>balance:
        print("Insufficient balance")
    else:
        balance-=amount
        print(f"{amount} debited from your account")

def check_balance():
    print(f"your balance is {balance}/-")

while True:
    print("welcome to canara bank")
    print("ATM MENU")
    print("1.Credit")
    print("2.Debit")
    print("3.Balance")
    print("4.Exit")

    choice=input("enter your choice(1-4): ")

    if choice=="1":
        credit()
    elif choice=="2":
        debit()
    elif choice=="3":
        check_balance()
    elif choice=="4":
        print("THANKYOU")
        break
    else:
        print("Invalid choice. Try again")

        