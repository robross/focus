import json
import os


def _loadDatabase():
    if not os.path.isfile('data.json'):
        emptyDb = {}
        emptyDb['items'] = []
        emptyDb['log'] = []

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


def _setContexOnItem(id, context, db):
    for item in db['items']:
        if item["id"] == id:
            text = item['text']
            baseParts = []
            parts = text.split(' ')
            for part in parts:
                if part[0] in ['#', '@']:
                    continue
                baseParts.append(part)

            baseParts.append(' ' + context)

            item["text"] = ' '.join(baseParts)
            return


def _processCommand(command, db):
    if command.startswith('rm'):
        id = int(command[3:])
        _deleteItem(id, db)
    elif command.startswith('set context'):
        parts = command.split(' ')
        id = int(parts[2])
        context = ' '.join(parts[3:])
        _setContexOnItem(id, context, db)
    else:
        _appendItem(command, db)


def _logCommand(command, db):
    db["log"].append({
        "command": command,
        "active": True
    })


def _rebuildDatabase(db):
    db["items"] = []
    for logEntry in db['log']:
        if not logEntry['active']:
            continue

        _processCommand(logEntry['command'], db)


def _undo(db):
    for item in reversed(db['log']):
        if not item['active']:
            continue

        item["active"] = False
        break

    _rebuildDatabase(db)


def _redo(db):
    undoStack = []
    for item in reversed(db['log']):
        if not item['active']:
            undoStack.append(item)
        else:
            break

    if len(undoStack) == 0:
        return

    undoStack[-1]['active'] = True
    _rebuildDatabase(db)


if __name__ == '__main__':
    db = _loadDatabase()
    context = ''

    while (True):
        os.system('clear')

        for item in db['items']:
            if not item["deleted"]:
                print(f'{item["id"]}\t{item["text"]}')

        print('\n')

        command = input(f'focus({context.strip()}): ').strip()

        if len(command) == 0:
            context = ' '.join(context.split(' ')[:-1])
            continue

        if command.lower() == 'exit':
            break

        if command == 'undo':
            _undo(db)
            _saveDatabase(db)
            continue
        
        if command == 'redo':
            _redo(db)
            _saveDatabase(db)
            continue

        if command[0] in ['#', '@']:
            command = command.replace(' ', '_')
            suffix = ' ~' if context.endswith('~') else ''
            oldContext = context.strip(' ~')

            context = oldContext + ' ' + command + suffix
            continue

        if context.endswith('~'):
            command = int(command)
            command = f'set context {command} {context[:-1].strip()}'
            _processCommand(command, db)
            _logCommand(command, db)
            _saveDatabase(db)
            continue

        if command == '~':
            context = context.strip() + ' ~'
            continue

        _processCommand(command + context, db)
        _logCommand(command + context, db)

        _saveDatabase(db)
