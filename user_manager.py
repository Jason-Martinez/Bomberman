import json
import os

SCORES_PATH = os.path.join('Assets', 'data', 'scores.json')
class Users_data:
    def __init__(self,username):
        self.username = username.strip()
        self.file_path = SCORES_PATH

    def load_data(self):
        if not os.path.exists(SCORES_PATH):
            return []
        try:
            with open(SCORES_PATH, "r") as file:
                return json.load(file)
            
        except (FileNotFoundError, json.JSONDecodeError):
            return []
      
    def save_data(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def save_or_update_user(self, score=0, skin=0):
        data = self.load_data()
        user_data = {"user": self.username, "score": score, "skin": skin}
        for i, entry in enumerate(data):
            if entry.get("user") == self.username:
                # Solo cambia la skin, mantiene el score
                user_data["score"] = entry.get("score", 0)
                data[i] = user_data
                break
        else:
            # Si no existe, lo agrega
            data.append(user_data)
        self.save_data(data)
            
    def get_top5(self):
        data = self.load_data()
        return sorted(data, key=lambda x: x.get("score", 0), reverse=True)[:5]
    
    def get_user(self):
        data = self.load_data()
        for entry in data:
            if entry.get("user") == self.username:
                return entry
        return None
    
    def update_score(self, new_score):
        data = self.load_data()
        for entry in data:
            if entry.get("user") == self.username:
                entry["score"] = new_score
                break
        self.save_data(data)

