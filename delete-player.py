import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter

# Initialize Firebase
cred = credentials.Certificate('utils/credentials.json')  # Replace with your Firebase credentials file path
firebase_admin.initialize_app(cred)
db = firestore.client()

last_name = input("Enter player's last name: ")

player_ref = db.collection("players")
query = player_ref.where(filter=FieldFilter('lastName', '==', last_name)).limit(1)
players = query.stream()
for player in players:
    player_data = player.to_dict()
    team_ref = player_data.get('teamId')
    team_ref.update({"players": firestore.ArrayRemove([player.reference])}) 
    player.reference.delete() 
    print('player deleted')

    
 







