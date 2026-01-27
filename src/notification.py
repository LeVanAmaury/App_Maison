import requests

def send_family_notification(message, title="Family Hub"):
    topic = "test_marwanetesvraimentgayaufinal"
    url = f"https://ntfy.sh/{topic}"

    try:
        requests.post(
            url,
            data=message.encode('utf-8'),
            headers={
                "Title": title,
                "Priority": "default",
                "Tags": "house_with_garden,bell"
            }
        )
        return True
    except Exception as e:
        print(f"Erreur ntfy : {e}")
        return False