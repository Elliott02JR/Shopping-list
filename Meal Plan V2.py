import sqlite3
from tabulate import tabulate


class shopping_list
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
                input = input(prompt)
                if validity_check(input):
                    return input
                else:
                    print(error_message)
            except (EOFError, KeyboardInterrupt):
                print("\nInput cancelled. Please try again.")
            except Exception as e:
                print(f"Unexpected error: {e}. Please try again.")
