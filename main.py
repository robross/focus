if __name__ == '__main__':
    db = []

    while True:
        for item in db:
            print(item)

        print('\n')

        command = input('focus: ')
        command = command.strip()

        if command.lower() == 'exit':
            break

        db.append(command)