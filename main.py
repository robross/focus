import json
import os


def _loadDatabase():
    if not os.path.isfile('data.json'):
        emptyDb = {}
        emptyDb['items'] = []

        with open('data.json', 'w') as f:
            json.dump(emptyDb, f)

    with open('data.json', 'r') as f:
        return json.load(f)


if __name__ == '__main__':
   db = _loadDatabase()
   print(db)