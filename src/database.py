import sqlite3
import streamlit as st

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
                    item TEXT NOT NULL
                )
            ''')
            #Table pour les anniversaires
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS birthdays (
                    birthday_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            ''')
            # Table pour les notes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()



# Gestion de la liste de course
#----------------------------------------------------------------------------------------
    def add_shopping_item(self,item):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO shopping_list (item) VALUES (?)",
                (item,)
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
                [task_id]
            )
            conn.commit()

    def get_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            return cursor.fetchall()

    def toggle_task_status(self, task_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET done = 1 WHERE task_id = ?",
                [task_id]
            )
            conn.commit()






    #Gestion des anniversaires
    #---------------------------------------------------------------------------------------- 
    def add_birthday(self, name, date_str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO birthdays (name, date) VALUES (?,?)", [name,date_str])
            conn.commit()

    def get_birthdays(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM birthdays ORDER BY date ASC")
            return cursor.fetchall()
        

    #Gestion des notes
    #---------------------------------------------------------------------------------------- 
    def add_note(self, content):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO notes (content) VALUES (?)", [content])
            conn.commit()

    def get_notes(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
            return cursor.fetchall()
        
    def delete_note(self, note_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM notes where note_id = ?", [note_id])
            conn.commit()
            


@st.cache_resource
def get_db():
    return FamilyDB()