import sqlite3
import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class FamilyDB:

# Initialisation de la base
#----------------------------------------------------------------------------------------
    def __init__(self, db_path="app_maison.db"):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if url and key:
            self.supabase: Client = create_client(url, key)
        else:
            st.error("Config supabase manquante dans le .env !")

# Gestion de la liste de course
#----------------------------------------------------------------------------------------
    def add_shopping_item(self,item):
        self.supabase.table("shopping_list").insert({"item": item}).execute()

    def remove_shopping_item(self,item_id):
        self.supabase.table("shopping_list").delete().eq("item_id", item_id).execute()

    def get_shopping_list(self):
        res = self.supabase.table("shopping_list").select("*").execute()
        return[(i['item_id'], i['item']) for i in res.data]

    # Gestion des tâches
    #---------------------------------------------------------------------------------------- 
    def add_task(self, title, assignee):
        self.supabase.table("tasks").insert({"title": title, "assignee": assignee}).execute()

    def remove_task(self, task_id):
        self.supabase.table("tasks").delete().eq("task_id", task_id).execute()

    def get_tasks(self):
        res = self.supabase.table("tasks").select("*").execute()
        return[(t['task_id'], t['title'], t['assignee'], t['done']) for t in res.data]

    def toggle_task_status(self, task_id, current_status):
        new_status = not current_status
        self.supabase.table("tasks").update({"done": new_status}).eq("task_id", task_id).execute()

    #Gestion des anniversaires
    #---------------------------------------------------------------------------------------- 
    def add_birthday(self, name, date_str):
        self.supabase.table("birthdays").insert({"name":name, "date":date_str}).execute()

    def get_birthdays(self):
        res = self.supabase.table("birthdays").select("*").order("date").execute()
        return [(b['birthday_id'], b['name'], b['date']) for b in res.data]
        
    #Gestion des notes
    #---------------------------------------------------------------------------------------- 
    def add_note(self, content):
        self.supabase.table("notes").insert({"content": content}).execute()

    def get_notes(self):
        res = self.supabase.table("notes").select("*").order("created_at", desc=True).execute()
        return [(n['note_id'], n['content'], n['created_at']) for n in res.data]
        
    def delete_note(self, note_id):
        self.supabase.table("notes").delete().eq("note_id", note_id).execute()

    # Gestion de la liste de course
    #----------------------------------------------------------------------------------------
    def add_upgrade(self,upgrade_name):
        self.supabase.table("shopping_list").insert({"upgrade_name": upgrade_name}).execute()

    def remove_upgrade(self,upgrade_id):
        self.supabase.table("upgrades").delete().eq("upgrade_id", upgrade_id).execute()

    def get_upgrades(self):
        res = self.supabase.table("upgrades").select("*").execute()
        return[(i['upgrade_id'], i['upgrade_name']) for i in res.data]
    

@st.cache_resource
def get_db():
    return FamilyDB()