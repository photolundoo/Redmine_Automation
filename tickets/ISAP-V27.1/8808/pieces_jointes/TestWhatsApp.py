import requests
import json

def send_whatsapp_alert(recipient_number, template_name, variable_header, variable_body):
    # 1. Configuration des identifiants (à mettre en variables d'environnement idéalement)
    ACCESS_TOKEN = "EAANV7J9sdSEBQxYgX7jqcGZC2az4MT5w5rCM8FEHGjA6L7UfOtgIM7dmQ4JgikXUVHZAJWesY8W8L9Tn8DFtKOQVlGkW35KAE2R6evLQn5p7pquQEioCW9lYbi4iKB3FCKblUDNNaAFZBjZBtr5ASZCKyaY5Q4ScnKPRu1ADEKXlcJP2mJY7l36olI4XwFkq5aNnIMiCeV27iaOEizMz0aeDX29a3ZA2OGs6stvpYwslJua3f6FI3mKoiSqBSGTZA1cnHDRNsTe1jdBZCJ44wICOrhIOZBuWItuBYQTUZD"
    PHONE_NUMBER_ID = "996949010175728" # Trouvé dans le portail Meta Dev : Configuration / Gérer numéros de téléphone
    VERSION = "v21.0" # Vérifie la version actuelle dans la doc
    
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # 2. Construction du payload
    # On utilise ici un Template avec des paramètres dynamiques {{1}}, {{2}}, etc.
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number, # Format E.164 (ex: "33612345678")
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": "fr" # Code langue du template
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {"type": "text", "parameter_name" : var, "text": value} for var,value in variable_header.items()
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "parameter_name" : var, "text": value} for var,value in variable_body.items()
                    ]
                }
            ]
        }
    }
    
    print(payload)

    # 3. Envoi de la requête
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Lève une erreur si le code HTTP n'est pas 200
        print("Alerte envoyée avec succès !")
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"Erreur lors de l'envoi : {err.response.text}")
        return None


destinataire = "33698796646" # Ton numéro de test
nom_du_template = "alerte_incident" # Le template par défaut de Meta pour tester
parametres_header = {"type" : "Enfant perdu"}
parametres_body = {"type" : "Enfant perdu", "category" : "Gestion visiteurs", "level" : "3"}

for number in ["33698796646", "33608323663"]:
    # Note: Pour le template "hello_world", il n'y a souvent pas de paramètres.
    # Laisse la liste vide [] pour le test initial.
    send_whatsapp_alert(number, nom_du_template, parametres_header, parametres_body)
