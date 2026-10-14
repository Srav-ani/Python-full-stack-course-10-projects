import random
import datetime

class Train:
    def __init__(self, t_num, name, src, dest, distance):
        self.t_num = t_num
        self.name = name
        self.src = src.upper()
        self.dest = dest.upper()
        self.distance = distance
        
        # Simulating limited seats to demonstrate RAC and WL shifting easily
        self.classes = {
            "1AC": {"fare_multiplier": 5.0, "total_cnf": 2, "total_rac": 0, "total_wl": 1},
            "2AC": {"fare_multiplier": 3.0, "total_cnf": 2, "total_rac": 1, "total_wl": 2},
            "3AC": {"fare_multiplier": 2.0, "total_cnf": 3, "total_rac": 2, "total_wl": 2},
            "SL":  {"fare_multiplier": 1.0, "total_cnf": 5, "total_rac": 2, "total_wl": 3},
        }
        
        # Queues to hold passenger IDs (PNR_PassengerIndex)
        self.queues = {
            cls: {"CNF": [], "RAC": [], "WL": []} for cls in self.classes
        }

    def get_fare(self, coach_class):
        base_fare_per_km = 1.25
        return round(self.distance * base_fare_per_km * self.classes[coach_class]["fare_multiplier"], 2)


class RailwaySystem:
    def __init__(self):
        self.trains = {}
        self.pnr_db = {}
        self._initialize_trains()

    def _initialize_trains(self):
        self.trains["12951"] = Train("12951", "Rajdhani Express", "MUMBAI", "DELHI", 1384)
        self.trains["12759"] = Train("12759", "Charminar Express", "CHENNAI", "HYDERABAD", 790)
        self.trains["22435"] = Train("22435", "Vande Bharat", "DELHI", "VARANASI", 762)

    def search_trains(self, src, dest):
        print(f"\n--- Trains from {src.upper()} to {dest.upper()} ---")
        found = False
        for t_num, train in self.trains.items():
            if train.src == src.upper() and train.dest == dest.upper():
                found = True
                print(f"[{t_num}] {train.name} | Distance: {train.distance} km")
                print("Availability & Fares:")
                for cls, config in train.classes.items():
                    cnf_avail = config['total_cnf'] - len(train.queues[cls]['CNF'])
                    rac_avail = config['total_rac'] - len(train.queues[cls]['RAC'])
                    wl_avail = config['total_wl'] - len(train.queues[cls]['WL'])
                    
                    status = f"AVAILABLE ({cnf_avail})" if cnf_avail > 0 else \
                             f"RAC ({rac_avail})" if rac_avail > 0 else \
                             f"WL ({wl_avail})" if wl_avail > 0 else "REGRET"
                    print(f"  - {cls}: {status} | Fare: Rs. {train.get_fare(cls):.2f}")
        if not found:
            print("No direct trains found for this route.")

    def book_ticket(self):
        print("\n--- Book Ticket ---")
        t_num = input("Enter Train Number: ").strip()
        if t_num not in self.trains:
            print("Error: Invalid Train Number.")
            return

        train = self.trains[t_num]
        coach_class = input("Enter Class (1AC/2AC/3AC/SL): ").strip().upper()
        if coach_class not in train.classes:
            print("Error: Invalid Class.")
            return

        try:
            num_passengers = int(input("Enter number of passengers (Max 4): "))
            if not (1 <= num_passengers <= 4):
                print("Error: You can only book 1 to 4 passengers at a time.")
                return
        except ValueError:
            print("Error: Invalid number.")
            return

        # Check total availability (CNF + RAC + WL)
        config = train.classes[coach_class]
        queues = train.queues[coach_class]
        total_capacity = config['total_cnf'] + config['total_rac'] + config['total_wl']
        current_booked = len(queues['CNF']) + len(queues['RAC']) + len(queues['WL'])
        
        if total_capacity - current_booked < num_passengers:
            print("Error: Not enough seats/waitlist slots available. Booking rejected (REGRET).")
            return

        passengers = []
        for i in range(num_passengers):
            print(f"\nPassenger {i+1} Details:")
            name = input("  Name: ").strip()
            age = input("  Age: ").strip()
            gender = input("  Gender (M/F/O): ").strip().upper()
            passengers.append({"name": name, "age": age, "gender": gender, "status": "", "seat": ""})

        # Generate PNR
        pnr = str(random.randint(1000000000, 9999999999))
        
        # Allocate seats/status
        for idx, p in enumerate(passengers):
            p_id = f"{pnr}_{idx}"
            if len(queues['CNF']) < config['total_cnf']:
                queues['CNF'].append(p_id)
                p['status'] = "CNF"
                p['seat'] = f"{coach_class}-{len(queues['CNF'])}"
            elif len(queues['RAC']) < config['total_rac']:
                queues['RAC'].append(p_id)
                p['status'] = f"RAC{len(queues['RAC'])}"
                p['seat'] = "Side Lower (Shared)"
            else:
                queues['WL'].append(p_id)
                p['status'] = f"WL{len(queues['WL'])}"
                p['seat'] = "Pending"

        total_fare = train.get_fare(coach_class) * num_passengers
        
        self.pnr_db[pnr] = {
            "train_num": t_num,
            "class": coach_class,
            "doj": (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "passengers": passengers,
            "total_fare": total_fare
        }

        print("\nBooking Successful!")
        print(f"Your PNR Number is: {pnr}")
        print(f"Total Fare: Rs. {total_fare:.2f}")

    def pnr_status(self):
        pnr = input("\nEnter 10-digit PNR: ").strip()
        if pnr not in self.pnr_db:
            print("Error: Invalid PNR Number.")
            return

        ticket = self.pnr_db[pnr]
        train = self.trains[ticket['train_num']]
        
        print("\n" + "="*50)
        print(f"PNR STATUS: {pnr}")
        print(f"Train: {train.t_num} - {train.name}")
        print(f"Route: {train.src} to {train.dest} | Date: {ticket['doj']}")
        print(f"Class: {ticket['class']} | Total Fare: Rs. {ticket['total_fare']:.2f}")
        print("-"*50)
        print(f"{'Name':<15} | {'Age':<3} | {'Sex':<3} | {'Status':<8} | {'Seat'}")
        print("-"*50)
        for p in ticket['passengers']:
            # For cancelled passengers, status check
            print(f"{p['name']:<15} | {p['age']:<3} | {p['gender']:<3} | {p['status']:<8} | {p['seat']}")
        print("="*50)

    def cancel_ticket(self):
        pnr = input("\nEnter PNR to cancel: ").strip()
        if pnr not in self.pnr_db:
            print("Error: Invalid PNR Number.")
            return

        ticket = self.pnr_db[pnr]
        train = self.trains[ticket['train_num']]
        coach_class = ticket['class']
        queues = train.queues[coach_class]

        self.pnr_status()
        print("\nDo you want to cancel the ENTIRE ticket? (Y/N)")
        confirm = input("> ").strip().upper()

        if confirm == 'Y':
            # Remove all passengers from queues
            for idx, p in enumerate(ticket['passengers']):
                if p['status'] == "CANCELLED":
                    continue
                
                p_id = f"{pnr}_{idx}"
                # Find and remove passenger from respective queue
                if p_id in queues['CNF']:
                    queues['CNF'].remove(p_id)
                elif p_id in queues['RAC']:
                    queues['RAC'].remove(p_id)
                elif p_id in queues['WL']:
                    queues['WL'].remove(p_id)
                
                p['status'] = "CANCELLED"
                p['seat'] = "-"

            # Process queue shifting (Cascade WL -> RAC -> CNF)
            self._shift_queues(train, coach_class)
            print(f"Ticket {pnr} has been completely cancelled. Refund initiated.")
        else:
            print("Partial cancellation aborted (simulated).")

    def _shift_queues(self, train, coach_class):
        config = train.classes[coach_class]
        queues = train.queues[coach_class]

        # Shift RAC to CNF
        while len(queues['CNF']) < config['total_cnf'] and len(queues['RAC']) > 0:
            promoted_p_id = queues['RAC'].pop(0)
            queues['CNF'].append(promoted_p_id)
            self._update_passenger_status(promoted_p_id, "CNF", f"{coach_class}-{len(queues['CNF'])}")

        # Shift WL to RAC
        while len(queues['RAC']) < config['total_rac'] and len(queues['WL']) > 0:
            promoted_p_id = queues['WL'].pop(0)
            queues['RAC'].append(promoted_p_id)
            self._update_passenger_status(promoted_p_id, f"RAC{len(queues['RAC'])}", "Side Lower")

        # Update remaining WL numbers
        for i, p_id in enumerate(queues['WL']):
            self._update_passenger_status(p_id, f"WL{i+1}", "Pending")

    def _update_passenger_status(self, p_id, new_status, new_seat):
        pnr, idx = p_id.split('_')
        idx = int(idx)
        passenger = self.pnr_db[pnr]['passengers'][idx]
        passenger['status'] = new_status
        passenger['seat'] = new_seat

    def view_train_chart(self):
        t_num = input("\nEnter Train Number for Charting: ").strip()
        if t_num not in self.trains:
            print("Error: Invalid Train.")
            return

        train = self.trains[t_num]
        print(f"\n--- Reservation Chart: {train.name} ({t_num}) ---")
        for cls in train.classes:
            queues = train.queues[cls]
            print(f"\nClass: {cls} | CNF: {len(queues['CNF'])} | RAC: {len(queues['RAC'])} | WL: {len(queues['WL'])}")
            
            print("Confirmed Passengers:")
            for p_id in queues['CNF']:
                pnr, idx = p_id.split('_')
                p = self.pnr_db[pnr]['passengers'][int(idx)]
                print(f"  - {p['name']} (PNR: {pnr}, Seat: {p['seat']})")
                
            if not queues['CNF']: print("  (None)")


def main():
    irctc = RailwaySystem()
    print("=" * 50)
    print("    WELCOME TO INDIAN RAILWAYS RESERVATION SYSTEM")
    print("=" * 50)

    while True:
        print("\n" + "-" * 30)
        print("           MAIN MENU")
        print("-" * 30)
        print("1. Search Train")
        print("2. Book Ticket")
        print("3. Check PNR Status")
        print("4. Cancel Ticket")
        print("5. View Train Chart (Admin)")
        print("6. Exit")
        
        choice = input("Select Option (1-6): ").strip()
        
        if choice == '1':
            src = input("Enter Source Station (e.g., DELHI, MUMBAI): ")
            dest = input("Enter Destination Station: ")
            irctc.search_trains(src, dest)
        elif choice == '2':
            irctc.book_ticket()
        elif choice == '3':
            irctc.pnr_status()
        elif choice == '4':
            irctc.cancel_ticket()
        elif choice == '5':
            irctc.view_train_chart()
        elif choice == '6':
            print("Thank you for using Indian Railways. Happy Journey!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()






#    output:  ==================================================
#     WELCOME TO INDIAN RAILWAYS RESERVATION SYSTEM
# ==================================================

# ------------------------------
#            MAIN MENU
# ------------------------------
# 1. Search Train
# 2. Book Ticket
# 3. Check PNR Status
# 4. Cancel Ticket
# 5. View Train Chart (Admin)
# 6. Exit
# Select Option (1-6): 1
# Enter Source Station (e.g., DELHI, MUMBAI): chennai
# Enter Destination Station: hyderabad

# --- Trains from CHENNAI to HYDERABAD ---
# [12759] Charminar Express | Distance: 790 km
# Availability & Fares:
#   - 1AC: AVAILABLE (2) | Fare: Rs. 4937.50
#   - 2AC: AVAILABLE (2) | Fare: Rs. 2962.50
#   - 3AC: AVAILABLE (3) | Fare: Rs. 1975.00
#   - SL: AVAILABLE (5) | Fare: Rs. 987.50

# ------------------------------
#            MAIN MENU
# ------------------------------
# 1. Search Train
# 2. Book Ticket
# 3. Check PNR Status
# 4. Cancel Ticket
# 5. View Train Chart (Admin)
# 6. Exit
# Select Option (1-6): 2

# --- Book Ticket ---
# Enter Train Number: 12759
# Enter Class (1AC/2AC/3AC/SL): 2AC
# Enter number of passengers (Max 4): 1

# Passenger 1 Details:
#   Name: sid
#   Age: 20
#   Gender (M/F/O): M

# Booking Successful!
# Your PNR Number is: 2545417493
# Total Fare: Rs. 2962.50

# ------------------------------
#            MAIN MENU
# ------------------------------
# 1. Search Train
# 2. Book Ticket
# 3. Check PNR Status
# 4. Cancel Ticket
# 5. View Train Chart (Admin)
# 6. Exit
# Select Option (1-6): 3

# Enter 10-digit PNR: 2545417493

# ==================================================
# PNR STATUS: 2545417493
# Train: 12759 - Charminar Express
# Route: CHENNAI to HYDERABAD | Date: 2026-09-19
# Class: 2AC | Total Fare: Rs. 2962.50
# --------------------------------------------------
# Name            | Age | Sex | Status   | Seat
# --------------------------------------------------
# sid             | 20  | M   | CNF      | 2AC-1
# ==================================================

# ------------------------------
#            MAIN MENU
# ------------------------------
# 1. Search Train
# 2. Book Ticket
# 3. Check PNR Status
# 4. Cancel Ticket
# 5. View Train Chart (Admin)
# 6. Exit
# Select Option (1-6): 5

# Enter Train Number for Charting: 12759

# --- Reservation Chart: Charminar Express (12759) ---

# Class: 1AC | CNF: 0 | RAC: 0 | WL: 0
# Confirmed Passengers:
#   (None)

# Class: 2AC | CNF: 1 | RAC: 0 | WL: 0
# Confirmed Passengers:
#   - sid (PNR: 2545417493, Seat: 2AC-1)

# Class: 3AC | CNF: 0 | RAC: 0 | WL: 0
# Confirmed Passengers:
#   (None)

# Class: SL | CNF: 0 | RAC: 0 | WL: 0
# Confirmed Passengers:
#   (None)

# ------------------------------
#            MAIN MENU
# ------------------------------
# 1. Search Train
# 2. Book Ticket
# 3. Check PNR Status
# 4. Cancel Ticket
# 5. View Train Chart (Admin)
# 6. Exit
# Select Option (1-6): 4

# Enter PNR to cancel: 2545417493

# Enter 10-digit PNR: 2545417493

# ==================================================
# PNR STATUS: 2545417493
# Train: 12759 - Charminar Express
# Route: CHENNAI to HYDERABAD | Date: 2026-09-19
# Class: 2AC | Total Fare: Rs. 2962.50
# --------------------------------------------------
# Name            | Age | Sex | Status   | Seat
# --------------------------------------------------
# sid             | 20  | M   | CNF      | 2AC-1
# ==================================================

# Do you want to cancel the ENTIRE ticket? (Y/N)
# > Y
# Ticket 2545417493 has been completely cancelled. Refund initiated.

# ------------------------------
#            MAIN MENU
# ------------------------------
# 1. Search Train
# 2. Book Ticket
# 3. Check PNR Status
# 4. Cancel Ticket
# 5. View Train Chart (Admin)
# 6. Exit
# Select Option (1-6): 6
# Thank you for using Indian Railways. Happy Journey!