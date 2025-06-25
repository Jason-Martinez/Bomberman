import json


class Users_data:
    def __init__(self,username, file_path="Bomberman/assets/data/scores.json"):
        self.username = username.strip()
        self.file_path = file_path
        

    def exist_user_or_create_user(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        for entry in data:
            if entry.get("user") == self.username:
                return False
            
        data.append({"user": self.username, "score": 0})
        with open(self.file_path, "w") as file:
            json.dump(data, file)

        return True
            
    def get_top5(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        top5 = sorted(data, key=lambda x: x.get("score", 0), reverse=True)[:5]
        return top5

