import sqlite3
from tabulate import tabulate


class ShoppingList:
    def __init__(self):
        self.connector = sqlite3.connect("Shopping List.db")
        self.cursor = self.connector.cursor()
        self.active_table = None

    def create_table(self, table_name, params, insert_rows = None):

        """This is a helper function that creates a table with given parameters if it exists. If initial rows need to be filled in then it does that too"""
        try:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}"({params})')
            if insert_rows:
                dynamic_question_marks = ','.join(['?'] * len(insert_rows[0]))
                for row in insert_rows:
                    self.cursor.execute(f'INSERT OR IGNORE INTO "{table_name}" VALUES ({dynamic_question_marks})',row)
                self.connector.commit()
                print(f'Table "{table_name}" created or already exists')
        except Exception as e:
            print(f'Error while creating table"{table_name}":{e}')
        except sqlite3.OperationalError as oe:
            print(f'OperartionalError while creating table "{table_name}":{oe}')
        except sqlite3.IntegrityError as ie:
            print(f'IntegrityError while creating table "{table_name}":{ie}')
        except sqlite3.ProgrammingError as pe:
            print(f'ProgrammingError while creating table "{table_name}":{pe}')

    def create_key_tables(self):
        self.create_table(table_name="Ingredients",params= "Ingredient char(20) PRIMARY KEY, Quantity INT NOT NULL, unit TEXT NOT NULL")
        self.create_table(table_name="All Recipes", params="Recipe char(40) NOT NULL PRIMARY KEY, Portions INT NOT NULL")
        self.create_table(table_name="Shopping List", params="Ingredient char(20) PRIMARY KEY, Quantity INT NOT NULL, unit TEXT NOT NULL")
        self.create_table(table_name="Meal Plan", params="day TEXT NOT NULL PRIMARY KEY, meal TEXT NOT NULL",insert_rows=("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"))

    def ingredient_exist_check(self, table, column, value, id_column):

        """This is a helper function that checks if an value is in a table and returns a unique ID code if so. If not it adds it to the table and returns the new ID"""
        try:
            self.cursor.execute(f'SELECT "{id_column}" FROM "{table}" WHERE "{column}" = ?', (value,))
            row =self.cursor.fetchone()
            if row:
                return row[0]
            self.cursor.execute(f'INSERT INTO "{table}" ("{column}") VALUES (?)',(value,))
            self.connector.commit()
            self.cursor.execute(f'SELECT "{id_column}" FROM "{table}" WHERE "{column}" = ?',(value,))
            row  = self.cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print(f'Error in ingredients_self_check: {e}')
            return None
        
    def check_input(self, prompt, validity_check, error_message):
        while True:
            try:
                user_input = input(prompt)
                if validity_check(user_input):
                    return input
                else:
                    print(error_message)
            except (EOFError, KeyboardInterrupt):
                print("\nInput cancelled. Please try again.")
            except Exception as e:
                print(f"Unexpected error: {e}. Please try again.")

    def valid_units(self, unit):
        units = ("g","kg","ml","l","tsp","tbsp", "")
        if unit in units: 
            return True
        else:
            return False
    def valid_days(self, day):
        days_of_the_week = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        if day in days_of_the_week:
            return True
        else
            return False
        
    def insert_row(self,table ,columns, values):
        values_placeholders = ','.join(['?']) * len(values)
        columns_string = ', '.join(columns)
        try:
            self.cursor.execute(f'INSERT INTO "{table}" ({columns_string}) VALUES ({values_placeholders})', (values,))
            self.connector.commit()
            return True
        except sqlite3.IntegrityError as ie:
            print(f"Integrity error: {ie}")
            return False
        except sqlite3.OperationalError as oe:
            print(f"Operational error: {oe}")
        except Exception as e:
            print(f"Unexpected error {e}")

    def add_ingredient_to_recipe(self, recipe, columns):
        """This function adds an ingredient to a recipe"""
        print("Please enter 'break' to exit the function")
        while True:
            ing = self.check_input("Enter the name of the ingredient: ",lambda x: 0 < len(x) < 20 and isinstance(x,str), "Invalid input. Please enter a valid ingredient name.")
            if ing.strip().lower() == "break":
                break
            quantity = self.check_input("Enter the quantity of the ingredient: ", lambda x: (0 < x < 20) or x.strip().lower() == 'break', "Invalid input. Please enter a valid number")
            if quantity == "break":
                break
            units = self.check_input("Enter the unit of the ingredient. Leave empty if it is unitless: ", lambda x: x.strip().lower() == "break" or self.valid_units(unit= x), "Invalid input, please enter one of the following: g, kg, ml, l, tsp, tbsp")
            ing_id = self.ingredient_exist_check(table="Ingredients",column="Ingredient", value = ing, ID_column='Ing_ID')
            add_row = self.insert_row(table=recipe, columns=columns, values=(ing,quantity,units,ing_id))
    
    def view_table(self, table, columns, headers):
        try:
            view_table = self.cursor.execute(f'SELECT {columns} FROM "{table}"').fetchall()
            display_table = [[headers]]
            for row in view_table:
                display_table.append(row)
            print(tabulate(display_table, headers= 'firstrow', tablefmt='fancy_grid'))
            return True
        except sqlite3.IntegrityError as ie:
            print(f"IntegrityError detectde: {ie}")
            return False
        except sqlite3.OperationalError as oe:
            print(f"OperationalError detected: {oe}")
            return False
        except Exception as e:
            print(f"Unexpected error {e}")
            return False

    def update_row(self, table, set_column, set_values, where_column, where_value):
        set_column_sql = ', '.join([f"{col} = ?" for col in set_column])
        update_statment = f'UPDATE "{table}" SET {set_column_sql} WHERE {where_column} = ?'
        try:
            self.cursor.execute(update_statment,(*set_values, where_value))
            self.connector.commit()
            print("Row has been updated")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def drop_table(self, table_to_drop):
        while True:
            try:
                drop_table = f'DROP TABLE "{table_to_drop}"'
                self.cursor.execute(drop_table)
                self.connector.commit()
                print("Table " + table_to_drop + " has been DELETED")
                return
            except sqlite3.OperationalError:
                print ("This table does not exist")
                return
            except Exception as e:
                print(f"OperationalError: {e}")
                return e
            except (EOFError, KeyboardInterrupt):
                print("\nInput cancelled. Please try again.")
    
    def edit_meal_plan(self, table, columns)
        
        try:
            select_day = self.check_input(prompt= f"Enter the day you want to edit", validity_check= lambda x:self.valid_days(day = select_day) or select_day.strip().lower() = "break", error_message= f"Invalid input, please enter a day of the week")
            select_meal = self.check_input(prompt= f"Please enter the meal you would like on this day : {select_day}", validity_check= lambda x: 0 < len(x) < 40 and isinstance(x,str), error_message= "Please input a valid recpie" )
            self.update_row(table= table, set_column= columns, set_values= select_meal, where_column= columns, where_value=select_day)
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Please try again.")
            return        

    def view_and_edit_meal_plan(self, table):
        while True:
            self.view_table(table=table, columns=("Day","Meal"), headers=["Day", "Meal"])
            print("Please select one of the following options:\n1.Edit Meal\n2.Return to Menu")
            while True:
                selection_int = self.check_input(prompt="Please enter the number of the option you would like to select", validity_check= lambda x: 0 < x < 2 and isinstance(x,float), error_message="Please input a valid number")
                if selection_int == 2:
                    return
                if selection_int == 1:
                    self.edit_meal_plan(table=table)
                    break
    def check_value_in_table(self, table, column, value):
        check_value = self.cursor.execute(f'SELECT EXISTS (SELECT 1 FROM "{table}" WHERE {column} = ?)',(value,))
        exists, = self.cursor.fetchone()
        if bool(exists):
            return True
        else:
            return False
    
    def clear_table(self, table):
        try:
            self.cursor.execute(f'DELETE FROM "{table_name}"')
            self.connector.commit()
            print(f"Table cleared")
        except Exception as e:
            print(f"Operational error: {e}")

    def main_code(self):
        self.create_key_tables
        while True:
            self.view_table(table="All Recipes", columns=("recipe","portion"),headers=["Recipe","Portion"] )

    
