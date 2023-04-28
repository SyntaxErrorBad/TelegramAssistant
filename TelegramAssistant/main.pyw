import telebot
import time
import os
import pyautogui
import openai
import psutil


from SQL.DataSQL import *
from config import *
from Process import *

bot = telebot.TeleBot(BOT_TOKEN,skip_pending=True)
openai.api_key = GPT_TOKEN


@bot.message_handler(commands=['start'])
def start(message):
    if DataBase().CheckUser(ID = message.from_user.id):
        #If not in DataBase
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Yes", "No")
        bot.send_message(message.chat.id,"You don't have Account! Create?",reply_markup=keyboard)
        bot.register_next_step_handler(message,Quest_Login)
    else:
        Login,Root = DataBase().RegisterUser(ID=message.from_user.id)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row(f"{Login}")
        bot.send_message(message.chat.id,"You wellcome!",reply_markup=keyboard)
        bot.register_next_step_handler(message,BotStartWork,Login=Login,Root=Root)

@bot.message_handler(content_types = ['text'])
def CheckUserBot(message):
    if DataBase().CheckUser(ID = message.from_user.id):
        #If not in DataBase
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Yes", "No")
        bot.send_message(message.chat.id,"You don't have Account! Create?",reply_markup=keyboard)
        bot.register_next_step_handler(message,Quest_Login)
    else:
        Login,Root = DataBase().RegisterUser(ID=message.from_user.id)
        bot.send_message(message.chat.id,f"You wellcome {Login}!",reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message,ControlText,Root = Root,keybd = True)

def Quest_Login(message):
    if message.text == "Yes":
        #If want to create an account
        bot.send_message(message.chat.id,"Enter your login: ")
        bot.register_next_step_handler(message,LoginUser)
    else:
        bot.send_message(message.chat.id,"Error! You need to prees only YES!")
        bot.register_next_step_handler(message,start)

def LoginUser(message):
    if DataBase().LoginUser(Login=message.text):
        #if login not in DataBase
        bot.send_message(message.chat.id,"Enter your correct login: ")
        bot.register_next_step_handler(message,LoginUser)
    else:
        #if login in DataBase
        bot.send_message(message.chat.id,"Enter your password: ")
        bot.register_next_step_handler(message,PasswordUser,Login = message.text)

def PasswordUser(message,Login):
    if message.text != "<- BACK ->":
        if DataBase().LoginPassword(Login=Login,Password=message.text):
            #if password correct
            Root = DataBase().LoginAccount(Login=Login,Password=message.text,ID=message.from_user.id,Time=message.date)
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row(f"{Login}")
            bot.send_message(message.chat.id,"You wellcome!",reply_markup=keyboard)
            bot.register_next_step_handler(message,BotStartWork,Login=Login,Root=Root)
        else:
            #if password uncorrect
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Password uncorrect!', reply_markup = keyboard)
            bot.register_next_step_handler(message, PasswordUser,Login = Login)

    elif message.text == "<- BACK ->":
        bot.send_message(message.chat.id,"Enter your correct login: ")
        bot.register_next_step_handler(message,LoginUser)

#MENU HELP
def MENU(Root):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    if Root == "0":
        keyboard.row("Power OFF","Change Brightness")
        keyboard.row("Screenshot","Power off Add")
        keyboard.row("ChatGPT","Block Keyboard")
        #keyboard.row("Dowbload video/audio","Write text")
        keyboard.row("Write text","Account Control")
        keyboard.row("Change account")
        return keyboard
    elif Root == "1":
        keyboard.row("ChatGPT")
        keyboard.row("Change account")
        return keyboard

