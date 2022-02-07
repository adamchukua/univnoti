from tgtoken import TOKEN
from lessons import lessons
from scheduleList import scheduleList
from reminderTimes import reminderTimes
import telebot
import datetime
import schedule
from threading import Thread
from time import sleep

bot = telebot.TeleBot(TOKEN)
typeOfWeek = (datetime.datetime.today().isocalendar()[1] - datetime.date(2021, 10, 29).isocalendar()[1]) % 2
dayOfWeek = datetime.datetime.today().weekday()

weekdays = {
    0: "Понеділок",
    1: "Вівторок",
    2: "Середа",
    3: "Четвер",
    4: "П'ятниця",
    5: "Субота",
    6: "Неділя"
}


def day_lessons(day):
    result = "*" + weekdays[day] + " (тиждень " + str(typeOfWeek + 1) + ")*\n\n"
    i = 1

    if len(scheduleList[typeOfWeek][day]) > 0:
        for lesson in scheduleList[typeOfWeek][day]:
            if len(lesson) > 0:
                result += str(i) + ". " + lesson[0][0] + " - " + lesson[0][1] + "\n"
            i += 1
    else:
        result = "Нічого немає, чіллим... Жартую, у вас курсова."

    return result


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Цей бот нагадує про пари.")


@bot.message_handler(commands=["help"])
def send_help(message):
    commands = "*Посилання на пари*\n\n"

    for lesson in lessons:
        commands += "`!" + lesson + "` - " + lessons[lesson][0].lower() + "\n"

    commands += "\n*Розклад*\n\n" \
                "`!сьогодні` - дізнатися розклад на сьогодні\n" \
                "`!завтра` - дізнатися розклад на завтра"

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
        bot.send_message(message.chat.id, day_lessons(dayOfWeek),
                         parse_mode="Markdown",
                         disable_web_page_preview=True)
    elif request == "завтра" or request == "з":
        bot.send_message(message.chat.id, day_lessons((dayOfWeek + 1) % 7),
                         parse_mode="Markdown",
                         disable_web_page_preview=True)
    elif request == "все":
        send_help(message)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def schedule_send_link(i):
    return bot.send_message(-1001637467506,
                            "📆 Через 5 хвилин пара \"" +
                            scheduleList[typeOfWeek][dayOfWeek][i][0][0] +
                            "\": " +
                            scheduleList[typeOfWeek][dayOfWeek][i][0][1])


if __name__ == "__main__":
    i = 0
    numberOfLessons = len(scheduleList[typeOfWeek][dayOfWeek])

    while numberOfLessons > i - 1:
        schedule.every().day.at(reminderTimes[i]).do(schedule_send_link, i)
        i += 1

    Thread(target=schedule_checker).start()

bot.infinity_polling()
