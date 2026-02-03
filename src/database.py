import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class FamilyDB:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if url and key:
            self.supabase: Client = create_client(url, key)
        else:
            st.error("Config supabase manquante dans les Secrets !")

    # --- LISTE DE COURSES ---
    def add_shopping_item(self, item, list_category):
        self.supabase.table("shopping_list").insert({"item": item, "list_category": list_category}).execute()

    def remove_shopping_item(self, item_id):
        self.supabase.table("shopping_list").delete().eq("item_id", item_id).execute()

    def get_shopping_list(self):
        res = self.supabase.table("shopping_list").select("*").execute()
        return res.data

    # --- TÂCHES ---
    def add_task(self, title, assignee, creator):
        self.supabase.table("tasks").insert({
            "title": title, "assignee": assignee, 
            "created_by": creator, "done": False
        }).execute()

    def remove_task(self, task_id):
        self.supabase.table("tasks").delete().eq("task_id", task_id).execute()

    def get_tasks(self):
        res = self.supabase.table("tasks").select("*").execute()
        return [(t['task_id'], t['title'], t['assignee'], t['done'], t['created_by']) for t in res.data]

    def toggle_task_status(self, task_id, current_status):
        self.supabase.table("tasks").update({"done": not current_status}).eq("task_id", task_id).execute()

    # --- NOTES ---
    def add_note(self, content, author):
        self.supabase.table("notes").insert({"content": content, "author": author}).execute()

    def get_notes(self):
        res = self.supabase.table("notes").select("*").order("created_at", desc=True).execute()
        return [(n['note_id'], n['content'], n['created_at'], n.get('author', 'Anonyme'), n.get('read_by', [])) for n in res.data]

    def mark_note_as_read(self, note_id, user_name):
        res = self.supabase.table("notes").select("read_by").eq("note_id", note_id).execute()
        if res.data:
            current_readers = res.data[0].get('read_by')
            if current_readers is None:
                current_readers = []
            if user_name not in current_readers:
                current_readers.append(user_name)
                self.supabase.table("notes").update({"read_by": current_readers}).eq("note_id", note_id).execute()


    def delete_note(self, note_id):
        self.supabase.table("notes").delete().eq("note_id", note_id).execute()

    # --- ANNIVERSAIRES ---
    def add_birthday(self, name, date_str):
        self.supabase.table("birthdays").insert({"name": name, "date": date_str}).execute()

    def get_birthdays(self):
        res = self.supabase.table("birthdays").select("*").order("date").execute()
        return [(b['birthday_id'], b['name'], b['date']) for b in res.data]

    def remove_birthday(self, birthday_id):
        self.supabase.table("birthdays").delete().eq("birthday_id", birthday_id).execute()

    # --- MENU DE LA SEMAINE (Rétabli) ---
    def add_menu_item(self, day, meal_type, dish):
        self.supabase.table("weekly_menu").insert({
            "day": day, "meal_type": meal_type, "dish": dish
        }).execute()

    def get_menu(self):
        res = self.supabase.table("weekly_menu").select("*").execute()
        return res.data

    def clear_menu_item(self, item_id):
        # Vérifie si ta colonne s'appelle item_id ou menu_id dans Supabase
        self.supabase.table("weekly_menu").delete().eq("item_id", item_id).execute()

    # --- AMÉLIORATIONS / UPGRADES (Rétabli) ---
    def add_upgrade(self, upgrade_name):
        self.supabase.table("upgrades").insert({"upgrade_name": upgrade_name}).execute()

    def remove_upgrade(self, upgrade_id):
        self.supabase.table("upgrades").delete().eq("upgrade_id", upgrade_id).execute()

    def get_upgrades(self):
        res = self.supabase.table("upgrades").select("*").execute()
        return [(i['upgrade_id'], i['upgrade_name']) for i in res.data]

@st.cache_resource
def get_db():
    return FamilyDB()