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
            
                
