from secret import TOKEN
from secret import CHAT_ID
from weekdays import weekdays
from lessons import lessons
from schedule_list import schedule_list
from reminder_times import reminder_times
import telebot
import datetime
import schedule
from threading import Thread
from time import sleep

bot = telebot.TeleBot(TOKEN)
week_type = (datetime.datetime.today().isocalendar()[1] - datetime.date(2022, 2, 7)
             .isocalendar()[1]) % 2
weekday = datetime.datetime.today().weekday()


def day_lessons(day, pretext):
    result = f"*{pretext} {weekdays[day]} (тиждень {str(week_type + 1)})*\n\n"
    lesson_number = 1

    # check if we have lessons today
    if len(schedule_list[week_type][day]) > 0:
        for lesson in schedule_list[week_type][day]:
            if len(lesson) > 0:
                if len(lesson) > 1:
                    for lesson1 in lesson:
                        result += f"{str(lesson_number)}. {lesson1[0]} - {lesson1[1]}\n"
                else:
                    result += f"{str(lesson_number)}. {lesson[0][0]} - {lesson1[0][1]}\n"

            lesson_number += 1
    else:
        result = "Нічого немає, чіллим... Жартую, у вас курсова 👁👄👁"

    return result


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Вітаю! Ось мої команди 👇")
    send_help(message)


@bot.message_handler(commands=["help"])
def send_help(message):
    commands = "*Посилання на пари*\n\n"

    for lesson in lessons:
        commands += f"`!{lesson}` – {lessons[lesson][0].lower()} \n"

    commands += "\n*Розклад*\n\n" \
                "`!сьогодні` – дізнатися розклад на сьогодні\n" \
                "`!завтра` – дізнатися розклад на завтра\n" \
                "`!розклад` – розклад початку та кінця пар"

    bot.send_message(message.chat.id, commands,
                     parse_mode="Markdown",
                     disable_web_page_preview=True)


@bot.message_handler(func=lambda message: True)
def main(message):
    if message.text[0] != "!":
        return

    request = message.text.lower()[1:]

    if request in lessons:
        bot.send_message(message.chat.id, lessons[request][1])
    elif request == "сьогодні" or request == "с":
        bot.send_message(message.chat.id, day_lessons(weekday, "Сьогодні"),
                         parse_mode="Markdown",
                         disable_web_page_preview=True)
    elif request == "завтра" or request == "з":
        bot.send_message(message.chat.id, day_lessons((weekday + 1) % 7, "Завтра"),
                         parse_mode="Markdown",
                         disable_web_page_preview=True)
    elif request == "розклад" or request == "р":
        result = "😃 1: 9:00-10:20\n" \
                "🙂 2: 10:30-11:50\n" \
                "🙃 3: 12:30-13:50\n" \
                "😶 4: 14:00-15:20\n" \
                "😶‍🌫️ 5: 15:30-16:50\n" \
                "🫠 6: 17:00-18:20\n" \
                "💀 7: 18:30-19:50"
        bot.send_message(message.chat.id, result)
    elif request == "все":
        send_help(message)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def schedule_send_link(lesson_number):
    for lesson in schedule_list[week_type][weekday][lesson_number]:
        bot.send_message(CHAT_ID, f"📆 За 5 хвилин пара \"{lesson[0]}: {lesson[1]}\"")


if __name__ == "__main__":
    i = 0
    lessons_number = len(schedule_list[week_type][weekday])

    while lessons_number > i:
        schedule.every().day.at(reminder_times[i]).do(schedule_send_link, i)
        i += 1

    Thread(target=schedule_checker).start()

bot.infinity_polling()
