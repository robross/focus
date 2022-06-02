import os
import re

from nlp import truecase
from actionWords import isActionWord


def _printDatabase(db):
    for item in db['items']:
        if item['deleted']:
            continue
        # ○●
        icon = '-'
        if item["type"] == "task":
            icon = '⨯' if item['status'] == 'done' else "·"

        print(f'{item["id"]}\t{icon} {item["text"]}')

    print('\n')


def _removeItem(db, id):
    for item in db['items']:
        if item['id'] == int(id):
            item['deleted'] = True
            break

    return db


def _todoItem(db, id):
    for item in db['items']:
        if item['id'] == int(id):
            item['status'] = ''
            break

    return db


def _doneItmem(db, id):
    for item in db['items']:
        if item['id'] == int(id):
            item['status'] = 'done'
            break

    return db


def _addItem(db, command):
    item = {
        'text': command,
        'id': 1 if len(db['items']) == 0 else db['items'][-1]["id"] + 1,
        'deleted': False,
        'type': 'task' if isActionWord(command.split(' ')[0]) else 'note',
        'status': ''
    }

    db['items'].append(item)
    db = _refreshTags(db)

    return db


def _tagItem(db, id, tags):
    for item in db['items']:
        if item['id'] == int(id):
            item['text'] = item['text'] + ' ' + tags
            break

    db = _refreshTags(db)

    return db


def _updateItem(db, id, text):
    for item in db['items']:
        if item['id'] == int(id):
            item['text'] = text
            break

    db = _refreshTags(db)

    return db


def _refreshTags(db):
    tags = []
    for item in db['items']:
        for tag in re.findall('#([^\s]+)', item['text']):
            if tag not in tags:
                tags.append(tag.lower())

    for item in db['items']:
        taggedWords = []
        words = item['text'].split(' ')
        for word in words:
            taggedWords.append('#' + word if word.lower() in tags else word)

        item['text'] = (' ').join(taggedWords)

    return db


def _buildDatabase(log):
    db = {
        'items': [],
        'tags': []
    }

    commandHandlers = [
        (re.compile('rm ([0-9]+)$', re.IGNORECASE), _removeItem),
        (re.compile('todo ([0-9]+)$', re.IGNORECASE), _todoItem),
        (re.compile('done ([0-9]+)$', re.IGNORECASE), _doneItmem),
        (re.compile('tag ([0-9]+) (#.*)', re.IGNORECASE), _tagItem),
        (re.compile('update ([0-9]+) (.*)', re.IGNORECASE), _updateItem),
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
    undoStack = []
    macro = ''

    while True:
        db = _buildDatabase(log)

        os.system('clear')
        _printDatabase(db)

        macroText = macro if '~' not in macro else f'{macro}> '
        command = input(f'focus:{macroText} ')
        command = command.strip()

        if len(command) == 0:
            macro = ''
            continue

        if command.lower() == 'exit':
            break

        if command.lower() == 'undo':
            if len(log) > 0:
                undoStack.append(log.pop())
            continue
        elif command.lower() == 'redo':
            if len(undoStack) > 0:
                log.append(undoStack.pop())
            continue
        else:
            undoStack = []

        if command[0] == '>':
            macro = command[1:].strip()
            continue

        if len(macro) > 0:
            if '~' in macro:
                command = macro.replace('~', command)
            else:
                command = macro + ' ' + command 

        command = truecase(command)
        log.append(command)
