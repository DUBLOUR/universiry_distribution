import telebot
from telebot import types
import sqlite3


token="1328045770:AAG_RCxpmVjgrqhYNfFJrsxoRFkGVk2CB80"
bot=telebot.TeleBot(token)
bot.send_message(354502298, "hello")

@bot.message_handler(commands=["start"])
def start_func(message):
    print(1)
    if 1:
#    try:
        conn = sqlite3.connect("data.db")
        db = conn.cursor()
        sql = "SELECT id FROM users"
        db.execute(sql)
        all=db.fetchall()

        not_exist=True
        for i in range(len(all)):
            if message.chat.id==all[i][0]:
                not_exist=False
                break

        if not_exist:
            db.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", [message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name, ""])
            #id, nickname, name, surname, status
            conn.commit()
            bot.send_message(message.chat.id, "Невероятно крутое интро")
        else:
            bot.send_message(message.chat.id, "И снова привет")
"""    except:
        try:
            bot.send_message(message.chat.id, "Не удалось Вас подключить :(")
            print(str(message.chat.id) + ": SIGN-UP ERROR")
        except:
            pass
"""

@bot.message_handler(commands=["start_poll_with_json"])
def poll(message):
    try:
        conn=sqlite3.connect("data.db")
        db=conn.cursor()
        sql = "UPDATE users SET status=? WHERE user_id=?"
        db.execute(sql, ["json_wait", message.chat.id])
        conn.commit()
        bot.send_message(message.chat.id, "Отправьте json в формате: [здесь Максик показывает красноречивый пример входных данных]")
    except:
        try:
            bot.send_message(message.chat.id, "Что-то пошло не так :(")
            print(str(message.chat.id) + ": START POLL ERROR")
        except:
            pass


@bot.message_handler(content_types=["document"])
def poll(message):
    try:
        fil = bot.get_file(message.document.file_id)
        print(message.document.file_size)
        if message.document.file_size <= 10*2**10:
            arr = bot.download_file(fil.file_path)
            with open(str(message.document.file_unique_id)+".json", "wb") as clas:
                clas.write(arr)
        else:
            bot.send_message(message.chat.id, "Слишком большой файл")
    except:
        try:
            bot.send_message(message.chat.id, "Что-то пошло не так :(")
            print(str(message.chat.id) + ": FILE READ ERROR")
        except:
            pass



if __name__ == '__main__':
    bot.polling(none_stop=True)