import st
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class FamilyDB:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    # --- COURSES ---
    def add_shopping_item(self, item, list_category):
        self.supabase.table("shopping_list").insert({"item": item, "list_category": list_category}).execute()

    def remove_shopping_item(self, item_id):
        self.supabase.table("shopping_list").delete().eq("item_id", item_id).execute()

    def get_shopping_list(self):
        res = self.supabase.table("shopping_list").select("*").execute()
        return res.data

    # --- TÂCHES ---
    def add_task(self, title, assignee, creator):
        self.supabase.table("tasks").insert({"title": title, "assignee": assignee, "created_by": creator, "done": False}).execute()

    def get_tasks(self):
        res = self.supabase.table("tasks").select("*").execute()
        return [(t['task_id'], t['title'], t['assignee'], t['done'], t['created_by']) for t in res.data]

    def toggle_task_status(self, task_id, current_status):
        self.supabase.table("tasks").update({"done": not current_status}).eq("task_id", task_id).execute()

    # --- NOTES (Fix Unpacking image_6bcfa0.png) ---
    def get_notes(self):
        res = self.supabase.table("notes").select("*").order("created_at", desc=True).execute()
        # On renvoie bien 4 valeurs : ID, Contenu, Date, Auteur
        return [(n['note_id'], n['content'], n['created_at'], n.get('author', 'Anonyme')) for n in res.data]

    def delete_note(self, note_id):
        self.supabase.table("notes").delete().eq("note_id", note_id).execute()

    # --- MENU & UPGRADES (Rétabli) ---
    def get_menu(self):
        res = self.supabase.table("weekly_menu").select("*").execute()
        return res.data

    def get_upgrades(self):
        res = self.supabase.table("upgrades").select("*").execute()
        return [(i['upgrade_id'], i['upgrade_name']) for i in res.data]

    def get_birthdays(self):
        res = self.supabase.table("birthdays").select("*").order("date").execute()
        return [(b['birthday_id'], b['name'], b['date']) for b in res.data]

@st.cache_resource
def get_db():
    return FamilyDB()