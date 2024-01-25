from datetime import datetime
import main_functions
import os.path

if __name__ == "__main__":
    temp_menu = -1
    login = False
    menu_str = 'Выберите операцию: \n 1. Cоздать аккаунт \n 2. Положить деньги на счет \n 3. Cнять деньги \n 4. Вывести баланс на экран \n 5. Добавить транзакцию \n 6. Выставить лимит на счет \n 7. Применить транзакции \n 8. Статистика по ожидаемым пополнениям \n 9. Отфильтровать транзакции \n 0. Выйти из программы \n'
    current_year = datetime.now().year
    choose = -1

    user = {
        'fio': '',
        'password': '',
        'birth': 0,
        'age': 0,
        'balance': 0,
        'limit': -1
    }

    while choose != 0:
        status, choose = main_functions.check_int_input(
            'Добрый день! \nВосстановить сохраненную информацию? \n1. Да \n2. Heт \n0. Завершить программу \n')
        if not (status):
            continue

        if choose == 1:
            login_fio = input("Введите ФИО: ")

            if not os.path.exists('memory'):
                os.mkdir('memory')

            if os.path.exists('memory/' + login_fio + '.txt'):
                login_info = main_functions.read_user_file('memory/' + login_fio + '.txt')
            else:
                print('Аккаунт не найден!\n')
                continue

            temp_pasword = input('Введите пароль: ')
            if temp_pasword != login_info['password']:
                print('Неверный пароль!\n')
            else:
                print('С возвращением!\n')
                login = True
                user = login_info
                break

        elif choose == 2:
            break

    while temp_menu != 0:
        status, temp_menu = main_functions.check_int_input(menu_str)
        if not (status):
            continue

        if temp_menu == 1:
            fio = input("Введите ФИО: ")
            user['fio'] = fio
            if fio == '':
                print('Некорректное имя\n')
                continue

            status, user['birth'] = main_functions.check_int_input("Введите год рождения: ")
            if not (status):
                continue

            if user['birth'] <= 0 or user['birth'] > current_year:
                print('Некорректный год рождения!\n')
                continue

            user['age'] = current_year - user['birth']
            age_year = user['age'] % 10

            if age_year == 1:
                age_text = 'год'
            elif 2 <= age_year <= 4:
                age_text = 'года'
            else:
                age_text = 'лет'

            print("Создан аккаунт: " + str(user['fio']) + " (" + str(user['age']) +
                  " " + age_text + ")")

            user['password'] = input("Создайте пароль для аккаунта: ")
            if user['password'] == '':
                while user['password'] == '':
                    user['password'] = input("Создайте пароль для аккаунта: ")

            main_functions.write_user_file(user)
            login = True
            print("Аккаунт успешно зарегистрирован!\n")

        elif temp_menu == 2:
            if (not (main_functions.check_auth(user, login))):
                continue

            status, temp_sum = main_functions.check_int_input('Введите сумму пополнения: ')
            if not status:
                continue

            if temp_sum > 0:
                if user['limit'] == -1 or user['limit'] >= (user['balance'] + temp_sum):
                    user['balance'] += temp_sum
                    main_functions.write_user_file(user)
                    print('Счёт успешно пополнен!\n')
                else:
                    print('Сумма превышает установленный лимит\n')
            else:
                print('Сумма должна быть больше нуля!\n')

        elif temp_menu == 3:
            if not (main_functions.check_auth(user, login)):
                continue

            status, temp_sum = main_functions.check_int_input('Ваш баланс: ' + str(user['balance']) + ' руб. Введите сумму для снятия: ')
            if not status:
                continue

            if temp_sum > user['balance']:
                print('На балансе недостаточно средств!\n')
            elif temp_sum < 0:
                print('Сумма должна быть больше нуля!\n')
            else:
                user['balance'] -= temp_sum
                main_functions.write_user_file(user)
                print("Снятие успешно завершено, ваш баланс: " + str(user['balance']) +
                      " руб.\n")

        elif temp_menu == 4:
            if (not (main_functions.check_auth(user, login))):
                continue

            main_functions.write_user_file(user)
            print("Ваш баланс: " + str(user['balance']) + " руб.\n")

        elif temp_menu == 5:
            if (not (main_functions.check_auth(user, login))):
                continue

            if not os.path.exists('memory'):
                os.mkdir('memory')

            file_path = 'memory/' + user['fio'] + ' операции.txt'
            if os.path.exists(file_path):
                file_str = main_functions.read_file(file_path)
            else:
                file_str = ''

            status, trans_sum = main_functions.check_int_input('Введите сумму транзакции: ')
            if not status:
                continue

            if (trans_sum <= 0):
                print('Сумма должна быть больше нуля!\n')
                continue

            trans_comment = input('Введите комментарий для транзакции: ')
            file_str += str(trans_sum) + ' ' + trans_comment + '\n'
            main_functions.write_file(file_str, file_path)
            transactions_count = main_functions.get_waiting_transactions(file_path)
            print("Количество ожидаемых поступлений: " + str(transactions_count) +
                  '\n')

        elif temp_menu == 6:
            if (not (main_functions.check_auth(user, login))):
                continue

            status, limit = main_functions.check_int_input('Укажите лимит на вашем счету: ')
            if not status:
                continue

            if limit < user['balance']:
                print('На вашем счету баланс больше устанавливаемого лимита')
            else:
                user['limit'] = limit
                main_functions.write_user_file(user)
                print('Лимит успешно установлен')

        elif temp_menu == 7:
            if not (main_functions.check_auth(user, login)):
                continue

            if not os.path.exists('memory'):
                os.mkdir('memory')

            file_path = 'memory/' + user['fio'] + ' операции.txt'
            if os.path.exists(file_path):
                user = main_functions.run_transaction(file_path, user)
                main_functions.write_user_file(user)
            else:
                print('На счету нет запланированных транзакций')

        elif temp_menu == 8:
            if (not (main_functions.check_auth(user, login))):
                continue

            if not os.path.exists('memory'):
                os.mkdir('memory')

            file_path = 'memory/' + user['fio'] + ' операции.txt'
            if os.path.exists(file_path):
                statistics = main_functions.get_statistics(file_path)
                if len(statistics) > 0:
                    for stat, count in statistics.items():
                        print(str(stat) + 'руб: ' + str(count) + ' платеж(а) \n', end='')
                else:
                    print('На счету нет запланированных транзакций')
            else:
                print('На счету нет запланированных транзакций')

        elif temp_menu == 9:
            if not (main_functions.check_auth(user, login)):
                continue

            if not os.path.exists('memory'):
                os.mkdir('memory')

            file_path = 'memory/' + user['fio'] + ' операции.txt'
            if os.path.exists(file_path):
                status, value = main_functions.check_int_input('Введите сумму транзакции: ')
                if not status:
                    continue

                for item in main_functions.transaction_filter(file_path, value):
                    print(item)
            else:
                print('На счету нет запланированных транзакций')


    print("Спасибо за пользование нашей программой, до свидания!")
