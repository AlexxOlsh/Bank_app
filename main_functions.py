import codecs

def check_password(user_pass, input_pass):
    if input_pass != user_pass:
        print('Неверный пароль!\n')
        return False
    else:
        return True


def check_auth(user, login):
    if user['fio'] == '' and user['password'] == '':
        print("Создайте аккаунт!\n")
        return False

    elif not (login):
        temp_pasword = input('Введите пароль: ')

        if (not (check_password(user['password'], temp_pasword))):
            return False
    else:
        return True


def read_file(file_path):
    file_str = ''
    with codecs.open(file_path, encoding='utf-8') as open_file:
        for line in open_file:
            file_str += line

    return file_str


def read_user_file(file_path):
    user_file = {}
    with codecs.open(file_path, encoding='utf-8') as open_file:
        for line in open_file:
            line_array = line.split()
            key = line_array[0]
            line_array.remove(key)
            line_array_str = ''
            for word in line_array:
                if line_array_str == '':
                    line_array_str += word
                else:
                    line_array_str += ' ' + word

            user_file[key] = line_array_str
        user_file['limit'] = int(user_file['limit'])
        user_file['balance'] = int(user_file['balance'])

    return user_file


def write_user_file(user):
    user_file = ''
    for key, value in user.items():
        user_file += key + ' ' + str(value) + '\n'

    write_file(user_file, 'memory/' + user['fio'] + '.txt')


def write_file(file_str, file_path):
    with codecs.open(file_path, 'w', encoding='utf-8') as open_file:
        open_file.write(file_str)


def get_waiting_transactions(file_path):
    result = 0
    with open(file_path, encoding='utf-8') as open_file:
        for line in open_file:
            line_array = line.split()
            if line_array[-1] != 'True':
                result += 1

    return result


def get_statistics(file_path):
    with codecs.open(file_path, encoding='utf-8') as open_file:
        statistics = {}
        for line in open_file:
            line_arr = line.split()

            if line_arr[-1] != 'True':
                if (line_arr[0] in statistics):
                    statistics[line_arr[0]] += 1
                else:
                    statistics[line_arr[0]] = 1

    return statistics


def run_transaction(file_path, user):
    with codecs.open(file_path, encoding='utf-8') as open_file:
        output_file_lines = ''
        for line in open_file:
            line_arr = line.split()
            if line_arr[-1] != 'True':
                if line_arr[-1] == 'False':
                    line_arr.remove('False')

                temp_sum = int(line_arr[0])
                output_file_lines += line_arr[0] + ' '
                temp_print = 'Транзакция «'
                if user['limit'] >= (user['balance'] +
                                     temp_sum) or user['limit'] == -1:
                    line_arr.remove(str(temp_sum))

                    user['balance'] += int(temp_sum)
                    for word in line_arr:
                        temp_print += word + ' '
                        output_file_lines += word + ' '

                    output_file_lines += 'True'

                    temp_print += '» на сумму ' + str(
                        temp_sum) + 'руб. успешно применена.'
                else:
                    line_arr.remove(str(temp_sum))
                    for word in line_arr:
                        temp_print += word + ' '
                        output_file_lines += word + ' '

                    output_file_lines += 'False'
                    temp_print += '» на сумму ' + str(
                        temp_sum) + ' руб. не может быть применена (превышен лимит).'

                print(temp_print)
                output_file_lines += '\n'
            else:
                output_file_lines += line

    write_file(output_file_lines, file_path)

    return user


def check_int_input(input_text):

    value = int(input(input_text))
    return [True, value]



# def check_int_input(input_text):
#     try:
#         value = int(input(input_tex
#         return [True, value]
#     except ValueError:
#         print('Введите, пожалуйста, число \n')
#         return [False, -1]


def transaction_filter(file_path, threshold):
    with open(file_path, encoding='utf-8') as open_file:
        for line in open_file:
            words = line.split()
            try:
                trans = int(words[0])
            except ValueError:
                trans = 0

            if trans >= threshold:
                if words[-1] == 'True':
                    words[-1] = "- Выполнено"
                else:
                    words[-1] = "- Ожидает выполнения"

                yield ' '.join(words)
