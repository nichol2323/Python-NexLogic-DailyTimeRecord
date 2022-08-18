#pip install pyTelegramBotAPI
#pip install pygsheets
#pip install pytz

# Imports
import telebot
import pygsheets
import pytz
from datetime import datetime

# Pygsheet Config
service_file = r'APIKEY.json'
gc = pygsheets.authorize(service_file=service_file)
sheetname = 'CvSU Interns Design, Development, and Management Reference Sheet | 2022'
sh = gc.open(sheetname)
wks = sh.worksheet_by_title('Time Logs')
wksnames = sh.worksheet_by_title('Authorized Interns')

# Telegram API Token
API_TOKEN = '5434114429:AAHW-aXVZtza22fBjb8-JvL0Wqax7DHIGTo'
bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

class User:
    def __init__(self, name):
        self.timein = name
        self.timeout = None

print("Running...")


# Start
@bot.message_handler(commands=['start'])
def process_start(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        bot.reply_to(message, "Daily Time Record BOT")
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')


# Help
@bot.message_handler(commands=['help'])
def process_help(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        bot.reply_to(message, "/timein --> for timing in\n/timeout --> for timing out\n/status --> to view information")
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')


# Timein
@bot.message_handler(commands=['timein'])   
def process_timein(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        try:
            now = datetime.now(pytz.timezone('Asia/Manila'))
            date_time = now.strftime("%H:%M")
            time = now.strftime("%H:%M")
            date = now.strftime('%m/%d/%y')
            chat_id = message.chat.id
            timein = message.text
            user = User(timein)
            user_dict[chat_id] = user
            user.timein = date_time
            
            if timein == "/timein":
                user_first_name = str(message.chat.first_name)
                user_last_name = str(message.chat.last_name)
                full_name = user_first_name + " "+ user_last_name
                grecord = wks.get_all_records()
                num = 2
                for i in range(len(grecord)):
                    num+=1
                    if full_name == grecord[i].get("Intern Name") and date == grecord[i].get("Date"):
                        bot.reply_to(message, f'You have already TIMED IN')
                        break
                else:
                    wks.update_value((num, 2), date)
                    wks.update_value((num, 3), full_name)
                    wks.update_value((num, 4), time)
                    bot.reply_to(message, f'Successfully timein on {str(date_time)}')

        except Exception as e:
            bot.reply_to(message, 'Something went wrong. Please try again')
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')

 
# Timeout
@bot.message_handler(commands=['timeout'])  
def process_timeout(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        try:
            now2 = datetime.now(pytz.timezone('Asia/Manila'))
            date_time2 = now2.strftime("%H:%M")
            time = now2.strftime("%H:%M")
            timeout = message.text 
            user = User(timeout)
            user.timeout = date_time2
            user_first_name = str(message.chat.first_name)
            user_last_name = str(message.chat.last_name)
            full_name = user_first_name + " "+ user_last_name
            
            date = now2.strftime('%m/%d/%y')

            if timeout == "/timeout":
                grecord = wks.get_all_records()
                num = 1
                for i in range(len(grecord)):
                    num += 1
                    if full_name == grecord[i].get("Intern Name") and date == grecord[i].get("Date") and grecord[i].get("OUT")== '':
                                          
                        wks.update_value((num,5),time)
                        bot.reply_to(message, f'Successfully timeout on {str(date_time2)}')
                        break
                    elif full_name == grecord[i].get("Intern Name") and date == grecord[i].get("Date") and grecord[i].get("OUT")!= '':
                        bot.reply_to(message, 'You have already TIMED OUT')

        except Exception as e:
            bot.reply_to(message, 'Something went wrong. Please try again')
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')


# Status
@bot.message_handler(commands=['status'])  
def process_status(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        user_first_name = str(message.chat.first_name) 
        user_last_name = str(message.chat.last_name)
        full_name = user_first_name + " "+ user_last_name
        now = datetime.now(pytz.timezone('Asia/Manila'))
        date = now.strftime('%m/%d/%y')
        grecord = wks.get_all_records()
        num = 1
        for i in range(len(grecord)):
            num += 1
            if full_name == grecord[i].get("Intern Name") and date == grecord[i].get("Date") and grecord[i].get("IN")!= '' and grecord[i].get("OUT")!= '':
                bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("IN")}\nTimeout: {grecord[i].get("OUT")}\nDuration: {grecord[i].get("Duration")}')
                break
            elif full_name == grecord[i].get("Intern Name") and date == grecord[i].get("Date") and grecord[i].get("IN")!= '' and grecord[i].get("OUT")== '':
                bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("IN")}\nTimeout: NONE\nDuration: NONE')
                break
        else:
            bot.reply_to(message, "You haven't TIMED IN yet today")
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')
        

# Secret Command
@bot.message_handler(commands=['secret'])
def process_secret_command(message):
    bot.reply_to(message, "Last Update: 8/5/2022")

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