#Start Code
def BotStartWork(message,Login,Root):
    if Root == "0":
        bot.send_message(message.chat.id, f'Choose action {Login}!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = True)
    elif Root == "1":
        bot.send_message(message.chat.id, f'Choose action {Login}!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = True)
    else:
        pass

def ControlText(message,Root,keybd):
    if Root == "0":
        if message.text == "Power OFF":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Yes","No")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Please choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, ControlInfo,Func = ''.join(message.text),Root = Root,keybd = keybd)

        elif message.text == "Screenshot":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Yes","No")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Please choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, ControlInfo,Func = ''.join(message.text),Root = Root,keybd = keybd)

        elif message.text == "Power off Add":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Yes","No")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Please choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, ControlInfo,Func = ''.join(message.text),Root = Root,keybd = keybd)

        elif message.text == "ChatGPT":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Yes","No")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Please choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, ControlInfo,Func = ''.join(message.text),Root = Root,keybd = keybd)

        elif message.text == "Block Keyboard":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Yes","No")
            keyboard.row("<- BACK ->")
            if keybd:
                Blocked = "UnBlocked"
            else:
                Blocked = "Blocked"
            bot.send_message(message.chat.id, f'Please choose action!Now keyboard {Blocked}', reply_markup=keyboard)
            bot.register_next_step_handler(message, ControlInfo,Func = ''.join(message.text),Root = Root,keybd = keybd)

        elif message.text == "Change Brightness":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Please choose perfents!', reply_markup=keyboard)
            bot.register_next_step_handler(message, Brightness,Root = Root,keybd = keybd)
        
        elif message.text == "Dowbload video/audio":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Video","Audio")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Please choose format!', reply_markup=keyboard)
            bot.register_next_step_handler(message, Check_Format_YT,Root = Root,keybd = keybd)
        
        elif message.text == "Write text":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Write text please!', reply_markup=keyboard)
            bot.register_next_step_handler(message, Write_Text,Root = Root,keybd = keybd)
        
        elif message.text == "Account Control":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Add Account","Remove Account")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, AccountsST,Root = Root,keybd = keybd)
        
        elif message.text == "Change account":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Yes","No")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Do you agree?', reply_markup=keyboard)
            bot.register_next_step_handler(message, Change_Account,Root = Root,keybd = keybd)

    elif Root == "1":
        if message.text == "ChatGPT":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Yes","No")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Please choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, ControlInfo,Func = ''.join(message.text),Root = Root,keybd = keybd)

        elif message.text == "Change account":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Yes","No")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Do you agree?', reply_markup=keyboard)
            bot.register_next_step_handler(message, Change_Account,Root = Root,keybd = keybd)
        
    else:
        bot.send_message(message.chat.id, 'Something wrong!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

def ControlInfo(message,Func,Root,keybd):
    if message.text == "Yes":
        Func = (''.join(Func)).replace(" ","_")

        if Func == "Power_off_Add":
            Power_off_Add(Proc = None,Root=Root,keybd=keybd)
        elif Func == "ChatGPT":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Write Picture")
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Enter you words!',reply_markup = keyboard)
            bot.register_next_step_handler(message, ChatGPT,Root = Root,messages_bot = None,keybd=keybd)

        elif Func == "Block_Keyboard":
            info = getattr(TelegramProcess(message,Root,bot), Func)(keybd)
            if keybd:
                Blocked = "Blocked"
            else:
                Blocked = "UnBlocked"

            bot.send_message(message.chat.id, f'KeyBoard {Blocked}', reply_markup=MENU(Root=Root))
            bot.register_next_step_handler(message, ControlText,Root = Root,keybd = info)

        else:
            getattr(TelegramProcess(message,Root,bot), Func)()
            bot.send_message(message.chat.id, 'The process is finished!', reply_markup=MENU(Root=Root))
            bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)


    elif message.text == "No":
        bot.send_message(message.chat.id, 'In the future, take your time!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

    elif message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'Ok,no problem!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Yes","No")
        keyboard.row("<- BACK ->")
        bot.send_message(message.chat.id, 'Something went wrong!Please choose again!', reply_markup=keyboard)
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)










#Process
def Power_Kill_Add(message,Proc,Root,keybd):
    if message.text in Proc:
        for process in psutil.process_iter(['pid', 'name']):
            if process.name() == message.text:
                process.kill()
        bot.send_message(message.chat.id, 'Please choose action!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    elif message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'Please choose action!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    else:
        bot.send_message(message.chat.id, 'Something went wrong!')
        Power_off_Add(Proc = Proc,Root = Root)


def ChatGPT(message,messages_bot,Root,keybd):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    if message.text != "<- BACK ->":
        if message.text != "Write Picture":
            if messages_bot == None:
                messages_bot = []
                messages_bot.append({"role": "user", "content": message.text})
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_bot)
                messages_bot.append({"role": "assistant", "content": completion.choices[0].message.content})
                keyboard.row("<- BACK ->")
                bot.send_message(message.chat.id, completion.choices[0].message.content)
                bot.send_message(message.chat.id, 'Wait for your next question!', reply_markup=keyboard)
                bot.register_next_step_handler(message, ChatGPT,Root = Root,messages_bot = messages_bot,keybd = keybd)

            else:
                messages_bot.append({"role": "user", "content": message.text})
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_bot)
                messages_bot.append({"role": "assistant", "content": completion.choices[0].message.content})
                keyboard.row("<- BACK ->")
                bot.send_message(message.chat.id, completion.choices[0].message.content)
                bot.send_message(message.chat.id, 'Wait for your next question!', reply_markup=keyboard)
                bot.register_next_step_handler(message, ChatGPT,Root = Root,messages_bot = messages_bot,keybd = keybd)
        else:
            keyboard.row("<- BACK ->")
            bot.send_message(message.chat.id, 'Write the theme of the pictures!', reply_markup=keyboard)
            bot.register_next_step_handler(message, ChatGPTPicture,Root = Root,keybd = keybd)

    elif message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'Please choose action!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)



def Power_off_Add(message,Proc,Root,keybd):
    if Proc == None:
        Proc = []
        for proc in psutil.process_iter(['pid', 'name','exe']):
            if not any(proc.info['name'].startswith(sysproc) for sysproc in system_processes):
                if not any(str(proc.info['exe']).startswith(syspath) for syspath in proc_list):
                    if proc.info['name'] not in Proc:
                        Proc.append(proc.info['name'])
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    proc_num = 0
    while proc_num < len(Proc):
        if proc_num + 1 < len(Proc):
            keyboard.row(Proc[proc_num], Proc[proc_num+1])
            proc_num += 2
        else:
            keyboard.row(Proc[proc_num])
            proc_num += 1
    keyboard.row("<- BACK ->")
    bot.send_message(message.chat.id, 'Please choose Application!', reply_markup=keyboard)
    bot.register_next_step_handler(message, Power_Kill_Add,Root = Root,Proc = Proc,keybd=keybd)

def Brightness(message,Root,keybd):
    if message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'Ok', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    else:
        try:
            sbc.set_brightness(int(message.text))
            bot.send_message(message.chat.id, 'Complete', reply_markup=MENU(Root=Root))
            bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

        except:
            bot.send_message(message.chat.id, 'Something has gone wrong!', reply_markup=MENU(Root=Root))
            bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

def Check_Format_YT(message,Root,keybd):
    if message.text == "Audio":
        bot.send_message(message.chat.id, "Ok, give me url!")
        bot.register_next_step_handler(message, Give_Url_YT,Root = Root,keybd = keybd,Format = message.text)
    elif message.text == "Video":
        bot.send_message(message.chat.id, "Ok, give me url!")
        bot.register_next_step_handler(message, Give_Url_YT,Root = Root,keybd = keybd,Format = message.text)
    elif message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'No Problem', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Audio","Video")
        keyboard.row("<- BACK ->")
        bot.send_message(message.chat.id, 'Something has gone wrong!', reply_markup=keyboard)
        bot.register_next_step_handler(message, Check_Format_YT,Root = Root,keybd = keybd)

def Give_Url_YT(message,Root,keybd,Format):
    if message.text != "<- BACK ->":
        try:
            """Мдааааа"""
            print("Попиточка")
            bot.send_message(message.chat.id, 'ОК', reply_markup=MENU(Root=Root))
            bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
        except:
            bot.send_message(message.chat.id, 'Something has gone wrong!')
            bot.register_next_step_handler(message, Give_Url_YT,Root = Root,keybd = keybd,Format = Format)
    else:
        bot.send_message(message.chat.id, 'No Problem', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

def Write_Text(message,Root,keybd):
    try:
        if message.text != "<- BACK ->":
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Add Text","Remove Text")
            keyboard.row("Press Enter","<- BACK ->")
            TelegramProcess(bot = bot, Root=Root,message=message.text).Write_Text_Keyboard(Text = "Add Text")
            bot.send_message(message.chat.id, 'Choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, Write_Text_Add,Root = Root,keybd = keybd)

        else:
            bot.send_message(message.chat.id, 'Ok! Choose action!', reply_markup=MENU(Root=Root))
            bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    except:
        bot.send_message(message.chat.id, 'Something wrong!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

def Write_Text_Add(message,Root,keybd):
    if message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'Ok! Choose action!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

    elif message.text == "Add Text":
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Remove Text")
        keyboard.row("Press Enter","<- BACK ->")
        bot.send_message(message.chat.id, 'Add text please!', reply_markup=keyboard)
        bot.register_next_step_handler(message, Text_Process,Root = Root,keybd = keybd)

    elif message.text == "Remove Text":
        TelegramProcess(bot=bot,message=message.text,Root=Root).Write_Text_Keyboard(Text = "Remove Text")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Add Text","Remove Text")
        keyboard.row("Press Enter","<- BACK ->")
        bot.send_message(message.chat.id, 'Ok! Choose action!', reply_markup=keyboard)
        bot.register_next_step_handler(message, Text_Process,Root = Root,keybd = keybd)

    elif message.text == "Press Enter":
        TelegramProcess(bot=bot,message=message.text,Root=Root).Write_Text_Keyboard(Text = "Press Enter")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Add Text","Remove Text")
        keyboard.row("Press Enter","<- BACK ->")
        bot.send_message(message.chat.id, 'Ok! Choose action!', reply_markup=keyboard)
        bot.register_next_step_handler(message, Text_Process,Root = Root,keybd = keybd)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Add Text","Remove Text")
        keyboard.row("Press Enter","<- BACK ->")
        TelegramProcess(bot = bot, Root=Root,message=message.text)
        bot.send_message(message.chat.id, 'Please! Choose action!', reply_markup=keyboard)
        bot.register_next_step_handler(message, Write_Text_Add,Root = Root,keybd = keybd)

def Text_Process(message,Root,keybd):
    try:
        if message.text == "<- BACK ->":
            bot.send_message(message.chat.id, 'Ok! Choose action!', reply_markup=MENU(Root=Root))
            bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
        elif message.text == "Remove Text":
            TelegramProcess(bot=bot,message=message.text,Root=Root).Write_Text_Keyboard(Text = "Remove Text")
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Add Text","Remove Text")
            keyboard.row("Press Enter","<- BACK ->")
            bot.send_message(message.chat.id, 'Ok! Choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, Write_Text_Add,Root = Root,keybd = keybd)
        elif message.text == "Press Enter":
            TelegramProcess(bot=bot,message=message.text,Root=Root).Write_Text_Keyboard(Text = "Press Enter")
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Add Text","Remove Text")
            keyboard.row("Press Enter","<- BACK ->")
            bot.send_message(message.chat.id, 'Ok! Choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, Write_Text_Add,Root = Root,keybd = keybd)
        else:
            TelegramProcess(bot=bot,message=message.text,Root=Root).Write_Text_Keyboard(Text = "Add Text")
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("Add Text","Remove Text")
            keyboard.row("Press Enter","<- BACK ->")
            bot.send_message(message.chat.id, 'Ok! Choose action!', reply_markup=keyboard)
            bot.register_next_step_handler(message, Write_Text_Add,Root = Root,keybd = keybd)
    except:
        bot.send_message(message.chat.id, 'Something wrong!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)


#AccoutnsWork
def AccountsST(message,Root,keybd):
    #keyboard.row("Add Admin Account","Add User Account")
    if message.text == "Add Account":
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("<- BACK ->")
        bot.send_message(message.chat.id, 'Please write Login', reply_markup=keyboard)
        bot.register_next_step_handler(message, Accounts_Work,Root = Root,keybd = keybd,Login = None,Password = None,Roots = None)

    elif message.text == "Remove Account":
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        account_list = DataBase().DataBaseList()
        for account in account_list:
            keyboard.row(f"{'  :  '.join(account)}")
        keyboard.row("<- BACK ->")
        bot.send_message(message.chat.id, 'Please choose account', reply_markup=keyboard)
        bot.register_next_step_handler(message, Accounts_Remove,Root = Root,keybd = keybd,account_list=account_list)

    elif message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'Thanks for work!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    else:
        bot.send_message(message.chat.id, 'Something wrong!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

def Accounts_Work(message,Root,keybd,Login,Password,Roots):
    if message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'Thanks for work!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    else:
        if Login == None:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("<- BACK ->")
            Login = str(message.text)
            bot.send_message(message.chat.id, 'Please write Password', reply_markup=keyboard)
            bot.register_next_step_handler(message, Accounts_Work,Root = Root,keybd = keybd,Login = Login,Password = None,Roots = None)
        elif Password == None:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row("<- BACK ->")
            Password = str(message.text)
            bot.send_message(message.chat.id, 'Please write Root', reply_markup=keyboard)
            bot.register_next_step_handler(message, Accounts_Work,Root = Root,keybd = keybd,Login = Login,Password = Password,Roots = None)
        elif Roots == None:
            Roots = str(message.text)
            if DataBase().AddDataBase(login=Login,password=Password,root=Roots):
                bot.send_message(message.chat.id, 'All good', reply_markup=MENU(Root=Root))
                bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
            else:
                bot.send_message(message.chat.id, 'Something wrong!', reply_markup=MENU(Root=Root))
                bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

def Accounts_Remove(message,Root,keybd,account_list):
    if message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'Thanks for work!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    else:
        try:
            text = str(message.text).split(" : ")
            DataBase().RemoveAccount(Login=text[0],Password=text[1])
            bot.send_message(message.chat.id, f'Account {message.text} delete!', reply_markup=MENU(Root=Root))
            bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
        except:
            bot.send_message(message.chat.id, 'Something wrong!', reply_markup=MENU(Root=Root))
            bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)


def Change_Account(message,Root,keybd):
    if message.text == "<- BACK ->" or message.text == "No":
        bot.send_message(message.chat.id, 'Thanks for work!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    elif message.text == "Yes":
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Yes","No")
        DataBase().LeaveAccount(ID=message.from_user.id)
        bot.send_message(message.chat.id, 'You leave from account! Want login?',reply_markup=keyboard)
        bot.register_next_step_handler(message, Quest_Login)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Yes","No")
        keyboard.row("<- BACK ->")
        bot.send_message(message.chat.id, 'Something wrong!', reply_markup=keyboard)
        bot.register_next_step_handler(message, Change_Account,Root = Root,keybd = keybd)


def ChatGPTPicture(message,Root,keybd):
    if message.text == "<- BACK ->":
        bot.send_message(message.chat.id, 'Thanks for work!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)
    else:
        image_resp = openai.Image.create(prompt=''.join(message.text), n=1, size="512x512")
        urls = []
        for img in image_resp["data"]:
            urls.append(img["url"])
        bot.send_message(message.chat.id,''.join(urls))
        bot.send_message(message.chat.id, 'Take url!', reply_markup=MENU(Root=Root))
        bot.register_next_step_handler(message, ControlText,Root = Root,keybd = keybd)

def main():
    bot.polling(none_stop=True)

while True:
    try:
        if __name__ == "__main__":
            main()
    except:
        time.sleep(30)
        main()