import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('utils/credentials.json')  # Replace with your Firebase credentials file path
firebase_admin.initialize_app(cred)
db = firestore.client()

# get a reference to the coaches collection, then display all documents in the collection

coaches_ref = db.collection('coaches')
coaches = coaches_ref.get() # get retrieves a snapshot of data
 
for coach in coaches:
        coach_data = coach.to_dict()
        name = coach_data['firstName'] + " " + coach_data['lastName']
        email = coach_data['email']
        team_ref = coach_data['teamId']
        team_doc = team_ref.get()
        team_name = team_doc.to_dict().get('name', 'Unknown Team')
        print(f"Name: {name}, Email: {email}, Team: {team_name}")

