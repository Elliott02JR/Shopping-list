import sqlite3


class Shopping_list:
    def __init__(self):
        self.connector = sqlite3.connect("Shopping List.db")
        self.cursor = self.connector.cursor()

    def Create_Tables(self,Recipie):
        try:
            self.cursor.execute(f"CREATE TABLE {Recipie} (Ingredient char(20) PRIMARY KEY, quantity int NOT NULL)")
            return None
        except sqlite3.OperationalError:
            return ("Recipie Already Exists")
        except Exception as e:
            return e
    
    
    def Create_Ingredients_Table(self):
        try:
            self.cursor.execute(f"CREATE TABLE Ingredients (Ing_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, Ingredient char(20) NOT NULL)")
            return None
        except sqlite3.OperationalError:
            return ("Ingredients table already exists")
        except Exception as e:
            return e
        
    def Ingredient_exist_check(self,,table, column, value):

        exist_check = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {column} = ?)"
        self.cursor.execute(exist_check,(value,))
        exists, = self.cursor.fetchone()
        return bool(exists)

    def add_recipie(self, Recipie):
        while True:
            print("Type Break into the console to stop the code running")
            ing = input("Please Enter the Ingredient")
            if ing == "Break":
                break
            else:
                

                
            quant = input("Please enter the quantity of " + ing)
            if quant == "Break":
                break

                
            add_recipie_row = f"INSERT INTO {Recipie}(Ingredient, quantity) VALUES (?,?)"
            try:
                self.cursor.execute(add_recipie_row,(ing,quant))
                self.connector.commit
            except sqlite3.IntegrityError:
                print("{ing} is already in list, please add another ingredient")
            except Exception as e:
                print("Failed to add items")


        

Shopping_list().Create_Tables(Recipie= "test")
Shopping_list().add_recipie(Recipie="test")





