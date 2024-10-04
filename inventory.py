# This program allows users to see the shoe inventory of a warehouse.
# It reads from the text file "inventory.txt"
# and allows users to perform various functions on the inventory.

# Imported modules
from tabulate import tabulate
import string


class Shoe:
    """Class representing a shoe item in inventory."""
    def __init__(self, country, code, product, cost, quantity):
        """Initialize a new Shoe object.

        Args:
            country (str): The country of origin for the shoe.
            code (str): The unique code (SKU) for the shoe.
            product (str): The name of the shoe product.
            cost (float): The cost of each unit of the shoe.
            quantity (int): The quantity of this shoe in inventory.
        """
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_country(self):
        """Get the country of the shoe."""
        return self.country

    def get_code(self):
        """Get the code (SKU) of the shoe."""
        return self.code

    def get_product(self):
        """Get the product name of the shoe."""
        return self.product

    def get_cost(self):
        """Get the cost of the shoe."""
        return self.cost

    def get_quantity(self):
        """Get the quantity of this shoe in inventory."""
        return self.quantity

    def __str__(self):
        """Return a string representation of the Shoe object."""
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


# Empty list of shoes to store the inventory as objects.
shoe_list = []


def read_shoes_data():
    """Read shoe inventory data from a file and populate shoe_list."""
    read_data = False
    try:
        with open("inventory.txt", "r") as inventory_file:
            next(inventory_file)
            for line in inventory_file:
                temp = line.strip().split(",")
                shoe_list.append(Shoe(temp[0], temp[1], temp[2], temp[3], temp[4]))
                read_data = True
    except FileNotFoundError:
        print("*File not found. Please make sure the file 'inventory.txt' exists in the same directory.*\n")
        if read_data is False:
            exit()


def capture_shoes():
    """Capture new shoe details from user input and add to shoe_list
    and inventory file.
    """
    country = input("\nEnter the country: ")
    country = string.capwords(country)
    while True:
        code = input("\nEnter the code (eg. SKU55555): ").upper()
        if len(code) == 8:
            break
        else:
            print("\n*Invalid code. Code should be 8 characters long including 'SKU' (eg. SKU55555)*")
    product = input("\nEnter the product name: ")
    product = string.capwords(product)

    while True:
        try:
            cost = float(input("\nEnter the cost: "))
            quantity = int(input("\nEnter the quantity: "))
            new_shoe = Shoe(country, code, product, cost, quantity)
            shoe_list.append(new_shoe)
            with open("inventory.txt", "a") as inventory_file:
                inventory_file.write("\n" + str(new_shoe))
            formatted_shoe = f"{new_shoe.country}, {new_shoe.code}, {new_shoe.product}, {new_shoe.cost}, {new_shoe.quantity}"
            print(f"\n***New shoe: {formatted_shoe} has been captured successfully.***\n")
            break
        except ValueError:
            print("\n*Invalid input. Please enter numeric values.*")


def view_all():
    """Display all shoes in the inventory using tabulate for a
    formatted table.
    """
    country = []
    code = []
    product = []
    cost = []
    quantity = []
    for lines in shoe_list:
        country.append(lines.get_country())
        code.append(lines.get_code())
        product.append(lines.get_product())
        cost.append(lines.get_cost())
        quantity.append(lines.get_quantity())
    table = zip(country, code, product, cost, quantity)
    print()
    print(tabulate(table, headers=["Country", "Code", "Product", "Cost", "Quantity"], tablefmt='fancy_grid'))
    print()


