import os

from nlp import truecase


def _printDatabase(db):
    for item in db['items']:
        print(item)

    print('\n')


def _buildDatabase(log):
    db = {
        'items': []
    }

    for command in log:
        db['items'].append(command)

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
