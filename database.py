import json
import os

class Database:
    def __init__(self, filename="history.json"):
        self.filename = filename

        # Se o arquivo não existir, cria um vazio
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump([], file)

    # Carregar dados do JSON
    def load(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    # Salvar um novo registro no histórico
    def save(self, data):
        history = self.load()
        history.append(data)

        with open(self.filename, "w") as file:
            json.dump(history, file, indent=4)
