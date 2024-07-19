import firebase_admin
from firebase_admin import credentials, db

class FirebaseDB:
    def __init__(self, credential_path, database_url):
        try:
            # Initialize Firebase with your service account credentials
            cred = credentials.Certificate(credential_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            print("Firebase initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Firebase: {e}")

    def write_record(self, path, data):
        try:
            # Write data to the specified path in the Realtime Database
            ref = db.reference(path)
            ref.set(data)
            print(f"Data written to {path}: {data}")
        except Exception as e:
            print(f"Failed to write data to {path}: {e}")

    def read_record(self, path):
        try:
            # Read data from the specified path in the Realtime Database
            ref = db.reference(path)
            return ref.get()
        except Exception as e:
            print(f"Failed to read data from {path}: {e}")
            return None

    def update_record(self, path, data):
        try:
            # Update data at the specified path in the Realtime Database
            ref = db.reference(path)
            ref.update(data)
            print(f"Data updated at {path}: {data}")
        except Exception as e:
            print(f"Failed to update data at {path}: {e}")

    def delete_record(self, path):
        try:
            # Delete data at the specified path in the Realtime Database
            ref = db.reference(path)
            ref.delete()
            print(f"Data deleted at {path}")
        except Exception as e:
            print(f"Failed to delete data at {path}: {e}")
