import sqlite3

class FamilyDB:

# Initialisation de la base
#----------------------------------------------------------------------------------------
    def __init__(self, db_path="app_maison.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn : 
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    assignee TEXT NOT NULL,
                    done BOOLEAN DEFAULT 0
                )
            ''')
            # Table pour la liste de courses
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shopping_list (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT NOT NULL,
                    quantity INTEGER
                )
            ''')
            conn.commit()



# Gestion de la liste de course
#----------------------------------------------------------------------------------------
    def add_shopping_item(self,item,quantity):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO shopping_list (item, quantity) VALUES (?,?)",
                (item,quantity)
            )
            conn.commit()

    def remove_shopping_item(self,item_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM shopping_list WHERE item_id = ?", (item_id,))
            conn.commit()

    def get_shopping_list(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM shopping_list")
            return cursor.fetchall()



    # Gestion des tâches
    #---------------------------------------------------------------------------------------- 
    def add_task(self, title, assignee):
        with sqlite3.connect(self.db_path) as conn: 
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, assignee) VALUES (?,?)",
                (title, assignee)
            )
            conn.commit()

    def remove_task(self, task_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tasks WHERE task_id = ?",
                (task_id,)
            )
            conn.commit()

    def get_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            return cursor.fetchall()