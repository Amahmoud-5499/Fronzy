import webbrowser
import linearwinvolume as lv
import pyscreenshot
import os
import ctypes
from shlex import quote
import subprocess
import psutil
import platform

from telegram.update import Update
from telegram.ext.messagehandler import MessageHandler
from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.ext.filters import Filters
from telegram.ext.callbackcontext import CallbackContext
from decouple import config

# the needed data you should have it in .env file like TOKEN and username
API_KEY = config("token")
USERNAME = config("user")
updater = Updater(API_KEY, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello, how can i help you /help to see commands")


def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text(f"This command {update.message.text} is not available")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("this is help command")

# Define a function to handle the /status command
def status(update, context):
    # Get system information using psutil and platform
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    system = platform.system()
    release = platform.release()
    processor = platform.processor()

    # Format the system information as a string
    message = f"CPU usage: {cpu_percent}%\nRAM usage: {ram_percent}%\nDisk usage: {disk_percent}%\nSystem: {system}\nRelease: {release}\nProcessor: {processor}"

    # Send the system information to the user
    update.message.reply_text(message)

def unknown_text(update: Update, context: CallbackContext):
    print(config("user"))
    if update.message.from_user['username'] == USERNAME:
        msg = update.message.text.lower()
        if msg in ["hello", "hi", ]:
            update.message.reply_text("hi sir, welcome to Fronzy")
        elif msg == "youtube":
            webbrowser.open("www.youtube.com")
            update.message.reply_text("opening youtube")
        elif msg == "screenshot":
            path = "screenshot.png"
            img = pyscreenshot.grab()
            img.save(path)
            update.message.reply_photo(open(path, 'rb'), caption="here is your screenshot")
            os.remove(path)
        elif msg == "close keyboard":
            reply_markup = ReplyKeyboardRemove()
            update.message.reply_text(reply_markup=reply_markup, text="keyboard down")
        elif msg == "shutdown":
            subprocess.run('shutdown /s')
            text = "Shut down."
            update.message.reply_text(text=text)
        elif msg == "lock":
            ctypes.windll.user32.LockWorkStation()
            text = "PC locked."
            update.message.reply_text(text=text)
        elif msg == "sleep":
            subprocess.call(["C:\\Windows\\System32\\rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"])
            text = "PC in sleep mode."
            update.message.reply_text(text=text)
        elif msg == "mute":
            lv.set_volume(0)
            update.message.reply_text("currently is muted")

    else:
        update.message.reply_text("This is a private bot for personal use")


def launch(update: Update, context: CallbackContext):
    if context.args:
        ret = subprocess.run("start %s" % quote(context.args[0]), shell=True).returncode
        text = "Launching " + (context.args[0]) + "..."
        update.message.reply_text(text=text)
        if ret != 0:
            text = "Cannot launch " + (context.args[0])
            update.message.reply_text(text=text)
    else:
        update.message.reply_text(text="write name of app after /launch")


def volume(update: Update, context: CallbackContext):
    lv.set_volume(int(context.args[0]))


def keyboard(update: Update, context: CallbackContext):
    keyboard = [["screenshot", "youtube", "mute"],
                ["shutdown", "lock", "sleep"],
                ["close Keyboard"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(reply_markup=reply_markup, text="keyboard is up")


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("keyboard", keyboard))
updater.dispatcher.add_handler(CommandHandler("launch", launch))
updater.dispatcher.add_handler(CommandHandler("volume", volume))
updater.dispatcher.add_handler(CommandHandler('status', status))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
print("bot is working")
updater.idle()
