import telebot
from telebot import types
import random
from const import QUESTIONS
import time
from datetime import datetime

bot = telebot.TeleBot('6800103265:AAHLErhC2EnRsnCQzn1kJHjzWMgWQuo169o')

current_questions = QUESTIONS.copy()
current_question = 0
score = 0
counter_question = 1
timer=0


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(
        message.chat.id,
        f'Вітаю!\nЯ бот TestPython!\n{message.from_user.first_name} я пропоную вам пройти цей тест\n\nРОЗПОЧАТИ ТЕСТ ?',
        reply_markup=create_start_keyboard()
    )


@bot.message_handler(commands=['restart'])
def restart(message):
    global current_questions
    global counter_question
    global current_question
    global score

    current_questions = QUESTIONS.copy()
    score = 0
    counter_question = 1
    current_question = 0
    random.shuffle(current_questions)
    bot.send_message(
        message.chat.id,
        'Перезапустити тест?',
        reply_markup=create_start_keyboard()
    )


@bot.message_handler(commands='info')
def main(message):
    bot.send_message(message.chat.id, 'Розробив Фоменко Вʼячеслав')

    # bot.register_next_step_handler(message)


def create_start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    start_test_btn = types.KeyboardButton('Розпочати тест')
    keyboard.add(start_test_btn)
    return keyboard


def create_ansvers_keyboard():
    answears_keyboard = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    a_btn = types.KeyboardButton('a')
    b_btn = types.KeyboardButton('b')
    c_btn = types.KeyboardButton('c')
    d_btn = types.KeyboardButton('d')
    answears_keyboard.add(a_btn, b_btn, c_btn, d_btn)
    return answears_keyboard


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.lower()


    print(text)
    global current_questions
    global counter_question
    global current_question
    global score
    global timer
    # print(text)
    if 'розпочати тест' == text:
        current_questions = QUESTIONS.copy()
        score = 0
        random.shuffle(current_questions)
        current_question = current_questions[0]
        timer = time.time()
        bot.send_message(message.chat.id, f'Тест розпочато!\nПитання {counter_question} / 10\n {current_question["question"]}',  reply_markup=create_ansvers_keyboard())
        current_questions.remove(current_question)
        counter_question = counter_question + 1
        print('\n')
        for p in current_questions:
          print(p)
        return

    if isinstance(current_question, dict):
        try:
            print(counter_question)
            if text == current_question['answer']:
              if counter_question == 11:
                print('\n')
                print('hello')
                for p in current_questions:
                  print(p)
                current_questions = QUESTIONS.copy()
                counter_question = 1
                current_question = 0
                restart_keyboard = types.ReplyKeyboardMarkup(
                    row_width=1, resize_keyboard=True)
                restart_btn = types.KeyboardButton('/restart')
        
                restart_keyboard.add(restart_btn)
                elapsed_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - timer))
                bot.send_message(message.chat.id, f'Ваш рахунок = {score}\nЧас виконання{elapsed_time}\nДата{datetime.now().strftime("%Y.%m.%d  %H:%M:%S ")}', reply_markup=restart_keyboard)
                score = 0
                timer=0
                
                
                return
              score = score + 1
              bot.send_message(message.chat.id,f'Віповідь правильна !')
              random.shuffle(current_questions)
              current_question = random.choice(current_questions)
              bot.send_message(message.chat.id, f'Питання {counter_question} / 10\n {current_question["question"]}',    reply_markup=create_ansvers_keyboard())
              counter_question = counter_question + 1
              print('\n')
              for p in current_questions:
                  print(p)
              current_questions.remove(current_question)
              return
            else:
              if counter_question == 11:
                current_questions = QUESTIONS.copy()
                counter_question = 1
                current_question = 0
                restart_keyboard = types.ReplyKeyboardMarkup(
                    row_width=1, resize_keyboard=True)
                restart_btn = types.KeyboardButton('/restart')

                restart_keyboard.add(restart_btn)
                elapsed_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - timer))
                bot.send_message(message.chat.id, f'Ваш рахунок = {score}\nЧас виконання {elapsed_time}\nДата {datetime.now().strftime("%Y.%m.%d  %H:%M:%S ")}', reply_markup=restart_keyboard)
                score = 0
                timer=0
                print('\n')
                for p in current_questions:
                  print(p)
                return
              # random.shuffle(current_questions)
              bot.send_message(message.chat.id,f'Віповідь не правильна , правильна відповідь {current_question['answer']}!')
              current_question = random.choice(current_questions)
              bot.send_message(message.chat.id, f'Питання {counter_question} / 10\n {current_question["question"]}',    reply_markup=create_ansvers_keyboard())
              counter_question = counter_question + 1
              for p in current_questions:
                print(p)
              current_questions.remove(current_question)
              return
        except():
            print('err')
            

    # print(len(current_questions))
    if counter_question == 10:
        current_questions = QUESTIONS.copy()
        counter_question = 1
        current_question = 0
        restart_keyboard = types.ReplyKeyboardMarkup(
            row_width=1, resize_keyboard=True)
        restart_btn = types.KeyboardButton('/restart')

        restart_keyboard.add(restart_btn)
        elapsed_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - timer))
        bot.send_message(message.chat.id, f'Ваш рахунок = {score}\nЧас виконання {elapsed_time}\nДата {datetime.now().strftime("%Y.%m.%d  %H:%M:%S ")}', reply_markup=restart_keyboard)
        score = 0
        timer=0
        for p in current_questions:
            print(p)
        return


@bot.message_handler(func=lambda message: message.text.lower() == 'рестарт тест')
def restart_test(message):
    global current_questions
    global counter_question
    global current_question
    global score

    current_questions = QUESTIONS.copy()
    score = 0
    random.shuffle(current_questions)
    current_question = random.choice(current_questions)
    counter_question = 1

    bot.send_message(message.chat.id, f'Тест розпочато!\nПитання {counter_question} / 10\n {current_question["question"]}', reply_markup=create_ansvers_keyboard())


bot.polling(non_stop=True)
