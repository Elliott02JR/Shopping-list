import sqlite3
from tabulate import tabulate

class ShoppingList:
    def __init__(self):
        # Initialize the database connection and cursor
        self.connector = sqlite3.connect("Shopping List New.db")
        self.cursor = self.connector.cursor()
        self.active_table = None

    def create_table(self, table_name, params, insert_rows = None):
        """
        Creates a table with the specified name and parameters if it does not already exist.
        Optionally inserts initial rows if provided.
        """
        try:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}"({params})')
            if insert_rows:
                dynamic_question_marks = ','.join(['?'] * len(insert_rows[0]))
                for row in insert_rows:
                    self.cursor.execute(f'INSERT OR IGNORE INTO "{table_name}" VALUES ({dynamic_question_marks})',row)
                self.connector.commit()
                print(f'Table "{table_name}" created or already exists')
                return
        except Exception as e:
            print(f'Error while creating table"{table_name}":{e}')
            return
        except sqlite3.OperationalError as oe:
            print(f'OperartionalError while creating table "{table_name}":{oe}')
            return
        except sqlite3.IntegrityError as ie:
            print(f'IntegrityError while creating table "{table_name}":{ie}')
            return
        except sqlite3.ProgrammingError as pe:
            print(f'ProgrammingError while creating table "{table_name}":{pe}')
            return

    def create_key_tables(self):
        """
        Creates all the main tables required for the application.
        This centralizes table creation for easy maintenance and updates.
        """
        self.create_table(table_name="Ingredients",params= "Ingredient char(20) PRIMARY KEY, Quantity INT NOT NULL, unit TEXT NOT NULL")
        self.create_table(table_name="All Recipes", params="Recipe char(40) NOT NULL PRIMARY KEY, Portions INT NOT NULL")
        self.create_table(table_name="Shopping List", params="Ingredient char(20) PRIMARY KEY, Quantity INT NOT NULL, unit TEXT NOT NULL")
        self.create_table(
            table_name="Meal Plan",
            params="day TEXT NOT NULL PRIMARY KEY, meal TEXT NOT NULL",
            insert_rows=[("monday",""), ("tuesday",""), ("wednesday",""), ("thursday",""), ("friday",""), ("saturday",""), ("sunday","")]
        )
       
    def check_input(self, prompt, validity_check, error_message):
        """
        Prompts the user for input, validates it using the provided function, and handles errors.
        Returns the user input if valid, or 'break' if the user wishes to exit.
        """
        while True:
            try:
                user_input = input(prompt)
                if user_input.strip().lower() == "break":
                    return "break"
                if validity_check(user_input):
                    print(f"Debug: {user_input}")
                    return user_input
                else:
                    print(error_message)
            except (EOFError, KeyboardInterrupt):
                print("\nInput cancelled. Please try again.")
            except Exception as e:
                print(f"Unexpected error: {e}. Please try again.")

    def valid_units(self, unit):
        """
        Checks if the provided unit is in the list of accepted units.
        Returns True if valid, False otherwise.
        """
        units = ("g","kg","ml","l","tsp","tbsp", "")
        if unit in units: 
            return True
        else:
            return False

    def valid_days(self, day):
        """
        Checks if the provided day is a valid day of the week.
        Returns True if valid, False otherwise.
        """
        days_of_the_week = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        if day in days_of_the_week:
            return True
        else:
            return False
        
    def insert_row(self,table ,columns, values):
        """
        Inserts a row of data into the specified table.
        Columns and values should be tuples, allowing for flexible data insertion.
        """
        values_placeholders = ','.join(['?'] * len(values))
        columns_string = ', '.join(columns)
        try:
            self.cursor.execute(f'INSERT INTO "{table}" ({columns_string}) VALUES ({values_placeholders})', values)
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
        """
        Adds ingredients to a recipe table.
        Prompts the user for ingredient details and inserts them into the recipe table.
        """
        print("Please enter 'break' to exit the function")
        while True:
            ing = self.check_input("Enter the name of the ingredient: ",lambda x: 0 < len(x) < 20 and isinstance(x,str), "Invalid input. Please enter a valid ingredient name.")
            if ing.strip().lower() == "break":
                break
            quantity = self.check_input("Enter the quantity of the ingredient: ", lambda x: x.isdigit() and 0 < int(x) < 20 or x.lower().strip() == 'break', "Invalid input. Please enter a valid number")
            if quantity == "break":
                break
            else:
                quantity = int(quantity)
            units = self.check_input("Enter the unit of the ingredient. Leave empty if it is unitless: ", lambda x: x.strip().lower() == "break" or self.valid_units(unit= x), "Invalid input, please enter one of the following: g, kg, ml, l, tsp, tbsp")
            add_row = self.insert_row(table=recipe, columns=columns, values=(ing,quantity,units))
    
    def view_table(self, table, columns, headers):
        """
        Displays the contents of a table in a formatted grid using the tabulate library.
        Accepts the table name, columns to display, and header names.
        """
        try:
            if isinstance(columns, (tuple,list)):
                columns_str = ', '.join(columns)
            else:
                columns_str = columns
            view_table = self.cursor.execute(f'SELECT {columns_str} FROM "{table}"').fetchall()
            display_table = [headers]
            for row in view_table:
                display_table.append(row)
            print(tabulate(display_table, headers= 'firstrow', tablefmt='fancy_grid'))
            return True
        except sqlite3.IntegrityError as ie:
            print(f"IntegrityError detectde: {ie}")
            return
        except sqlite3.OperationalError as oe:
            print(f"OperationalError detected: {oe}")
            return
        except Exception as e:
            print(f"Unexpected error {e}")
            return

    def update_row(self, table, set_column, set_values, where_column, where_value):
        """
        Updates a row in the specified table.
        set_column and set_values are tuples for the columns and their new values.
        where_column and where_value specify which row to update.
        """
        set_column_sql = ', '.join([f"{col} = ?" for col in set_column])
        update_statment = f'UPDATE "{table}" SET {set_column_sql} WHERE {where_column} = ?'
        try:
            self.cursor.execute(update_statment,(*set_values, where_value))
            self.connector.commit()
            print("Row has been updated")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def remove_row(self, table,column, value):
        """
        Removes a row from the specified table where the column matches the given value.
        """
        try:
            self.cursor.execute(f'DELETE FROM "{table}" WHERE {column} = ?', (value,))
            self.connector.commit()
            print("Row has been deleted")
        except sqlite3.OperationalError as oe:
            print(f"OperationalError: {oe}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def drop_table(self, table_to_drop):
        """
        Drops (deletes) the specified table from the database.
        """
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
    
    def edit_meal_plan(self, table, column_meal, column_day):
        """
        Allows the user to edit the meal for a specific day in the meal plan.
        Prompts for the day and the new meal, then updates the table.
        """
        try:
            select_day = self.check_input(
                prompt= f"Enter the day you want to edit",
                validity_check= lambda x:self.valid_days(day = x.strip().lower()) or x.strip().lower() == "break",
                error_message= f"Invalid input, please enter a day of the week"
            )
            select_meal = self.check_input(
                prompt= f"Please enter the meal you would like on this day : {select_day}",
                validity_check= lambda x: 0 < len(x) < 40 and isinstance(x,str),
                error_message= "Please input a valid recpie"
            )
            self.update_row(
                table= table,
                set_column= (column_meal,),
                set_values= (select_meal,),
                where_column= column_day,
                where_value=select_day
            )
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Please try again.")
            return        

    def view_and_edit_recipe(self, table):
        """
        Allows the user to view and edit a recipe's ingredients.
        Provides options to edit, remove, or add ingredients.
        """
        while True:
            self.view_table(table= table, columns=("ingredient","Quantity","unit"),headers=["Ingredient","Quantity","Unit"])
            print("Please select one of the following options:\n1. Edit Ingredients\n2. Remove Ingredient\n3. Add Ingredient\n4. Return to menu")
            while True:
                selection_int = self.check_input(
                    prompt="Please enter the number of the option you would like to select",
                    validity_check= lambda x: x.isdigit() and 0 < int(x) <= 4,
                    error_message="Please input a valid number"
                )
                selection_int = int(selection_int)
                if selection_int == 4:
                    return
                elif selection_int == 1:
                    old_ing = self.check_input(
                        prompt="Please enter the name of the ingredient you would like to edit",
                        validity_check= lambda x: 0 < len(x) < 20 and isinstance(x,str),
                        error_message="Please enter a valid ingredient"
                    )
                    new_ing = self.check_input(
                        prompt="Please enter the new name of the ingredient",
                        validity_check= lambda x: 0 < len(x) < 20 and isinstance(x,str),
                        error_message="Please enter a valid ingredient"
                    )
                    new_quantity = self.check_input(
                        prompt="Please enter the new quantity of the ingredient",
                        validity_check= lambda x: x.isdigit() and 0 < int(x) < 2000,
                        error_message="Please enter a valid number"
                    )
                    self.update_row(
                        table= table,
                        set_column=("Ingredient","Quantity"),
                        set_values=(new_ing,new_quantity),
                        where_column="Ingredient",
                        where_value=old_ing
                    )
                elif selection_int == 2:
                    edit_ing = self.check_input(
                        prompt="Please enter the name of the ingredient you would like to remove",
                        validity_check= lambda x: 0 < len(x) < 20 and isinstance(x,str),
                        error_message="Please enter a valid ingredient"
                    )
                    self.remove_row(table=table,column='ingredient', value=edit_ing)
                    self.remove_row(table = table, column= 'ingredient',value=edit_ing)
                elif selection_int == 3:
                    self.add_ingredient_to_recipe(recipe=table, columns=("ingredient","quantity","unit"))

    def view_and_edit_meal_plan(self, table):
        """
        Allows the user to view and edit the weekly meal plan.
        Provides options to edit a meal or return to the menu.
        """
        while True:
            self.view_table(table=table, columns=("Day","Meal"), headers=["Day", "Meal"])
            print("Please select one of the following options:\n1.Edit Meal\n2.Return to Menu")
            while True:
                selection_int = self.check_input(
                    prompt="Please enter the number of the option you would like to select",
                    validity_check= lambda x: x.isdigit() and 0 < int(x) <= 2,
                    error_message="Please input a valid number"
                )
                selection_int = int(selection_int)
                if selection_int == 2:
                    return
                if selection_int == 1:
                    self.edit_meal_plan(table=table,column_day='day', column_meal= 'meal')
                    break

    def check_value_in_table(self, table, column, value):
        """
        Checks if a specific value exists in a given column of a table.
        Returns True if it exists, False otherwise.
        """
        self.cursor.execute(f'SELECT EXISTS (SELECT 1 FROM "{table}" WHERE {column} = ?)',(value,))
        return self.cursor.fetchone()[0] == 1
    
    def clear_table(self, table):
        """
        Deletes all rows from the specified table, but keeps the table structure.
        """
        try:
            self.cursor.execute(f'DELETE FROM "{table}"')
            self.connector.commit()
            print(f"Table cleared")
        except Exception as e:
            print(f"Operational error: {e}")

    def shopping_list(self):
        """
        Displays and manages the shopping list.
        Allows the user to create a new shopping list or return to the menu.
        """
        while True:
            self.view_table(table="Shopping List", columns=("Ingredient","Quantity","unit"),headers=["Ingredient","Quantity","Units"])
            print("Please select one of the following options:\n1. Create new shopping list\n2. Return to Menu")
            while True:
                selection_int = self.check_input(
                    prompt="Please enter the number of the option you would like to select",
                    validity_check= lambda x:x.isdigit() and 0 < int(x) <= 6,
                    error_message="Please input a valid number"
                )
                selection_int = int(selection_int)
                if selection_int == 1:
                    self.clear_table(table = 'Shopping List')
                    self.new_shopping_list(
                        meal_table='Meal Plan',
                        shopping_table='Shopping List',
                        recipe_table='All Recipes',
                        meal='meal',
                        ing='Ingredient',
                        quant='Quantity',
                        unit='unit',
                        portions='portions',
                        recipe='Recipe'
                    )
                    break
                if selection_int == 2:
                    return
                
    def check_value_in_table(self, table, column, value):
        """
        Checks if a value exists in a specific column of a table.
        Returns True if it exists, False otherwise.
        """
        self.cursor.execute(f'SELECT EXISTS (SELECT 1 FROM "{table}" WHERE {column} = ?)',(value,))
        return self.cursor.fetchone()[0] == 1
    
    def new_shopping_list(self,meal_table,shopping_table,recipe_table,meal,ing,quant,unit,portions,recipe):
        """
        Generates a new shopping list based on the current meal plan.
        Aggregates ingredients from all meals and updates the shopping list table.
        """
        meals = self.get_meal_from_plan(meal_table= meal_table, meal_column= meal)
        for row in meals:
            portion = self.get_portion_for_recipe(recipe_table=recipe_table,portion_column=portions,recipe_column=recipe,recipe_name=row)
            self.cursor.execute(f'SELECT {ing},{quant},{unit} FROM "{row}"')
            find_recipe_table = self.get_ingredients_for_recipe(table=row,ing_col= ing,quant_col=quant,unit_col=unit)
            for rows in find_recipe_table:
                ingredient_to_add = rows[0]
                quantity_to_add = float(rows[1])/portion
                new_unit = rows[2]
                self.add_or_update_shopping_list(
                    shopping_list_table=shopping_table,
                    quantity=quant,
                    ingredient=ing,
                    unit=unit,
                    ing_value=ingredient_to_add,
                    quant_value=quantity_to_add,
                    unit_value=new_unit
                )
        self.connector.commit()

    def get_meal_from_plan(self, meal_table, meal_column):
        """
        Retrieves all meals from the meal plan table.
        Returns a list of meal names.
        """
        self.cursor.execute(f'SELECT {meal_column} FROM "{meal_table}"')
        return [row[0] for row in self.cursor.fetchall() if row[0]]

    def get_portion_for_recipe(self, recipe_table, portion_column, recipe_column,recipe_name):
        """
        Retrieves the number of portions for a given recipe.
        Returns the portion count as a float, or 1.0 if not found.
        """
        self.cursor.execute(f'SELECT {portion_column} FROM "{recipe_table}" WHERE {recipe_column} = ?',(recipe_name,))
        portion = self.cursor.fetchone()
        return float(portion[0]) if portion else 1.0

    def get_ingredients_for_recipe(self, table, ing_col, quant_col, unit_col):
        """
        Retrieves all ingredients, quantities, and units for a given recipe table.
        Returns a list of tuples.
        """
        self.cursor.execute(f'SELECT {ing_col},{quant_col},{unit_col} FROM "{table}"')
        return self.cursor.fetchall()

    def add_or_update_shopping_list(self,shopping_list_table,quantity,ingredient,unit, ing_value,quant_value,unit_value):
        """
        Adds a new ingredient to the shopping list or updates the quantity if it already exists.
        """
        ing_value = ing_value.strip().lower()
        self.cursor.execute(f'UPDATE "{shopping_list_table}" SET {quantity} = {quantity} + ? WHERE {ingredient} = ?',(quant_value,ing_value))
        if self.cursor.rowcount == 0:
            try:
                self.insert_row(table=shopping_list_table,columns=(ingredient,quantity,unit),values=(ing_value,quant_value,unit_value))
            except sqlite3.IntegrityError:
                print(f'Ingredient "{ing_value}" already exists in Shopping List')
            
    def new_recipe(self):
        """
        Guides the user through creating a new recipe, including its name, portions, and ingredients.
        """
        recipie_name = self.check_input(
            prompt="Please enter the recipie name.",
            validity_check=lambda x: 0 < len(x) < 20,
            error_message="Please enter a valid recipie"
        )
        portions = self.check_input(
            prompt="Please enter the number of portions this recipie makes",
            validity_check= lambda x: x.isdigit() and 0 < int(x) < 10,
            error_message="Please enter a valid number"
        )
        portions = int(portions)
        self.insert_row(table="All Recipes", columns=("Recipe", "Portions"),values=(recipie_name,portions))
        self.create_table(table_name=recipie_name,params="ingredient TEXT PRIMARY KEY, quantity int NOT NULL, unit TEXT NOT NULL",insert_rows= False)
        self.add_ingredient_to_recipe(recipe=recipie_name, columns=("ingredient","quantity","unit"))
    
    def main_code(self):
        """
        Main loop for the application.
        Displays the main menu and handles user navigation and actions.
        """
        self.create_key_tables()
        while True:
            self.view_table(table="All Recipes", columns=("Recipe", "Portions"), headers=["Recipe","Portion"])
            print("Please select one of the following options:\n1. View and Edit Recipie\n2. View and Edit this weeks meal plan\n3. Create and view a custom shopping list for this week\n4. Add a new recipie\n5. Delete Recipie\n6. Save and Exit")
            while True:
                selection_int = self.check_input(
                    prompt="Please enter the number of the option you would like to select",
                    validity_check= lambda x: x.isdigit() and 0 < int(x) <= 6,
                    error_message="Please input a valid number"
                )
                selection_int = int(selection_int)
                if selection_int == 1:
                    recipie_name = self.check_input(
                        prompt="Please enter the recipie you would like to view and edit.",
                        validity_check=lambda x: 0 < len(x) < 20,
                        error_message="Please enter a valid recipie"
                    )
                    self.view_and_edit_recipe(table=recipie_name)
                    break
                elif selection_int == 2:
                    self.view_and_edit_meal_plan(table= "Meal Plan")
                    break
                elif selection_int == 3:
                    self.shopping_list()
                    break
                elif selection_int == 4:
                    self.new_recipe()
                    break
                elif selection_int == 5:
                    recipie_name = self.check_input(
                        prompt="Please enter the recipie you would like to drop",
                        validity_check=lambda x: 0 < len(x) < 20,
                        error_message="Please enter a valid recipie"
                    )
                    self.drop_table(table_to_drop=recipie_name)
                    self.remove_row(table = 'All Recipes',column= 'Recipe',value=recipie_name)
                    break
                elif selection_int == 6:
                    self.connector.commit()
                    return

ShoppingList().main_code()
