import streamlit as st
from src.database import FamilyDB

@st.cache_resource      # Pour ne pas recréer la connexion à chaque clic
def get_db():
    return FamilyDB()

db = get_db()

st.title("Gestion famille")

# --- SECTION AJOUT DE TÂCHE ---
st.subheader("Ajouter une tâche")
with st.form("add_task_form"):
    task_text = st.text_input("Quelle est la tâche ?")
    member = st.selectbox("Pour qui ?", ["Amaury", "Thais" , "Corentin", "Maman", "Papoune"])
    submit = st.form_submit_button("Ajouter la tache")

    if submit and task_text:
        db.add_task(task_text, member)
        st.success("Tâche ajoutée !")


# --- SECTION AJOUT DE COURSES ---
st.subheader("Remplir la liste de course")
with st.form("add_shopping_item_form"):
    item_name = st.text_input("Quel objet veux tu ajouter à la liste de course ?")
    item_quantity = st.text_input("Quelle quantité ?")
    submit = st.form_submit_button("Ajouter l'objet")

    if submit and item_name and item_quantity:
        db.add_shopping_item(item_name,item_quantity)
        st.success("Objet ajouté à la liste de course !")




# --- SECTION AFFICHAGE ---
st.divider()

col_tasks, col_shopping = st.columns(2)

with col_tasks:
    st.subheader("Liste des tâches en cours")
    tasks = db.get_tasks()

    if not tasks:
        st.info("Aucune tâche pour le moment.")
    else:
        for task in tasks:
            task_id = task[0]
            task_title = task[1]
            task_member = task[2]

            col_text_task, col_btn_task = st.columns([0.5,0.5])

            with col_text_task:
                st.write(f"**{task_member}** : {task_title}")

            with col_btn_task:
                if st.button("Supprimer", key=f"delete_{task_id}"):
                    db.remove_task(task_id)
                    st.rerun()

with col_shopping:
    st.subheader("Liste de course")
    shopping_list = db.get_shopping_list()

    if not shopping_list:
        st.info("La liste de course est vide.")
    else:
        for item in shopping_list:
            item_id = item[0]
            item_name = item[1]
            item_quantity = item[2]

            col_text_shopping, col_quantity_shopping, col_btn_shopping = st.columns([0.5,0.2,0.3])

            with col_text_shopping:
                st.write(f"**{item_name}**")
            
            with col_quantity_shopping:
                st.write(item_quantity)

            with col_btn_shopping:
                if st.button("Supprimer", key=f"delete_{item_id}"):
                    db.remove_shopping_item(item_id)
                    st.rerun()