import time
import os
import telepot
from telepot.loop import MessageLoop
import pickle
import requests
import schedule
from datetime import datetime
import pandas as pd
import imgkit
from DBManager import DBManager
import json
from bs4 import BeautifulSoup as BS
from io import BytesIO
from zipfile import ZipFile



#config = imgkit.config(wkhtmltoimage='C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe')

try:
    adminKeyFile = open('adminKey.txt','r')
    adminKey = adminKeyFile.read()
except FileNotFoundError:
    adminKey = 'admin'

adminCommand = set()
waiting_for_adminKey = set()
bot = telepot.Bot("872205161:AAEAAbdCKxepLufosxtd63yr98eGqF3I8so")
url='https://api.data.gov.sg/v1/environment/psi'

db = DBManager('db.sqlite3')
    
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        bot.sendMessage(chat_id, 'Please input text')
        return
    
    if chat_id in adminCommand:
        if verify_admin(chat_id, msg):
            update(chat_id)
        return
            
    if msg['text'] == '/start':
        if not db.is_existed(chat_id):
            bot.sendMessage(chat_id, f"Welcome {msg['chat']['first_name']}, please input command to use my service")
        else:
            bot.sendMessage(chat_id, "You are already using my service before")
    elif msg['text'] == '/weekly_update':
        weekly_update(chat_id)
    elif msg['text'] == '/stop_receive_update':
        stop_receive_update(chat_id)
    elif msg['text'] == '/manual_update':
        manual_update(chat_id)
    else:
        bot.sendMessage(chat_id, "Unregconized command, please refer to the command list to choose")
    print(db.user_list())
    

def weekly_update(chat_id):
    if not db.is_existed(chat_id):
        db.add(chat_id)
        bot.sendMessage(chat_id, "Thank you for using my service, you will receive dengue and haze status update for every Monday or whenever my admin post any status update")
    else:
        bot.sendMessage(chat_id, "You are already using weekly_update service")

def stop_receive_update(chat_id):
    if db.is_existed(chat_id):
        db.delete(chat_id)
        bot.sendMessage(chat_id, "You will no longer receive any update")
    else:
        bot.sendMessage(chat_id, "You are currently not using my service")


def manual_update(chat_id):
    adminCommand.add(chat_id)
    bot.sendMessage(chat_id, "Please input admin key to verify your admin right")

def verify_admin(chat_id, msg):
    adminCommand.remove(chat_id)
    if msg['text'] == adminKey:
        bot.sendMessage(chat_id, "The dengue and haze status will now be updated to relevant users")
        return True

    else:
        bot.sendMessage(chat_id, "Invalid admin key, the manual_update is only for admin\nPlease choose another command")
        return False


def update(chat_id=-1):
    users = db.user_list()
    if users.__len__() == 0:
        if chat_id != -1:
            bot.sendMessage(chat_id, 'There is currently no users using my service')
        return
    for user_info in users:
        haze_photo = open('haze_status.png','rb')
        dengue_photo = open('dengue_status.png', 'rb')
        
        bot.sendMessage(user_info[0], 'HAZE STATUS will be summarized and displayed here shortly')
        bot.sendPhoto(user_info[0], haze_photo)
        bot.sendMessage(user_info[0], f"The table above shows the polution level of each region in each polution category\n(last updated: {haze_response['items'][0]['update_timestamp']})")

        bot.sendMessage(user_info[0], 'DENGUE STATUS will be summarized and displayed here shortly') 
        bot.sendPhoto(user_info[0], dengue_photo)
        bot.sendMessage(user_info[0], f"The table above shows the dengue clusters location and the coresponding case size\n(last updated: {today.isoformat()})")
        
def crawling_dengue_data(url='https://data.gov.sg/dataset/e7536645-6126-4358-b959-a02b22c6c473/download'):
    global today
    resp = requests.get(url).content
    zipfile = ZipFile(BytesIO(resp))
    
    dengue_data = json.load(zipfile.open('dengue-clusters-geojson.geojson', 'r'))
    dengue_status = {'LOCATION': [], 'CASE_SIZE': []}
    today = datetime.today().replace(microsecond=0)
    pickle.dump(today, open('today.obj','wb'))
    
    for feature in dengue_data['features']:
        soup = BS(feature['properties']['Description'], 'html.parser')
        iterator = soup.table.children
        while True:
            child = next(iterator)
            if child.th.string == 'LOCALITY':
                dengue_status['LOCATION'].append(child.td.string)
                break
        while True:
            child = next(iterator)
            if child.th.string == 'CASE_SIZE':
                dengue_status['CASE_SIZE'].append(child.td.string)
                break
    dengue_status = pd.DataFrame(dengue_status)
    text_file = open('dengue_status.html', 'w+')
    text_file.write(css)
    text_file.write(dengue_status.to_html())
    text_file.close()
    imgkit.from_file("dengue_status.html", "dengue_status.png", options=imgkitoptions) 

        
MessageLoop(bot, {'chat':handle}).run_as_thread()

schedule.every().monday.do(update)
schedule.every().day.do(crawling_dengue_data)

css = open('CSS.txt', 'r').read()

imgkitoptions = {"format": "png",
                 "crop-w": '700'}


global haze_response
global today

while True:
    if not os.path.isfile('D:/CZ3003 - SOFTWARE SYSTEM ANALYSIS & DESIGN/dengue_status.png'):
        crawling_dengue_data()
        today = pickle.load(open('today.obj','rb'))
    else:
        today_file = pickle.load(open('today.obj','rb'))
        today = datetime.today()
        if (today.year, today.month, today.day) != (today_file.year, today_file.month, today_file.day):
            crawling_dengue_data()
        else: today = today_file
    haze_response = requests.get(url).json()
    haze_status = {}
    haze_status = {'POLUTION_INDEX_TYPE': [],'WEST': [], 'NATIONAL': [], 'EAST': [], 'CENTRAL': [], 'SOUTH': [], 'NORTH': []}
    for index_type, info in haze_response['items'][0]['readings'].items():
        haze_status['POLUTION_INDEX_TYPE'].append(index_type.upper())
        for region, index_val in info.items():
            haze_status[region.upper()].append(index_val)
    haze_status = pd.DataFrame(haze_status)
    haze_status = haze_status[['POLUTION_INDEX_TYPE', 'WEST', 'NATIONAL', 'EAST', 'CENTRAL', 'SOUTH', 'NORTH']]
    text_file = open('haze_status.html', 'w+')
    text_file.write(css)
    text_file.write(haze_status.to_html())
    text_file.close()
    imgkit.from_file("haze_status.html", "haze_status.png", options=imgkitoptions)
    schedule.run_pending()
    time.sleep(43200)
        
            

    
