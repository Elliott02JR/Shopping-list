import sqlite3
from tabulate import tabulate

class Shopping_list:
    def __init__(self):
        self.connector = sqlite3.connect("Shopping List.db")
        self.cursor = self.connector.cursor()
        self.active_table = None


    def Create_Tables(self,Recipie):
        try:
            self.cursor.execute(f"CREATE TABLE {Recipie} (Ingredient TEXT PRIMARY KEY, quantity int NOT NULL, Ing_ID int NOT NULL)")
            return None
        except sqlite3.OperationalError:
            return ("Recipie Already Exists")
        except Exception as e:
            return e
    
    
    def Create_Ingredients_Table(self):
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS Ingredients (Ing_ID INTEGER PRIMARY KEY AUTOINCREMENT, Ingredient char(20) NOT NULL)")
            print("Ingredients table created")
            return None
        except sqlite3.OperationalError:
            return ("Ingredients table already exists")
        except Exception as e:
            #return e
            print(f"OperationalError: {e}")

    def Ingredient_exist_check(self,table, column, value):

        exist_check = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {column} = ?)"
        self.cursor.execute(exist_check,(value,))
        exists, = self.cursor.fetchone()
        if bool(exists):
            value_ID = f"SELECT Ing_ID FROM {table} WHERE {column} = ?"
            self.cursor.execute(value_ID,(value,))
            value_ID = self.cursor.fetchone()
            return value_ID[0]
        else:
            add_ingredient = f"INSERT INTO {table} ({column}) VALUES (?)"
            self.cursor.execute(add_ingredient,(value,))
            self.connector.commit()
            value_ID = f"SELECT Ing_ID FROM {table} WHERE {column} = ?"
            self.cursor.execute(value_ID,(value,))
            value_ID = self.cursor.fetchone()
            return value_ID[0]


    def check_ingredient_input(self):
        while True:
            ingredient = str(input("Please enter the ingredient: "))
            if 0 < len(ingredient) <= 20:
                return ingredient
            else:
                print("The input is limited to 20 characters. Please Reneter")
    
    def check_quantity_input(self):
        while True:
            Quant = int(input("Please enter the Quantity: "))
            if type(Quant) == int and 0 < Quant <= 2000  :
                return Quant
            else:
                print("Only enter an interger below 2000")


    def add_recipie(self, Recipie):
        print("Type Done into the console to stop the code running")
        while True:
            
            ing = self.check_ingredient_input()
            value_ID = self.Ingredient_exist_check(table = "Ingredients", column = "Ingredient", value = ing)
            if ing == "Break":
                break
            

                
            quant = self.check_quantity_input()
            if quant == "Break":
                break

                
            add_recipie_row = f"INSERT INTO {Recipie}(Ingredient, quantity, Ing_ID) VALUES (?,?,?)"
            try:
                self.cursor.execute(add_recipie_row,(ing, quant, value_ID))
                self.connector.commit()
            except sqlite3.IntegrityError:
                print(ing + " is already in list, please add another ingredient")
            except Exception as e:
                print(f"OperationalError: {e}")
    
    def view_recipie(self, Recipie):
        view_Recipie = f"SELECT * FROM {Recipie}"
        self.cursor.execute(view_Recipie)
        view_Recipie = self.cursor.fetchall()
        Table = [["Ingredient","Quantity","ID"]]
        for row in view_Recipie:
            Table.append(row)
        print(tabulate(Table, headers='firstrow', tablefmt='fancy_grid'))

    def view_all_tables(self):
        try:
            view_all_tables = f"SELECT name FROM sqlite_master WHERE type='table'"
            self.cursor.execute(view_all_tables)
            view_all_tables = self.cursor.fetchall()
            Table_table = [["Recipies"]]
            for row in view_all_tables:
                Table_table.append(row)
            print(tabulate(Table_table, headers='firstrow', tablefmt='fancy_grid'))
        except Exception as e:
            print(f"OperationalError: {e}")
    
    def select_table_to_view(self,table):
        self.active_table = table
        return table
    
    def delete_item_from_table(self, table, item):



    def Main_code(self):

        print("Type 'Break' to exit the code")

        while True:
            print("Please select from the following options:")
            print("1. View and Edit Recipies")
            print("2. View this weeks meal plan")
            print("3. Create a custom shopping list for this week")
            print("4. Add a new recipie")

            while True:
                response = ("Input: ")
                if response = 1:
                    Shopping_list.view_all_tables()
                    #Add in def for entering and editing a table





#Shopping_list().Create_Ingredients_Table()
#Shopping_list().Create_Tables(Recipie= "Test12")

Shopping_list().add_recipie(Recipie="Test12")
Shopping_list().view_recipie(Recipie="Test12")
Shopping_list().view_all_tables()





