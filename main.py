import os
import re

from nlp import truecase


def _printDatabase(db):
    for item in db['items']:
        if item['deleted']:
            continue

        print(f'{item["id"]}\t{item["text"]}')

    print('\n')


def _removeItem(db, id):
    for item in db['items']:
        if item['id'] == int(id):
            item['deleted'] = True
            break

    return db


def _addItem(db, command):
    item = {
        'text': command,
        'id': 1 if len(db['items']) == 0 else db['items'][-1]["id"] + 1,
        'deleted': False
    }

    db['items'].append(item)

    return db


def _buildDatabase(log):
    db = {
        'items': []
    }

    commandHandlers = [
        (re.compile('rm ([0-9]+)$', re.IGNORECASE), _removeItem),
        (re.compile('(.*)'), _addItem)
    ]

    for i, command in enumerate(log):
        for handler in commandHandlers:
            match = handler[0].match(command)
            if match:
                db = handler[1](db, *match.groups())
                break

    return db


if __name__ == '__main__':
    log = []

    while True:
        db = _buildDatabase(log)

        os.system('clear')
        _printDatabase(db)

        command = input('focus: ')
        command = command.strip()

        if command.lower() == 'exit':
            break

        command = truecase(command)
        log.append(command)
