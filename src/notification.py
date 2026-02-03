import requests

def send_private_notification(message, targets_members):
    topics = {
        'Amaury': "famille_caudiu_levan_amaury",
        'Corentin': "famille_caudiu_levan_corentin",
        'Thais': "famille_caudiu_levan_thais",
        'Papoune': 'famille_caudiu_levan_papoune',
        'Maman': 'famille_caudiu_levan_maman'
    }
    for target_member in targets_members:
        topic=topics.get(target_member)
        if topic:
            try:
                requests.post(f"https://ntfy.sh/{topic}",
                    data=message.encode('utf-8'),
                    headers={
                        'Title':'Nouvelle tache assignee',
                        'Priority':'high',
                        'Tags':'clipboard,memo'
                    }
                )
                return True
            except Exception as err:
                print(f'Erreur ntfy : {err}')
                return False
        else:
            return False