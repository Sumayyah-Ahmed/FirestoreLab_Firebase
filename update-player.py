import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter

# Initialize Firebase
cred = credentials.Certificate('utils/credentials.json')  # Replace with your Firebase credentials file 
firebase_admin.initialize_app(cred)
db = firestore.client()

last_name = input("Enter player's last name: ")
new_rating = input("Enter new rating: ")

#find the player document then update the rating
players_ref = db.collection('players')
query = players_ref.where(filter=FieldFilter('lastName', '==', last_name)).limit(1)
players = query.stream()
for player in players:
    player_ref = player.reference
    player_ref.update({"rating": new_rating})