import sqlite3


class Shopping_list:
    def __init__(self):
        self.connector = sqlite3.connect("Shopping List.db")
        self.cursor = self.connector.cursor()


    def Create_Tables(self,Recipie):
        try:
            self.cursor.execute(f"CREATE TABLE {Recipie} (Ingredient TEXT PRIMARY KEY, Ing_ID int NOT NULL, quantity int NOT NULL)")
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

                

    def add_recipie(self, Recipie):
        while True:
            print("Type Break into the console to stop the code running")
            
            ing = input("Please Enter the Ingredient")
            value_ID = self.Ingredient_exist_check(table = "Ingredients", column = "Ingredient", value = ing)
            print(value_ID)
            if ing == "Break":
                break
            

                
            quant = input("Please enter the quantity of " + ing)
            if quant == "Break":
                break

                
            add_recipie_row = f"INSERT INTO {Recipie}(Ingredient, Ing_ID, quantity) VALUES (?,?,?)"
            try:
                self.cursor.execute(add_recipie_row,(ing,value_ID, quant))
                self.connector.commit()
            except sqlite3.IntegrityError:
                print(ing + " is already in list, please add another ingredient")
            except Exception as e:
                print(f"OperationalError: {e}")


        
Shopping_list().Create_Ingredients_Table()
Shopping_list().Create_Tables(Recipie= "test")

Shopping_list().add_recipie(Recipie="test")






