import csv
import os
import re
import hashlib

def validate_email(email):
    # Regular expression for validating email addresses
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    else:
        return False

def validate_phone_number(phone_number):
    # Regular expression for validating 11-digit phone numbers
    pattern = r'^\d{11}$'
    if re.match(pattern, phone_number):
        return True
    else:
        return False
    
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Function for creating a new account
def create_account():
    global surname
    global first_name
    global user_name
    global phone_number
    surname = str(input("Enter your surname: ")).upper().strip()
    first_name = str(input("Enter your first name: ")).upper().strip()
    user_name = input("Enter a unique name: ").upper().strip()
    if os.path.exists("user.csv"):
        with open("user.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == user_name:
                    print("User name already exists")
                    return create_account()
    email = input("Enter your Email: ")
    if validate_email(email):
        print("Valid email address.")
    else:
        print("Invalid email address. Please enter a valid email address.")
        new_email = input("Enter your Email: ")
        if validate_email(new_email):
            new_email = email
            print("Valid email address.")
        else:
            print("INVALID EMAIL ADDRESS! PLEASE ENTER A VALID EMAIL ADDRESS.")
            create_account()
    phone_number = input("Enter your phone number: ")
    if validate_phone_number(phone_number):
        print("Valid Phone number")
    else:
        print("Invalid Phone number")
        new_phone_number = input("Enter your phone number: ")
        if validate_email(new_phone_number):
            new_phone_number = phone_number
            print("Valid Phone number")
        else:
            print("INVALID PHONE NUMBER! PLEASE ENTER A VALID PHONE NUMBER")
            return create_account()
    password = input("Enter a 6-digit password: ")
    if len(password) != 6:
        print("PLEASE ENTER A 6 DIGIT PASSWORD")
    else:
        print(f"\nACCOUNT CREATED SUCCESSFULLY! YOUR ACCOUNT NUMBER IS {phone_number}\n")

    # Add new user to CSV file
    with open("user.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([surname, first_name, user_name, email, phone_number, password, 0.0])

def logout():
    main()

def show_balance(user_name):
    # Read the current balance from the CSV file
    with open("user.csv", "r") as file:
        reader = csv.DictReader(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
        for row in reader:
            if row["user_name"] == user_name:
                balance = float(row["balance"])
                print(f"\nYour Account Balance Is: ${round(balance, 2)}\n")
                break

def deposit(user_name, amount):
    amount = float(input("Enter amount: $"))
    # Read the current balance from the CSV file
    with open("user.csv", "r") as file:
        reader = csv.DictReader(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
        for row in reader:
            if row["user_name"] == user_name:
                current_balance = float(row["balance"])
                break
    # Update the balance
    new_balance = current_balance + amount
    # Write the new balance to the CSV file
    with open("user.csv", "r") as file:
        reader = csv.DictReader(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
        rows = [row for row in reader]
    with open("user.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
        writer.writeheader()
        for row in rows:
            if row["user_name"] == user_name:
                row["balance"] = str(new_balance)
            writer.writerow(row)

def withdraw(user_name):
    withdrawal_amount = float(input("ENTER AMOUNT: $"))
    # Read the current balance from the CSV file
    with open("user.csv", "r") as file:
        reader = csv.DictReader(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
        for row in reader:
            if row["user_name"] == user_name:
                current_balance = float(row["balance"])
                break
    if withdrawal_amount > current_balance:
        print("INSUFFICIENT FUNDS")
        return 0
    elif withdrawal_amount < 0:
        print("ENTER AN AMOUNT GREATER THAN 0")
        return 0
    else:
        new_balance = current_balance - withdrawal_amount
        # Write the new balance to the CSV file
        with open("user.csv", "r") as file:
            reader = csv.DictReader(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
            rows = [row for row in reader]
        with open("user.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
            writer.writeheader()
            for row in rows:
                if row["user_name"] == user_name:
                    row["balance"] = str(new_balance)
                writer.writerow(row)

def transfer_funds(sender_user_name):
    recipient_user_name = input("Enter the recipient's user name: ").upper().strip()
    transfer_amount = float(input("Enter the amount to transfer: $"))
    
    # Check if the sender has sufficient balance
    with open("user.csv", "r") as file:
        reader = csv.DictReader(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
        rows = [row for row in reader]
        sender_row = None
        recipient_row = None
        for row in rows:
            if row["user_name"] == sender_user_name:
                sender_row = row
            if row["user_name"] == recipient_user_name:
                recipient_row = row

    sender_balance = float(sender_row["balance"])
    if not sender_row:
        print("Sender account not found.")
        print("Please try again.")
        return transfer_funds()

    elif not recipient_row:
        print("Recipient account not found.")
        print("Please try again.")
        return transfer_funds()

    elif transfer_amount <= 0:
        print("Enter an amount greater than 0.")
        print("Please try again.")
        return transfer_funds()

    elif transfer_amount > sender_balance:
        print("Insufficient funds.")
        print("Please try again.")
        return transfer_funds()
    
    # Update balances
    else:
        sender_row["balance"] = str(sender_balance - transfer_amount)
        recipient_row["balance"] = str(float(recipient_row["balance"]) + transfer_amount)
    
    # Write the updated balances back to the CSV file
    with open("user.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    
    print(f"\n${transfer_amount} has been successfully transferred to {recipient_user_name}'s account.\n")
    

def login():
    user_name = input("Enter your user name: ").upper().strip()
    password = input("Enter your password: ").strip()
    phone_number = None
    
    if os.path.exists("user.csv"):
        with open("user.csv", "r") as file:
            reader = csv.DictReader(file, fieldnames=['surname', 'first_name', 'user_name', 'email', 'phone_number', 'password', 'balance'])
            for row in reader:
                print(f"Checking user: {row['user_name']} and password: {row['password']}")
                if row["user_name"] == user_name and row["password"] == password:
                    print("Login successful!\n")
                    phone_number = row["phone_number"]
                    print(f'\nWELCOME BACK {user_name}\n'f'\nACCOUNT NUMBER: {phone_number}\n')
                    is_running = True
                    while is_running:
                        
                        print("*****************")
                        print("    WHAT WOULD YOU LIKE TO DO?     ")
                        print("*****************") 
                        print("1. TRANSFER")
                        print("2. DEPOSIT")
                        print("3. WITHDRAWAL")
                        print("4. SHOW BALANCE")
                        print("5. LOG OUT")
                        print("*****************")
                        try:
                            choice_2 = int(input("ENTER YOUR CHOICE FROM (1 ~ 5): "))
                            if choice_2 == 1:
                                transfer_funds(user_name)
                            elif choice_2 == 2:
                                deposit(user_name, amount=0)
                            elif choice_2 == 3:
                                withdraw(user_name)
                            elif choice_2 == 4:
                                show_balance(user_name)
                            elif choice_2 == 5:
                                logout()
                            else:
                                print("INVALID CHOICE. Please try again.")
                        except ValueError:
                            print("\nINVALID INPUT! PLEASE ENTER A NUMBER.\n")
                    return  # Exit the login function once user successfully logs in
            print("Invalid credentials. Please try again.")
            login()  # If credentials are invalid, retry login

def main():
    is_running = True
    while is_running:
        print("*****************")
        print("    BANK PROGRAM     ")
        print("*****************")
        print("1. CREATE AN ACCOUNT")
        print("2. LOGIN INTO YOUR ACCOUNT")
        print("*****************")
        try:
            choice = int(input("ENTER YOUR CHOICE (1 OR 2): "))
            if choice == 1:
                create_account()
            elif choice == 2:
                login()
            else:
                print("INVALID CHOICE")
                main()
            break
        except ValueError:
            print("\nINVALID INPUT! PLEASE ENTER A NUMBER.\n")
    print("\nTHANK YOU FOR USING THIS APP!\n")

if __name__ == '__main__':
    main()
