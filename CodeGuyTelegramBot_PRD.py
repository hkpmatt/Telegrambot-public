#!/usr/bin/env python
# coding: utf-8

# In[1]:

import logging
from telegram import Update, Bot, Message, Chat, User
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Updater, MessageHandler, filters, InlineQueryHandler
import nest_asyncio
import string
import re
import datetime
import csv, os
from dotenv import load_dotenv

load_dotenv()
nest_asyncio.apply()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

hellotxt=("以下係我哋有嘅服務:\n\n"
"- Programming (C++, Python, Java , shell script, R, SQL)\n"
"- Machine Learning & theory(Pytorch, Tensorflow, sk-learn…)\n"
"- Data Preparing & Cleaning\n"
"- Data crawling\n"
"- Database (Oracle SQL, MySQL, SAS…)\n"
"- Visualization (Seaborn, geoplotlib, Matplotlib, R, Tableau…)\n"
"- 3D-model (Fusion360, Blender)\n"
"- Automation (telegrambot, webbot)\n"
"- Personal use GPT (Huggingface, LangChain)\n\n"

"請寫低你需要嘅服務\n"
"我哋好快會專人回覆你\n")

csv_file_path = 'data.csv'
grpchatid = os.getenv('grpchatid')
token = os.getenv('token')

# Check if the CSV file exists
if not os.path.exists(csv_file_path):
    # Create the CSV file
    with open(csv_file_path, 'w', newline='', encoding="UTF-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['date', 'first_name', 'id', 'forward_date', 'forward_sender_name'])
else: 
    pass

def count_occur(input_string):
    occurrence_count = 0
    index = -1
    while occurrence_count < 3:
        index = input_string.find(", tzinfo=", index + 1)
        if index == -1:
            break
        occurrence_count += 1

    if occurrence_count == 3:
       return index

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAANMZQfvauP78C6jKOwMapJnwC2QOIoAAmUTAAJ-exlJdL4IQXS3XZ0wBA')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Fast Gunner 有咩可以幫到你？\n 撳 /hello 睇吓我哋嘅服務list")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=hellotxt)

async def help1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/start - 介紹 Introduction\n/hello - 服務 Services")
    
async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        #forward message's user name and datetime from hidden user
        print(update.message)
        code = str(update.message)
        forward_sender_name_first = code.find("forward_sender_name='")+len(("forward_sender_name='"))
        forward_sender_name_end = code.find("', from_user=User")
        forward_sender_name = code[forward_sender_name_first:forward_sender_name_end]
        print(forward_sender_name)
        forward_date_start = date_start = code.find("forward_date=datetime.datetime(")+len("forward_date=datetime.datetime(")
        print(forward_date_start)
        forward_date_end = count_occur(code)
        print(forward_date_end)
        forward_date_str = code[forward_date_start:forward_date_end]
        print(forward_date_str)
        forward_date_tuple = tuple(map(int, forward_date_str.split(", ")))
        print('hidden: ',forward_sender_name,forward_date_tuple)
        date_tuple=None
        first_name=None
        id_value=None
        data_row=[]
        
        if date_tuple:
            data_row.append(date_tuple)
        else:
            data_row.append('')
        if first_name:
            data_row.append(first_name)
        else:
            data_row.append('')
        if id_value:
            data_row.append(id_value)
        else:
            data_row.append('')
        if forward_date_tuple:
            data_row.append(forward_date_tuple)
        else:
            data_row.append('')
        if forward_sender_name:
            data_row.append(forward_sender_name)
        else:
            data_row.append('')
        with open(csv_file_path, 'a', newline='', encoding="UTF-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_row)
            
        found_id_value = None
        with open(csv_file_path, 'r', encoding="UTF-8") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header row
            
            for row in csv_reader:
                date_tuple = eval(row[0]) if row[0] else None
                first_name = row[1]
                id_value = row[2]

                # Check if the record matches the search criteria
                if str(date_tuple) == str(forward_date_tuple) and str(first_name) == str(forward_sender_name):
                    print("found")
                    found_id_value = id_value
                    break
        await context.bot.copy_message(chat_id=found_id_value, from_chat_id=grpchatid, message_id=update.effective_message.id)
        
    except:
        #user to bot info with datetime user name and chatid
        print(update.message)
        code = str(update.message)
        date_start = code.find("date=datetime.datetime(") + len("date=datetime.datetime(")
        date_end = code.find(", tzinfo=")
        date_str = code[date_start:date_end]
        print(date_start,date_end,date_str)
        date_tuple = tuple(map(int, date_str.split(", ")))
        first_name = re.search(r"first_name='([^']*)'", code).group(1)
        id_value = int(re.search(r"id=(\d+)", code).group(1))
        print("nonhidden: ",date_tuple,first_name,id_value)
        forward_date_tuple=None
        forward_sender_name=None
        data_row=[]
        
        if date_tuple:
            data_row.append(date_tuple)
        else:
            data_row.append('')
        if first_name:
            data_row.append(first_name)
        else:
            data_row.append('')
        if id_value:
            data_row.append(id_value)
        else:
            data_row.append('')
        if forward_date_tuple:
            data_row.append(forward_date_tuple)
        else:
            data_row.append('')
        if forward_sender_name:
            data_row.append(forward_sender_name)
        else:
            data_row.append('')
        with open(csv_file_path, 'a', newline='', encoding="UTF-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_row)
        
        if (update.effective_chat.id!=int(grpchatid)): #forward msg to grp"
            await context.bot.forward_message(chat_id=grpchatid, from_chat_id=update.effective_chat.id, message_id=update.effective_message.id)
    try:
        #direct reply to user if user is not hidden  
        code = str(update.effective_message.reply_to_message)
        id_value = nonhidden(code)
        if (id_value!= grpchatid):
            await context.bot.copy_message(chat_id=id_value, from_chat_id=grpchatid, message_id=update.effective_message.id)
    except:
        pass
        


def nonhidden(code):
    forward_from_start = code.find("forward_from=User(") + len("forward_from=User(")
    forward_from_end = code.find(", from_user=")
    forward_from_str = code[forward_from_start:forward_from_end]
    id_start = forward_from_str.find("id=") + len("id=")
    id_end = forward_from_str.find(",", id_start)
    return forward_from_str[id_start:id_end]
    

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE,):
    text = ' '.join(context.args[1:])
    
    await context.bot.send_message(chat_id= context.args[0], text=text)


    
if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    updates = Update
    #Handler
    start_handler = CommandHandler('start', start)
    hello_handler = CommandHandler('hello', hello)
    forward_handler = MessageHandler( filters.TEXT and (~filters.COMMAND) or filters.REPLY or filters.PHOTO or filters.AUDIO, forward)  
    reply_handler = CommandHandler('reply', reply)
    help_handler = CommandHandler('help', help1)
    #add_handler
    application.add_handler(start_handler)
    application.add_handler(reply_handler)
    application.add_handler(help_handler)
    application.add_handler(forward_handler)
    application.add_handler(hello_handler)
    
    application.run_polling()






