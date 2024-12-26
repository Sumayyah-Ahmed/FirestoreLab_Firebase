import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter


# Initialize Firebase
cred = credentials.Certificate('utils/credentials.json')  # Replace with your Firebase credentials file path
firebase_admin.initialize_app(cred)
db = firestore.client()



def find_players_by_team(team_name):
    teams_ref = db.collection('teams')
    team_query = teams_ref.where(filter=FieldFilter('name', '==', team_name)).limit(1)
    team_docs = team_query.stream() #stream provides realtime updates
    team_ref = None
    for team in team_docs:
        team_ref = team.reference 
 
    if not team_ref:
        print(f"No team found with name '{team_name}'. Please enter a valid team name.")
        return
 
    players_ref = db.collection('players')
    query = players_ref.where(filter=FieldFilter('teamId', '==', team_ref))  # teamId is a reference to the team document
    player_docs = query.stream()
 
    for player in player_docs:
        player_data = player.to_dict()
        print(f"{player_data['firstName']} {player_data['lastName']}")
 
 
team_name = input("Enter the team name: ")
find_players_by_team(team_name)