def restock_shoes():
    """Restock shoes with the lowest quantity by user input."""
    minimum_quantity = float("inf")
    minimum_product = None
    for lines in shoe_list:
        quantity = int(lines.get_quantity())
        if quantity < minimum_quantity:
            minimum_quantity = quantity
            minimum_product = lines
    if minimum_product is not None:
        print(f"\nThe lowest quantity is {minimum_quantity} ({minimum_product.country}, {minimum_product.code}, {minimum_product.product}, {minimum_product.cost})")

        while True:
            try:
                add_stock = int(input("""\nDo you want to add more stock to this product?
Enter 1 for Yes and 2 for No: """))
                if add_stock == 1:
                    try:
                        new_quantity = int(input("\nEnter the additional quantity: "))
                        minimum_product.quantity = int(minimum_product.quantity)
                        minimum_product.quantity += new_quantity
                        update_inventory_file()
                        print(f"""\n***Added {new_quantity} more stock to {minimum_product.country}, {minimum_product.code}, {minimum_product.product}, {minimum_product.cost}
New total stock is {minimum_product.quantity}.***\n""")
                        break
                    except ValueError:
                        print("\n*Invalid input. Please enter a numeric value.*\n")
                elif add_stock == 2:
                    print("\n***Restocking cancelled.***\n")
                    break
                else:
                    print("\n*Invalid input. Please enter 1 or 2.\n*")
            except ValueError:
                print("\n*Invalid input. Please enter 1 or 2.*\n")


def search_shoe():
    """Search for a shoe in the inventory based on user input."""
    while True:
        shoe_code = input("\nPlease enter the shoe code that you want to search (eg. SKU55555): ").upper()
        if len(shoe_code) == 8:
            break
        else:
            print("\n*Invalid code. Code should be 8 characters long including 'SKU' (eg. SKU55555)*")

    for index, line in enumerate(shoe_list):
        if shoe_code == line.get_code():
            print("\n***This shoe is already in the inventory.***\n")
            table = [(line.country, line.code, line.product, line.cost, line.quantity)]
            print(tabulate(table, headers=["Country", "Code", "Product", "Cost", "Quantity"], tablefmt='fancy_grid'))
            print()
            return index
    print("\n***This shoe is not available in the inventory.***\n")
    return None


def edit_or_delete(index):
    """Edit or delete a shoe from the inventory based on user input.

    Parameters:
    index (int): The index of the shoe in the shoe_list. If None, no
    operation is performed.
    """
    if index is not None:
        edit_choice = int(input("Enter 1 to edit, 2 to delete or 3 to return to the main menu: "))

        if edit_choice == 1:
            while True:
                try:
                    new_country = input("\nEnter the new country (leave blank to keep the same): ")
                    if new_country != "":
                        new_country = string.capwords(new_country)
                    else:
                        new_country = shoe_list[index].country

                    while True:
                        new_code = input("\nEnter the new code (leave blank to keep the same): ")
                        if new_code == "":
                            new_code = shoe_list[index].code
                            break
                        elif len(new_code) == 8:
                            new_code = new_code.upper()
                            break
                        else:
                            print("\n*Invalid code. Code should be 8 characters long including 'SKU' (eg. SKU55555)*")

                    new_product = input("\nEnter the new product name (leave blank to keep the same): ")
                    if new_product != "":
                        new_product = string.capwords(new_product)
                    else:
                        new_product = shoe_list[index].product

                    new_cost = input("\nEnter the new cost (leave blank to keep the same): ")
                    if new_cost != "":
                        new_cost = float(new_cost)
                    else:
                        new_cost = shoe_list[index].cost

                    new_quantity = input("\nEnter the new quantity (leave blank to keep the same): ")
                    if new_quantity != "":
                        new_quantity = int(new_quantity)
                    else:
                        new_quantity = shoe_list[index].quantity

                    updated_shoe = Shoe(new_country, new_code, new_product, new_cost, new_quantity)
                    shoe_list[index] = updated_shoe
                    update_inventory_file()
                    print("\n***Shoe details updated successfully.***\n")
                    break
                except ValueError:
                    print("\n*Invalid input. Please enter numeric values for cost and quantity.*\n")

        elif edit_choice == 2:
            del shoe_list[index]
            update_inventory_file()
            print("\n***Shoe deleted successfully.***\n")
        elif edit_choice == 3:
            print("\n***Edit or delete operation cancelled.***\n")
        else:
            print("\n*Invalid choice. Please enter 1 to edit or 2 to delete.*\n")
    else:
        print("*Please search for another shoe.*\n")


