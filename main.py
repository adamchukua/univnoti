import telebot
import datetime
import schedule
import tgtoken
from threading import Thread
from time import sleep

bot = telebot.TeleBot(tgtoken.TOKEN)
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

times = [
    "08:55",
    "10:25",
    "12:25",
    "13:55",
    "15:25",
    "16:55",
    "18:25"
]

lessons = {
    "англ": ["Англійська мова", "meet.google.com/ygy-phic-sia"],
    "кгозл": ["Комп'ютерна графіка та обробка зображень (лекція)", "meet.google.com/cat-tnso-ydp"],
    "кгозп": ["Комп'ютерна графіка та обробка зображень (практика)", "постійне посилання відсутнє"],
    "веб": ["Web-програмування", "meet.google.com/cat-tnso-ydp"],
    "ткпл": ["Технології комп'ютерного проєктування (лекція)", "meet.google.com/tue-zwcs-wtc"],
    "ткпп": ["Технології комп'ютерного проєктування (практика)", "meet.google.com/xui-xeti-obn"],
    "алгл": ["Алгоритми та структури даних (лекція)", "meet.google.com/wzr-abyj-bas"],
    "алгп": ["Алгоритми та структури даних (практика)", "meet.google.com/abx-gsop-fey"],
    "ооп": ["Об'єктно-орієнтоване проєктування", "meet.google.com/yjv-qxit-wfx"],
    "тймсл": ["Теорія ймовірності та математична статистика (лекція)", "постійне посилання відсутнє"],
    "тймсп": ["Теорія ймовірності та математична статистика (практика)", "постійне посилання відсутнє"],
    "нп": ["Нефаховий предмет", "постійне посилання відсутнє"],
    "фв": ["Фізичне виховання", "постійне посилання відсутнє"]
}

scheduleList = [
    [
        [
            [
                lessons["алгп"]
            ],
            [
                lessons["ткпп"]
            ],
            [
                lessons["веб"]
            ]
        ],
        [],
        [
            [
                lessons["ткпл"]
            ],
            [
                lessons["алгл"]
            ],
            [
                lessons["ооп"]
            ]
        ],
        [
            [
                lessons["кгозп"]
            ],
            [
                lessons["веб"]
            ],
            [
                lessons["нп"]
            ]
        ],
        [
            [
                lessons["ооп"]
            ],
            [
                lessons["англ"]
            ],
            [
                lessons["ткпп"]
            ],
            [
                lessons["фв"]
            ]
        ],
        [],
        []
    ],
    [
        [
            [
                lessons["алгп"]
            ],
            [
                lessons["тймсп"]
            ],
            [
                lessons["веб"]
            ]
        ],
        [],
        [
            [
                lessons["тймсл"]
            ],
            [
                lessons["алгл"]
            ],
            [
                lessons["ооп"]
            ]
        ],
        [
            [],
            [
                lessons["кгозл"]
            ],
            [
                lessons["нп"]
            ],
            [
                lessons["нп"]
            ]
        ],
        [
            [
                lessons["ооп"]
            ],
            [
                lessons["англ"]
            ],
            [
                lessons["ткпп"]
            ],
            [
                lessons["фв"]
            ]
        ],
        [],
        []
    ]
]


def day_lessons(day):
    result = "*" + weekdays[day] + " (тиждень " + str(typeOfWeek + 1) + ")*\n\n"
    i = 1

    if len(scheduleList[typeOfWeek][day]) > 0:
        for lesson in scheduleList[typeOfWeek][day]:
            try:
                result += str(i) + ". " + lesson[0][0] + " - " + lesson[0][1] + "\n"
            except:
                print("error: a lesson doesn't exist")
            i += 1
    else:
        result = "Нічого немає, чіллим... Жартую, у вас курсова."

    return result


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Цей бот нагадує про пари.")


@bot.message_handler(func=lambda message: True)
def main(message):
    request = message.text.lower()[1:]

    if request in lessons:
        bot.send_message(message.chat.id, lessons[request][1])
    elif request == "сьогодні":
        bot.send_message(message.chat.id, day_lessons(dayOfWeek),
                         parse_mode="Markdown",
                         disable_web_page_preview=True)
    elif request == "завтра":
        bot.send_message(message.chat.id, day_lessons((dayOfWeek + 1) % 7),
                         parse_mode="Markdown",
                         disable_web_page_preview=True)
    elif request == "все":
        all = "*Посилання на пари*\n\n"

        for lesson in lessons:
            all += "`!" + lesson + "` - " + lessons[lesson][0].lower() + "\n"

        all += "\n*Розклад*\n\n" \
               "`!сьогодні` - дізнатися розклад на сьогодні\n" \
               "`!завтра` - дізнатися розклад на завтра"

        bot.send_message(message.chat.id, all,
                         parse_mode="Markdown",
                         disable_web_page_preview=True)


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
    if len(scheduleList[typeOfWeek][dayOfWeek]) > 0:
        schedule.every().day.at(times[0]).do(schedule_send_link, 0)
        schedule.every().day.at(times[1]).do(schedule_send_link, 1)
        schedule.every().day.at(times[2]).do(schedule_send_link, 2)
        schedule.every().day.at(times[3]).do(schedule_send_link, 3)
        schedule.every().day.at(times[4]).do(schedule_send_link, 4)
        schedule.every().day.at(times[5]).do(schedule_send_link, 5)
        schedule.every().day.at(times[6]).do(schedule_send_link, 6)

    Thread(target=schedule_checker).start()

bot.infinity_polling()