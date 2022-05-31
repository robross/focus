import json
import os


def _loadDatabase():
    if not os.path.isfile('data.json'):
        emptyDb = {}
        emptyDb['items'] = []

        _saveDatabase(emptyDb)

    with open('data.json', 'r') as f:
        return json.load(f)


def _saveDatabase(db):
    with open('data.json', 'w') as f:
        json.dump(db, f)


def _appendItem(item, db):
    id = len(db['items'])
    db['items'].append({
        "id": id,
        "text": item,
        "deleted": False
    })


def _deleteItem(id, db):
    for item in db['items']:
        if item["id"] == id:
            item['deleted'] = True
            return


if __name__ == '__main__':
    db = _loadDatabase()

    while (True):
        os.system('clear')

        for item in db['items']:
            if not item["deleted"]:
                print(f'{item["id"]}\t{item["text"]}')

        print('\n')

        command = input('focus: ').strip()

        if len(command) == 0:
            continue

        if command.lower() == 'exit':
            break

        if command.startswith('rm'):
            id = int(command[3:])
            _deleteItem(id, db)
        else:
            _appendItem(command, db)

        _saveDatabase(db)
