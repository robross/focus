import os

from nlp import truecase


def _printDatabase(db):
    for item in db['items']:
        print(f'{item["id"]}\t{item["text"]}')

    print('\n')


def _buildDatabase(log):
    db = {
        'items': []
    }

    for i, command in enumerate(log):
        item = {
            'text': command,
            'id': i + 1 
        }

        db['items'].append(item)

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