def update_inventory_file():
    """Update the inventory file with current shoe_list data."""
    with open("inventory.txt", "r") as inventory_file:
        lines = inventory_file.readlines()
    header = lines[0]

    with open("inventory.txt", "w") as inventory_file:
        inventory_file.write(header.strip())
        for line in shoe_list:
            inventory_file.write("\n" + str(line))


def value_per_item():
    """Calculate and display the total value per item in the
    inventory.
    """
    value_table = []
    for line in shoe_list:
        value = float(line.get_cost()) * int(line.get_quantity())
        value_table.append((line.country, line.code, line.product, line.cost, line.quantity, value))
    print()
    print(tabulate(value_table, headers=["Country", "Code", "Product", "Cost", "Quantity", "Value"], tablefmt='fancy_grid'))
    print()


def highest_qty():
    """Identify and display the shoe with the highest quantity in the
    inventory.
    """
    max_quantity = 0
    max_shoe = None
    for lines in shoe_list:
        shoe_quantity = int(lines.get_quantity())
        if shoe_quantity > max_quantity:
            max_quantity = shoe_quantity
            max_shoe = lines
    if max_shoe is not None:
        print("\nHighest quantity in stock:")
        print(f"***{max_shoe.country}, {max_shoe.code}, {max_shoe.product}, {max_shoe.cost}, {max_shoe.quantity} needs to be on SALE.***\n")
    else:
        print("\n*No shoes found in the inventory.*\n")


def main_menu():
    """Display the main menu and handle user interactions."""
    while True:
        try:
            user_choice = int(input("""Inventory Menu

Select one of the following options.
Please enter the number only.

1. Capture new shoes
2. View all shoes
3. Restock lowest quantity shoes
4. Search for shoes (edit/delete)
5. Total value per item
6. Highest quantity in stock
7. Exit
: """))
            if user_choice == 1:
                capture_shoes()
            elif user_choice == 2:
                view_all()
            elif user_choice == 3:
                restock_shoes()
            elif user_choice == 4:
                index = search_shoe()
                edit_or_delete(index)
            elif user_choice == 5:
                value_per_item()
            elif user_choice == 6:
                highest_qty()
            elif user_choice == 7:
                print("\n***Thank you for using the inventory system. Goodbye!***\n")
                exit()
            else:
                print("\n*Invalid input. Please enter a number between 1 and 7.*\n")
        except ValueError:
            print("\n*Invalid input. Please enter a number.*\n")


def main():
    """Main function to initialize the inventory system."""
    print("Welcome to the Shoe Inventory.\n")
    read_shoes_data()
    main_menu()


if __name__ == "__main__":
    main()


"""References:
https://www.geeksforgeeks.org/inventory-management-with-file-handling-in-python/
https://www.studytonight.com/python-howtos/how-to-read-a-file-from-line-2-or-skip-the-header-row#:~:text=Example%3A%20Read%20the%20Text%20File%20from%20Line%202%20using%20next()&text=This%20method%20uses%20next(),header_line%20%3D%20next(f)%20.
https://pypi.org/project/tabulate/
https://www.digitalocean.com/community/tutorials/python-str-repr-functions
https://www.geeksforgeeks.org/zip-in-python/
https://favtutor.com/blogs/infinity-python#:~:text=It%20represents%20too%20large%20values,inf')%20indicates%20negative%20infinity.
https://www.geeksforgeeks.org/convert-integer-to-string-in-python/
https://www.studocu.com/en-za/messages/question/2756326/countrycodeproductcostquantity-south-africasku44386air-max-90230020-chinasku90000jordan
https://github.com/ReagWarner/StockTake/blob/main/inventory.py
https://stackoverflow.com/questions/1549641/how-can-i-capitalize-the-first-letter-of-each-word-in-a-string"""
