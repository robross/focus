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
    db['items'].append(item)


if __name__ == '__main__':
   db = _loadDatabase()
   
   while (True):
       os.system('clear')

       for item in db['items']:
           print(item)
        
       print('\n')

       command = input('focus: ')
       
       if command.lower() == 'exit':
           break

       _appendItem(command, db)
       _saveDatabase(db)
           

