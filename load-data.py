import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase
cred = credentials.Certificate('utils\credentials.json')  # Replace with your Firebase credentials file path
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load data from JSON file
with open('utils/soccer-data.json', 'r') as file:
    data = json.load(file)

# Function to load teams data
def load_teams(teams):
    for team in teams:
        team_doc = db.collection('teams').document(team['teamId']) #sets the reference id
        team_doc.set({
            'name': team['name'],
            'colors' : team['colors'],           
            'coachId': db.document(f'coaches/{team["coachId"]}'),
            'players': []  # This will be populated with player references later
        })
    print("Teams loaded successfully.")

# Function to load players data
def load_players(players):
    for player in players:
        player_doc = db.collection('players').document()
        player_doc.set({
            'firstName': player['firstName'],
            'lastName' : player['lastName'],
            'birthdate': player['birthdate'],
            'rating': player['rating'],
            'teamId': db.document(f'teams/{player["teamId"]}')
        })
        
        # Update team document with the player's reference
        team_ref = db.collection('teams').document(player['teamId'])
        team_ref.update({
            'players': firestore.ArrayUnion([player_doc])  # Add player reference to the team's players array
        })
    print("Players loaded successfully.")

# Function to load coaches data
def load_coaches(coaches):
    for coach in coaches:
        coach_doc = db.collection('coaches').document(coach["coachId"])
        coach_doc.set({
            'firstName': coach['firstName'],
            'lastName': coach['lastName'],
            'email' : coach['email'],
            'teamId': db.document(f'teams/{coach["teamId"]}')
        })
    print("Coaches loaded successfully.")

# Load the data
load_teams(data['teams'])
load_players(data['players'])
load_coaches(data['coaches'])


