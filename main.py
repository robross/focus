
def _printList(db):
    for item in db:
        print(item)

    print('\n')


if __name__ == '__main__':
    db = []

    while True:
        _printList(db)

        command = input('focus: ')
        command = command.strip()

        if command.lower() == 'exit':
            break

        db.append(command)
