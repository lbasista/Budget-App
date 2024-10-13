class Category:
    def __init__(self, name):
        self.category = name
        self.ledger = []
    def deposit(self, amount, description = ""):
        self.ledger.append({"amount": amount, "description": description})
    def withdraw(self, amount, description = ""):
        if not self.check_funds(amount):
            return False
        else:
            self.ledger.append({'amount': -1 * amount, 'description': description})
            return True
    def get_balance(self):
        fund = 0
        for transaction in self.ledger:
            fund += transaction["amount"]
        return fund
    def transfer(self, amount, budget):
        if not self.withdraw(amount, f"Transfer to {budget.category}"):
            return False
        else:
            budget.deposit(amount, f"Transfer from {self.category}")
            return True
    def check_funds(self, amount):
        if self.get_balance() < amount:
            return False
        else:
            return True
    def get_withdraw_amount(self):
        amount = 0
        for a in self.ledger:
            if a["amount"] < 0:
                amount += a["amount"]
        return amount
    def calc_percentage_withdraw(self, total):
        return round(self.get_withdraw_amount() * -1 / total * 100 / 10) * 10
    def __repr__(self):
        num_ast = (30 - len(self.category)) // 2
        result = ""
        for i in range(num_ast):
            result += "*"
        result += self.category
        for i in range(num_ast):
            result += "*"
        result += "\n"
        for t in self.ledger:
            end = len(str(t["description"]))
            if end > 23:
                end = 23
            result += t["description"][0:end]
            amount = "{:.2f}".format(t["amount"])
            num_space = 7-len(str(amount)) + 23 - len(t["description"][0:end])
            for i in range(num_space):
                result += " "
            result += str(amount) + "\n"
        bal = "{:.2f}".format(self.get_balance())
        result += f"Total: {bal}"
        return result

def create_spend_chart(categories):
    spend_list = []
    for category in categories:
        negative_items = 0
        for item in category.ledger:
            if item['amount'] < 0:
                negative_items += abs(item['amount'])
        spend_list.append(negative_items)

    all_spends = sum(spend_list)
    percent_list = [((item/all_spends) * 100) for item in spend_list]
    output_chart = "Percentage spent by category"
    for row in range(100, -10, -10):
        output_chart += '\n' + str(row).rjust(3) + '|'
        for column_value in percent_list:
            if column_value > row:
                output_chart += ' o '
            else:
                output_chart += '   '
        output_chart += ' '
    output_chart += "\n    ----------"
    cat_lengts = []
    for cat in categories:
        cat_lengts.append(len(cat.category))
    max_len = max(cat_lengts)
    for row in range(max_len):
        output_chart += '\n    '
        for column_item in range(len(categories)):
            if row < cat_lengts[column_item]:
                output_chart += ' ' + categories[column_item].category[row] + ' '
            else:
                output_chart += '   '
        output_chart += ' '
    return output_chart

# Przykładowe wywołanie
def main():
    # Tworzenie kategorii
    food = Category("Food")
    entertainment = Category("Entertainment")
    clothing = Category("Clothing")

    # Dodawanie transakcji
    food.deposit(1000, "Initial deposit")
    food.withdraw(200, "Groceries")
    food.withdraw(150, "Restaurants")

    entertainment.deposit(500, "Initial deposit")
    entertainment.withdraw(150, "Movies")
    entertainment.withdraw(50, "Concert")

    clothing.deposit(300, "Initial deposit")
    clothing.withdraw(100, "New shirt")
    clothing.withdraw(50, "Pants")

    # Wywołanie funkcji do tworzenia wykresu wydatków
    categories = [food, entertainment, clothing]
    chart = create_spend_chart(categories)

    # Wyświetlenie wyników
    print(food)
    print(entertainment)
    print(clothing)
    print(chart)

# Uruchom program
if __name__ == "__main__":
    main()