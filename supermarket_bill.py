name = input("Enter your Name:")

lists = ''' 
WELCOME! here is the list of items pls check
Rice Rs 60/kg 
Sugar Rs 20/kg 
Oil Rs 30/liter 
Mushroom Rs 50/kg 
Paneer Rs 40/kg
Maggie Rs 15/pack
Boost Rs 100/bottle '''

price = 0
pricelist = []
totalprice = 0
Finalprice = 0
ilist = []
qlist = []
plist = []


items = {'rice': 60, 'sugar': 20, 'oil': 30, 'mushroom': 50, 'paneer': 40, 'maggie': 15, 'boost': 100}

while True:
    option = input("Press 1 for list or 2 to exit: ")
    if option == '2':
        print("Thank you for shopping")
        break
    elif option == '1':
        print(lists)

        while True:
            inp1 = input("To buy press 1 or press 2 to exit: ")
            if inp1 == '2':
                print("Thank you for shopping")
                break
            elif inp1 == '1':
                item = input("Choose your items: ").lower()
                while True:
                    quantity_input = input("Enter quantity: ")
                    if quantity_input.isdigit():  
                        quantity = int(quantity_input)
                        break
                    else:
                        print("Please enter a valid quantity.")

                if item in items:
                    price = quantity * items[item]
                    pricelist.append((item, quantity, items[item], price))
                    totalprice += price
                    ilist.append(item)
                    qlist.append(quantity)
                    plist.append(price)
                else:
                    print("Selected item is not available. Sorry for the inconvenience.")

        if totalprice > 0:
            tax = (totalprice * 10) / 100
            finalamount = tax + totalprice

            print(25 * "=", "Pythonlife Supermarket", 25 * "=")
            print(28 * " ", "Hyderabad")
            print("Name:", name, 30 * " ","August 25 2026")
            print(75 * "-")
            print("sno", 10 * " ", 'items', 8 * " ", 'quantity', 8 * " ", 'price')
            for i in range(len(pricelist)):
                print(i, 13 * " ", ilist[i], 8 * " ", qlist[i], 8 * " ", plist[i])
            print(75 * "-")
            print(50 * " ", 'Total amount:', 'Rs', totalprice)
            print("Tax amount", 50 * " ", 'Rs', tax)
            print(75 * "-")
            print(50 * " ", 'Final amount:', 'Rs', finalamount)
            print(75 * "-")
            print(20 * " ", "Thank you & Visit again")
            print(75 * "-")