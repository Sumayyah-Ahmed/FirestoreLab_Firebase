import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('utils/credentials.json')  # Replace with your Firebase credentials file path
firebase_admin.initialize_app(cred)
db = firestore.client()   
    
def add_player():
    # Get player details from user input
    player_first_name = input("Enter player first name: ")
    player_last_name = input("Enter player last name: ")
    birthdate = input("Enter player birthdate: ")
    rating = input("Enter player rating: ")
    team_id = input("Enter team ID for the player: ")
 
    # Check if the team exists
    team_ref = db.collection('teams').document(team_id)
    team_doc = team_ref.get()
 
    if not team_doc.exists:
        print(f"No team found with ID '{team_id}'. Please enter a valid team ID.")
        return
 
    # Add player to the players collection
    player_data = {
        'firstName': player_first_name,
        'lastName' : player_last_name,
        'birthdate': birthdate,
        'rating': rating,
        'teamId': team_ref  # Reference to the team document
    }
    player_ref = db.collection('players').document()  # Auto-generate player ID
    player_ref.set(player_data)
 
    # Update the team's players array with the new player reference
    team_ref.update({
        'players': firestore.ArrayUnion([player_ref])})

add_player()
