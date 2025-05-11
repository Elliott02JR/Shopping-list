import sqlite3
from tabulate import tabulate

class Shopping_list:
    def __init__(self):
        self.connector = sqlite3.connect("Shopping List.db")
        self.cursor = self.connector.cursor()
        self.active_table = None


    def Create_Tables(self,Recipie):
            while True:
                try:
                    self.cursor.execute(f'CREATE TABLE IF NOT EXISTS "{Recipie}" (Ingredient TEXT PRIMARY KEY, quantity int NOT NULL, Ing_ID int NOT NULL)')
                    print("Table " + Recipie +"succesfully Created" )
                    self.connector.commit()
                    return None
                except sqlite3.OperationalError:
                    print ("Recipie Already Exists")
                    return
                except Exception as e:
                    print(e)
                    return e
    
    
    def create_all_recipies(self):
        while True:
            try:
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS 'All Recipies' (Recipie_ID INTEGER PRIMARY KEY AUTOINCREMENT, Recipie char(40) NOT NULL)")
                return None
            except sqlite3.OperationalError:
                return ("Ingredients table already exists")
            except Exception as e:
                return e
    def create_shopping_list(self):
        while True:
            try:
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS 'Shopping List' (Ingredient char(20) PRIMARY KEY, Quantity INT NOT NULL)")
                return None
            except sqlite3.OperationalError:
                return ("Shopping table already exists")
            except Exception as e:
                return e


    def Create_Ingredients_Table(self):
        while True:
            try:
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS Ingredients (Ing_ID INTEGER PRIMARY KEY AUTOINCREMENT, Ingredient char(20) NOT NULL)")
                print("Ingredients table created")
                return None
            except sqlite3.OperationalError:
                return ("Ingredients table already exists")
            except Exception as e:
                return e

    
    def Create_Mealplan_table(self):
        while True:    
            try:
                meal_plan = "Meal Plan"
                days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS 'Meal Plan' (day TEXT NOT NULL PRIMARY KEY, meal TEXT NOT NULL) ")
                
                for day in days_of_week:
                    self.cursor.execute(f"INSERT OR IGNORE INTO 'Meal Plan' (day, meal) VALUES (?,?)", (day,""))
                self.connector.commit()
                print("Meal Plan table created")
                return None
            except sqlite3.OperationalError:
                return ("Meal Plan table already exists")
            except Exception as e:
                return e
                print(f"OperationalError: {e}")

    def Ingredient_exist_check(self,table, column, value, ID_column):

        exist_check = f'SELECT EXISTS (SELECT 1 FROM "{table}" WHERE "{column}" = ?)'
        self.cursor.execute(exist_check,(value,))
        exists, = self.cursor.fetchone()
        if bool(exists):
            value_ID = f'SELECT "{ID_column}" FROM "{table}" WHERE "{column}" = ?'
            self.cursor.execute(value_ID,(value,))
            value_ID = self.cursor.fetchone()
            return value_ID[0]
        else:
            add_ingredient = f'INSERT INTO "{table}" ({column}) VALUES (?)'
            self.cursor.execute(add_ingredient,(value,))
            self.connector.commit()
            value_ID = f'SELECT "{ID_column}" FROM "{table}" WHERE "{column}" = ?'
        
            self.cursor.execute(value_ID,(value,))
            value_ID = self.cursor.fetchone()
            return value_ID[0]
    
    def check_recipie_input(self):
        while True:
            recipie_name = str(input("Please enter the recipie: "))
            if 0 < len(recipie_name) <= 40:
                return recipie_name
            else:
                print("The input is limited to 40 characters. Please Reneter")

    def check_ingredient_input(self):
        while True:
            ingredient = str(input("Please enter the ingredient: "))
            if 0 < len(ingredient) <= 20:
                return ingredient
            else:
                print("The input is limited to 20 characters. Please Reneter")
    
    def check_quantity_input(self):
        while True:
            Quant = float(input("Please enter the Quantity: "))
            if type(Quant) == float and 0 < Quant <= 2000  :
                return Quant
            else:
                print("Only enter an interger below 2000")


    def add_recipie(self, Recipie):
        print("Type Break into the console to stop the code running")
        while True:
            
            ing = self.check_ingredient_input()
            value_ID = self.Ingredient_exist_check(table = "Ingredients", column = "Ingredient", value = ing, ID_column='Ing_ID')
            if ing == "Break":
                break
            

                
            quant = self.check_quantity_input()
            if quant == "Break":
                break

                
            add_recipie_row = f'INSERT INTO "{Recipie}" (Ingredient, quantity, Ing_ID) VALUES (?,?,?)'
            try:
                self.cursor.execute(add_recipie_row,(ing, quant, value_ID))
                self.connector.commit()
            except sqlite3.IntegrityError:
                print(ing + " is already in list, please add another ingredient")
            except Exception as e:
                print(f"OperationalError: {e}")
    
    def view_recipie(self, Recipie):
        while True:
            try:
                view_Recipie = f'SELECT Ingredient, quantity, Ing_ID FROM "{Recipie}"'
                self.cursor.execute(view_Recipie)
                view_Recipie = self.cursor.fetchall()
                Table = [["Ingredient","Quantity","ID"]]
                for row in view_Recipie:
                    Table.append(row)
                print(tabulate(Table, headers='firstrow', tablefmt='fancy_grid'))
                return
            except sqlite3.IntegrityError:
                print("Recipie: " + Recipie + "does not exist. Please renter")
            except Exception as e:
                print(f"OperationalError: {e}")

    def view_all_tables(self,table):
        try:
            view_all_tables = f'SELECT Recipie FROM "{table}"'
            self.cursor.execute(view_all_tables)
            view_all_tables = self.cursor.fetchall()
            print("Debug: Retrieved tables:", view_all_tables)
            Table_table = [["Recipies"]]
            for row in view_all_tables:
                Table_table.append(row)
            print(tabulate(Table_table, headers='firstrow', tablefmt='fancy_grid'))
        except Exception as e:
            print(f"OperationalError: {e}")
    
    def select_table_to_view(self,table):
        self.active_table = table
        return table
    
    
    
    def check_int_input(self):
        while True:
            selection_int = int(input("Please enter the number: "))
            if type(selection_int) == int and 0 < selection_int <= 10  :
                return selection_int
            else:
                print("Please Type a number under 10")
    
    def exit_table(self):
        self.active_table = None

    def edit_recipie_ingredient(self):
        select_ingredient = input("Which ingredient would you like to edit?")
        find_ingredient = f'SELECT * FROM "{self.active_table}" WHERE Ingredient = ?'
        self.cursor.execute(find_ingredient,(select_ingredient,))
        old_values = self.cursor.fetchall()
        table_table = [["Ingredient","Quantity","ID"],old_values]
        print(tabulate(table_table, headers='firstrow', tablefmt='fancy_grid'))
        print("Please enter new values")
        new_ing = self.check_ingredient_input()
        new_quant = self.check_quantity_input()
        
        try:
            update_table = f'UPDATE "{self.active_table}" SET Ingredient = ?, quantity = ?, Ing_ID = ? Where Ingredient = ? '
            new_ID = self.Ingredient_exist_check(table = "Ingredients", column= "Ingredient" , value= new_ing)
            self.cursor.execute(update_table,(new_ing, new_quant, new_ID, select_ingredient))
        except Exception as e:
            print(f"OperationalError: {e}")
            
    def remove_row(self,table, column, value):
        while True:
            try:
                delete_row = f'DELETE from "{table}" where "{column}" = ?'
                self.cursor.execute(delete_row,(value,))
                self.connector.commit()
                print("Row " + value + " has been deleted")
                return
            except sqlite3.OperationalError:
                print ("This was not in the list")
                return

    def drop_table(self, table_to_drop):
        while True:
            try:
                drop_table = f'DROP TABLE "{table_to_drop}"'
                self.cursor.execute(drop_table)
                self.connector.commit()
                print("Table " + table_to_drop + " has been dropped")
                return
            except sqlite3.OperationalError:
                print ("This table does not exist")
                return
            except Exception as e:
                print(f"OperationalError: {e}")
                return e
                
    
    def view_and_edit_table(self,table):
        self.active_table = table
        while True:
            print("Now Showing: " + self.active_table)
            self.view_recipie(Recipie= self.active_table)
            print("Please select one of the following options:")
            print("1.Edit Ingredient")
            print("2.Remove Ingredient")
            print("3.Add Ingredient")
            print("4.Return to Menu")
            while True:
                selection_int = self.check_int_input()
                if  selection_int == 4:
                    self.exit_table()
                    return
                elif selection_int == 1:
                    self.edit_recipie_ingredient()
                    break
                elif selection_int == 2:
                    ing_delete = self.check_ingredient_input()
                    self.remove_row(table=self.active_table, column= "Ingredients", value=ing_delete)
                    break
                elif selection_int == 3:
                    self.add_recipie(Recipie=self.active_table)
                    break

    
    def view_meal_plan(self):
        while True:
            try:
                view_meal_plan = f"SELECT day, meal FROM 'Meal Plan'"
                self.cursor.execute(view_meal_plan)
                view_meal_plan = self.cursor.fetchall()
                Table = [["Day Of the Week","Meal"]]
                for row in view_meal_plan:
                    Table.append(row)
                print(tabulate(Table, headers='firstrow', tablefmt='fancy_grid'))
                return
            except sqlite3.IntegrityError:
                print("Meal Plan does not exist")
            except Exception as e:
                print(f"OperationalError: {e}")

    def edit_meal_plan(self):
        select_day = input("Which Day would you like to edit?")
        find_day = f"SELECT * FROM 'Meal Plan' WHERE day = ?"
        self.cursor.execute(find_day,(select_day,))
        old_values = self.cursor.fetchall()
        table_table = [["Day","Meal"],old_values]
        print(tabulate(table_table, headers='firstrow', tablefmt='fancy_grid'))
        print("Please enter new values")
        new_meal = self.check_recipie_input()
        print(new_meal, select_day)
        try:
            update_table = f"UPDATE 'Meal Plan' SET meal = ? Where day = ? "
            self.cursor.execute(update_table,(new_meal, select_day))
            self.connector.commit()
            print ("Table updated")
        except Exception as e:
            print(f"OperationalError: {e}")

    def view_and_edit_meal_plan(self,table):
        self.active_table = table
        while True:
            print("Now Showing: " + self.active_table)
            self.view_meal_plan()
            print("Please select one of the following options:")
            print("1.Edit Meal")
            print("2.Return to Menu")
            while True:
                selection_int = self.check_int_input()
                if  selection_int == 2:
                    self.exit_table()
                    return
                elif selection_int == 1:
                    self.edit_meal_plan()
                    break     
    def add_row(self,table,column, column2,column_value, column2_value):
        add_row_sql = f'INSERT INTO "{table}" ("{column}", "{column2}") VALUES (?,?)'
        self.cursor.execute(add_row_sql,(column_value,column2_value))

    def check_ing_in_shopping_list(self,ingredient,table):
        check_ingredient = f'SELECT EXISTS (SELECT 1 FROM "{table}" WHERE "{ingredient}" = ?)'
        self.cursor.execute(check_ingredient,(ingredient,))
        exists, = self.cursor.fetchone()
        if bool(exists):
            return True
        else:
            return False

    
    def combine_ingredients(self,meal_plan_table,shopping_list_table):
        meal_plan = f'SELECT meal FROM "{meal_plan_table}"'
        self.cursor.execute(meal_plan)
        meal_plan = self.cursor.fetchall()
        for row in meal_plan:
            find_recipie_table = f'SELECT Ingredient, Quantity FROM "{row[0]}"'
            self.cursor.execute(find_recipie_table)
            find_recipie_table = self.cursor.fetchall()
            for rows in find_recipie_table:
                print(rows)
                ingredient_to_add = rows[0]
                quantity_to_add = int(rows[1])
                print(quantity_to_add)
                exists = self.check_ing_in_shopping_list(ingredient=ingredient_to_add, table=shopping_list_table)
                if exists == True:
                    old_quant = self.cursor.execute(f'SELECT Quantity FROM "{shopping_list_table}" WHERE Ingredient = "{ingredient_to_add}"')
                    old_quant = old_quant.fetchone()
                    for row in old_quant:
                        print(row)
                    old_quant = int(old_quant[0])
                    quantity_to_add = old_quant + quantity_to_add
                    print(quantity_to_add)

                    
                    find_ingredient = f'UPDATE "{shopping_list_table}" SET quantity = ? '
                if exists == False:
                    self.add_row(table=shopping_list_table,column="Ingredient", column2= "Quantity", column_value=ingredient_to_add, column2_value=quantity_to_add)



        
        

    def Main_code(self):
        self.Create_Ingredients_Table()
        self.Create_Mealplan_table()
        self.create_all_recipies()
        self.create_shopping_list()
        while True:
            self.view_all_tables(table= "All Recipies")
            print("Please select from the following options:")
            print("1. View and Edit Recipie")
            print("2. View and Edit this weeks meal plan")
            print("3. Create a custom shopping list for this week")
            print("4. Add a new recipie")
            print("5. Delete Recipie")
            print("6. Save and Exit")

            while True:
                response = self.check_int_input()
                if response == 1:
                    recipie_name = input("Recipie: ") 
                    if recipie_name == "Meal Plan":
                        print("To View the Meal Plan table please select option 2")
                        break  
                    self.view_and_edit_table(table=recipie_name)
                    break
                elif response == 4:
                    Recipie_input = self.check_recipie_input()
                    self.Ingredient_exist_check(table='All Recipies', column= "Recipie", value=Recipie_input,ID_column= 'Recipie_ID')
                    self.Create_Tables(Recipie= Recipie_input)
                    self.add_recipie(Recipie= Recipie_input)
                    break
                elif response == 2:
                    self.view_and_edit_meal_plan(table='Meal Plan')
                    break
                elif response == 3:
                    self.combine_ingredients(meal_plan_table='Meal Plan',shopping_list_table='Shopping List')
                    break
                elif response == 6:
                    self.connector.commit()
                    return
                elif response == 5:
                    
                    drop_table = self.check_recipie_input()
                    self.remove_row(table='All Recipies',column='Recipie',value=drop_table)
                    self.drop_table(table_to_drop=drop_table)
                    break
        



Shopping_list().Main_code()


