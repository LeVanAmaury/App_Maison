import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class FamilyDB:
    """Class to handle all Supabase database operations for the family hub."""
    
    def __init__(self):
        # Prefer st.secrets if running in Streamlit Cloud, otherwise os.environ
        url = st.secrets.get("SUPABASE_URL") if "SUPABASE_URL" in st.secrets else os.environ.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY") if "SUPABASE_KEY" in st.secrets else os.environ.get("SUPABASE_KEY")
        
        if url and key:
            try:
                self.supabase: Client = create_client(url, key)
            except Exception as e:
                st.error(f"Erreur de connexion à Supabase : {e}")
        else:
            st.error("Configuration Supabase manquante (URL/Key) !")

    # --- SHOPPING LIST ---
    def add_shopping_item(self, item, list_category):
        return self.supabase.table("shopping_list").insert({"item": item, "list_category": list_category}).execute()

    def remove_shopping_item(self, item_id):
        return self.supabase.table("shopping_list").delete().eq("item_id", item_id).execute()

    def get_shopping_list(self):
        res = self.supabase.table("shopping_list").select("*").execute()
        return res.data

    # --- TASKS ---
    def add_task(self, title, assignee, creator):
        return self.supabase.table("tasks").insert({
            "title": title, "assignee": assignee, 
            "created_by": creator, "done": False
        }).execute()

    def remove_task(self, task_id):
        return self.supabase.table("tasks").delete().eq("task_id", task_id).execute()

    def get_tasks(self):
        res = self.supabase.table("tasks").select("*").execute()
        return res.data

    def toggle_task_status(self, task_id, current_status):
        return self.supabase.table("tasks").update({"done": not current_status}).eq("task_id", task_id).execute()

    # --- NOTES ---
    def add_note(self, content, author):
        return self.supabase.table("notes").insert({"content": content, "author": author}).execute()

    def get_notes(self):
        res = self.supabase.table("notes").select("*").order("created_at", desc=True).execute()
        return res.data

    def mark_note_as_read(self, note_id, user_name):
        res = self.supabase.table("notes").select("read_by").eq("note_id", note_id).execute()
        if res.data:
            current_readers = res.data[0].get('read_by') or []
            if user_name not in current_readers:
                current_readers.append(user_name)
                return self.supabase.table("notes").update({"read_by": current_readers}).eq("note_id", note_id).execute()
        return None

    def delete_note(self, note_id):
        return self.supabase.table("notes").delete().eq("note_id", note_id).execute()

    # --- BIRTHDAYS ---
    def add_birthday(self, name, date_str):
        return self.supabase.table("birthdays").insert({"name": name, "date": date_str}).execute()

    def get_birthdays(self):
        res = self.supabase.table("birthdays").select("*").order("date").execute()
        return res.data

    def remove_birthday(self, birthday_id):
        return self.supabase.table("birthdays").delete().eq("birthday_id", birthday_id).execute()

    # --- WEEKLY MENU ---
    def add_menu_item(self, day, meal_type, dish):
        return self.supabase.table("weekly_menu").insert({
            "day": day, "meal_type": meal_type, "dish": dish
        }).execute()

    def get_menu(self):
        res = self.supabase.table("weekly_menu").select("*").execute()
        return res.data

    def clear_menu_item(self, item_id):
        return self.supabase.table("weekly_menu").delete().eq("item_id", item_id).execute()

    # --- UPGRADES ---
    def add_upgrade(self, upgrade_name):
        return self.supabase.table("upgrades").insert({"upgrade_name": upgrade_name}).execute()

    def remove_upgrade(self, upgrade_id):
        return self.supabase.table("upgrades").delete().eq("upgrade_id", upgrade_id).execute()

    def get_upgrades(self):
        res = self.supabase.table("upgrades").select("*").execute()
        return res.data
    
    # --- SHOWERS ---
    def get_showers(self, target_date):
        res = self.supabase.table('douches').select('*').eq('date', target_date).execute()
        return res.data
    
    def add_shower_slot(self, slot_time, user_name, target_date):
        return self.supabase.table('douches').insert({
            'slot_time': slot_time,
            'user_name': user_name,
            'date': target_date
        }).execute()

    def remove_shower(self, shower_id):
        return self.supabase.table('douches').delete().eq('douche_id', shower_id).execute()

    # --- CALENDAR ---
    def get_calendar(self, start_date, end_date):
        res = self.supabase.table('family_calendar').select('*').gte('event_date', start_date).lte('event_date', end_date).order('start_time').execute()
        return res.data
    
    def add_calendar(self, name, date, start, end, member):
        return self.supabase.table("family_calendar").insert({
            "event_name": name, "event_date": date, 
            "start_time": start, "end_time": end, "member": member
        }).execute()

    def remove_calendar(self, event_id):
        return self.supabase.table('family_calendar').delete().eq('calendar_id', event_id).execute()

@st.cache_resource
def get_db():
    return FamilyDB()