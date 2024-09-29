import json
from datetime import datetime
import os
from termcolor import colored

# Constants
BANK_DATA_FILE = "bank_data.json"
MENU_OPTIONS = {
    "1": "Skapa konto",
    "2": "Logga in",
    "3": "Visa alla transaktioner",
    "4": "Avsluta",
}

accounts = {}


def save_data():
    with open(BANK_DATA_FILE, "w") as f:
        json.dump(accounts, f, default=str)


def load_data():
    global accounts
    if os.path.exists(BANK_DATA_FILE):
        with open(BANK_DATA_FILE, "r") as f:
            accounts = json.load(f)
    else:
        accounts = {}
        save_data()  # create save data in case file doesn't exist


############
# Decorators
############


def print_header(text):
    border = "*" * (len(text) + 4)
    print(colored(f"\n{border}", "cyan"))
    print(colored(f"* {text} *", "cyan", attrs=["bold"]))
    print(colored(f"{border}\n", "cyan"))


def print_success(text):
    border = "=" * (len(text) + 4)
    print(colored(f"\n{border}", "green"))
    print(colored(f"✓ {text} ✓", "green", attrs=["bold"]))
    print(colored(f"{border}\n", "green"))


def print_warning(text):
    border = "!" * (len(text) + 4)
    print(colored(f"\n{border}", "yellow"))
    print(colored(f"! {text} !", "yellow", attrs=["bold"]))
    print(colored(f"{border}\n", "yellow"))


def print_error(text):
    border = "X" * (len(text) + 4)
    print(colored(f"\n{border}", "red"))
    print(colored(f"X {text} X", "red", attrs=["bold"]))
    print(colored(f"{border}\n", "red"))


############
# Program
############


def menu():
    print_header("Bankomat")
    for key, value in MENU_OPTIONS.items():
        print(colored(f"{key}. {value}", "cyan"))

    user_input = input(colored("\nMeny val > ", "magenta"))
    if user_input in MENU_OPTIONS:
        match user_input:
            case "1":
                make_account()
            case "2":
                usr_id = input(colored("Kontonummer?: ", "magenta"))
                log_in(usr_id)
            case "3":
                show_all_transactions()
            case "4":
                print_header("Programmet avslutas")
                print_success("Hej då!")
                save_data()
                quit()
    else:
        print_error("Ogiltigt val, försök igen.")


def make_account():
    print_header("Lägg till användare")
    add_user = input(colored("Ange kontonummer: ", "magenta"))

    if add_user in accounts:
        print_error("Användaren finns redan\nVar god och testa igen")
    else:
        accounts[add_user] = []
        print_success(f"Konto {add_user} har skapats!\nDu kan nu logga in.")

    save_data()


def log_in(user_id):
    if user_id in accounts:
        print_header(f"Inloggad som kund ID: {user_id}")
        while True:
            print(
                colored(
                    "\n1. Ta ut pengar\n2. Sätt in pengar\n3. Visa saldo\n4. Visa transaktioner\n5. Avsluta (Gå till Huvudmeny)",
                    "yellow",
                )
            )
            account_user_input = input(colored("\nVal > ", "magenta"))
            match account_user_input:
                case "1":
                    withdraw_money(user_id)
                case "2":
                    deposit_money(user_id)
                case "3":
                    print_header("Saldo")
                    print_success(f"Ditt saldo är: {calculate_balance(user_id)} kr")
                case "4":
                    show_transactions(user_id)
                case "5":
                    return
                case _:
                    print_error("Ogiltigt val, försök igen.")
    else:
        print_error("Finns inget kontonummer med denna ID, testa igen")


################
# User Functions
################


def withdraw_money(user_id):
    withdrawal_amount = int(input(colored("Ange belopp: ", "magenta")))
    if withdrawal_amount <= 0:
        print_error("Beloppet måste vara större än noll.")
        return
    current_balance = calculate_balance(user_id)
    if withdrawal_amount > current_balance:
        print_error("Du har inte tillräckligt med pengar på kontot.")
    else:
        new_balance = current_balance - withdrawal_amount
        transaction = create_transaction(user_id, "uttag", -withdrawal_amount)
        accounts[user_id].append(transaction)
        print_success(
            f"{withdrawal_amount} kr har tagits ut. Ditt nya saldo är {new_balance} kr"
        )
        save_data()


def deposit_money(user_id):
    user_deposit = int(input(colored("Ange belopp: ", "magenta")))
    if user_deposit <= 0:
        print_error("Beloppet måste vara större än noll.")
        return
    transaction = create_transaction(user_id, "insättning", user_deposit)
    accounts[user_id].append(transaction)
    new_saldo = calculate_balance(user_id)
    print_success(f"{user_deposit} kr har satts in. Ditt nya saldo är {new_saldo} kr")
    save_data()


def create_transaction(user_id, type, amount):
    return {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "account": user_id,
        "type": type,
        "amount": amount,
    }


def calculate_balance(user_id):
    return sum(transaction["amount"] for transaction in accounts[str(user_id)])


def print_transaction(transaction, user_id=None):
    transaction_type = transaction["type"]
    amount = transaction["amount"]
    color = "green" if transaction_type == "insättning" else "red"
    symbol = "+" if transaction_type == "insättning" else "-"

    if user_id:
        print(colored(f"Konto: {user_id}", "cyan"))
    print(colored(f"Datum: {transaction['date']}", "yellow"))
    print(colored(f"Typ: {transaction_type}", "yellow"))
    print(colored(f"Belopp: {symbol}{abs(amount)} kr", color))
    print(colored("-" * 40, "blue"))


def show_transactions(user_id):
    print_header(f"Transaktioner för konto {user_id}")
    if not accounts[str(user_id)]:
        print_warning("Inga transaktioner att visa.")
    else:
        for transaction in accounts[str(user_id)]:
            print_transaction(transaction)


def show_all_transactions():
    print_header("Alla transaktioner")
    if not any(accounts.values()):
        print_warning("Inga transaktioner att visa.")
    else:
        for user_id, transactions in accounts.items():
            for transaction in transactions:
                print_transaction(transaction, user_id)
                print()


def main():
    load_data()
    while True:
        menu()


if __name__ == "__main__":
    main()
