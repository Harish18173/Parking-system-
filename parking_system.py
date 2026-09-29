"""
Smart Parking Lot Management System
------------------------------------
Console-based Python project.
Features:
  1. Display parking slots
  2. Park vehicle
  3. Exit vehicle & calculate fee
  4. Search vehicle
  5. Display parking history
  6. Exit

Data is stored in memory only (lost when the program closes).
"""

import math

# ---------------------------
# Sample Data
# ---------------------------

# Slot ID -> slot info. C = car slots, B = bike slots
slots = {}
for i in range(1, 7):
    slots[f"C{i}"] = {"type": "Car", "vehicle": None}
for i in range(1, 5):
    slots[f"B{i}"] = {"type": "Bike", "vehicle": None}

# Hourly rates (Rs. per hour)
rates = {"Car": 30, "Bike": 10}

# Records of every parking session
records = []
record_counter = 1


# ---------------------------
# Functions
# ---------------------------

def display_slots():
    print("\n--- Parking Slots ---")
    print(f"{'Slot':<8}{'Type':<8}{'Status':<12}{'Vehicle No.':<14}")
    for sid, info in slots.items():
        status = "Free" if info["vehicle"] is None else "Occupied"
        vehicle = info["vehicle"] if info["vehicle"] else "-"
        print(f"{sid:<8}{info['type']:<8}{status:<12}{vehicle:<14}")
    free = sum(1 for s in slots.values() if s["vehicle"] is None)
    print(f"\nFree slots: {free}/{len(slots)}")


def find_free_slot(vehicle_type):
    for sid, info in slots.items():
        if info["type"] == vehicle_type and info["vehicle"] is None:
            return sid
    return None


def is_already_parked(vehicle_no):
    return any(info["vehicle"] == vehicle_no for info in slots.values())


def park_vehicle():
    global record_counter
    print("\nVehicle type: 1. Car   2. Bike")
    choice = input("Enter choice (1/2): ").strip()
    if choice == "1":
        vtype = "Car"
    elif choice == "2":
        vtype = "Bike"
    else:
        print("Invalid vehicle type!")
        return

    vehicle_no = input("Enter vehicle number: ").strip().upper()
    if not vehicle_no:
        print("Vehicle number cannot be empty!")
        return
    if is_already_parked(vehicle_no):
        print("This vehicle is already parked!")
        return

    owner = input("Enter owner name: ").strip()

    slot_id = find_free_slot(vtype)
    if slot_id is None:
        print(f"Sorry, no free {vtype} slots available!")
        return

    slots[slot_id]["vehicle"] = vehicle_no
    records.append({
        "record_id": f"P{record_counter:03}",
        "vehicle_no": vehicle_no,
        "owner": owner,
        "type": vtype,
        "slot": slot_id,
        "hours": None,
        "fee": None,
        "status": "Parked",
    })
    record_counter += 1
    print(f"\nVehicle parked successfully in slot {slot_id}.")


def calculate_fee(vehicle_type, hours):
    # Any part of an hour is charged as a full hour (minimum 1 hour)
    billable_hours = max(1, math.ceil(hours))
    return rates[vehicle_type] * billable_hours


def exit_vehicle():
    vehicle_no = input("Enter vehicle number to exit: ").strip().upper()

    for rec in records:
        if rec["vehicle_no"] == vehicle_no and rec["status"] == "Parked":
            try:
                hours = float(input("Enter hours parked: ").strip())
                if hours < 0:
                    raise ValueError
            except ValueError:
                print("Invalid hours! Please enter a positive number.")
                return

            fee = calculate_fee(rec["type"], hours)
            rec["hours"] = hours
            rec["fee"] = fee
            rec["status"] = "Exited"
            slots[rec["slot"]]["vehicle"] = None
            print(f"\nVehicle {vehicle_no} exited from slot {rec['slot']}.")
            print(f"Parking fee: Rs.{fee}")
            return

    print("No parked vehicle found with this number!")


def search_vehicle():
    vehicle_no = input("Enter vehicle number to search: ").strip().upper()
    found = False

    print("\n--- Search Results ---")
    for rec in records:
        if rec["vehicle_no"] == vehicle_no:
            found = True
            fee = f"Rs.{rec['fee']}" if rec["fee"] is not None else "-"
            print(f"{rec['record_id']} | {rec['vehicle_no']} ({rec['type']}) | "
                  f"Owner: {rec['owner']} | Slot: {rec['slot']} | "
                  f"Status: {rec['status']} | Fee: {fee}")
    if not found:
        print("No record found for this vehicle.")


def display_history():
    if not records:
        print("\nNo parking records yet.")
        return

    print("\n--- Parking History ---")
    total = 0
    for rec in records:
        fee = f"Rs.{rec['fee']}" if rec["fee"] is not None else "-"
        if rec["fee"]:
            total += rec["fee"]
        print(f"{rec['record_id']} | {rec['vehicle_no']} ({rec['type']}) | "
              f"Owner: {rec['owner']} | Slot: {rec['slot']} | "
              f"Status: {rec['status']} | Fee: {fee}")
    print(f"\nTotal collection: Rs.{total}")


# ---------------------------
# Main Menu
# ---------------------------

def main():
    while True:
        print("\n====== Smart Parking Lot Management System ======")
        print("1. Display Parking Slots")
        print("2. Park Vehicle")
        print("3. Exit Vehicle & Calculate Fee")
        print("4. Search Vehicle")
        print("5. Display Parking History")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            display_slots()
        elif choice == "2":
            park_vehicle()
        elif choice == "3":
            exit_vehicle()
        elif choice == "4":
            search_vehicle()
        elif choice == "5":
            display_history()
        elif choice == "6":
            print("Thank you for using the Parking System. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1-6.")


if __name__ == "__main__":
    main()
