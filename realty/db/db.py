import asyncio
import os
import sqlite3
from datetime import datetime
import requests as requests
from realty.telegrambot import TelegramBot


class DataBase:
    def set_connection(self):
        try:
            connection = sqlite3.connect('../../realty22.db')
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE offers ('
                           'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           'price INTEGER,'
                           'title TEXT,'
                           'url TEXT,'
                           'geo TEXT,'
                           'offerDate TEXT,'
                           'date TEXT)')
            record = cursor.fetchall()
            cursor.execute('select* from offers')

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (connection):
                connection.commit()
                connection.close()
                print("Соединение с SQLite закрыто")

    def add_offers_to_db(self, offers):
        connection = sqlite3.connect('../realty22.db', isolation_level=None)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS offers ('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'price INTEGER,'
                       'title TEXT,'
                       'url TEXT,'
                       'geo TEXT,'
                       'offerDate TEXT,'
                       'date TEXT)')

        for entity in offers:
            price = entity['price']
            title = entity['title']
            url = entity['url']
            geo = entity['geo']
            offer_date = entity['offer_date']
            image = entity['image']

            cursor.execute("select* from offers where geo=? and price=?", (geo, price))
            if (len(cursor.fetchall()) == 0):
                cursor.execute('''
                INSERT INTO offers (price, title, url, geo, offerDate, date)
                VALUES(?,?,?,?,?,?)''',
                               (price, title, url, geo, offer_date, datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

                r = requests.get(image)
                filename = str(price)+'.jpg'
                w = open(filename, 'wb').write(r.content)

                f = open(filename, 'rb')
                asyncio.run(TelegramBot.send_message(TelegramBot.channel_id, f,
                                                     '<b>'+str(title)+'</b>'+'\n'+
                                                     'Цена: '+str(price)+' рублей'+'\n'+
                                                     'Адрес: : '+str(geo)+'\n'+
                                                     str(url)))
                # TelegramBot.bot.send_photo(TelegramBot.channel_id, f,
                #                                      '<b>'+str(title)+'</b>'+'\n'+
                #                                      'Цена: '+str(price)+' рублей'+'\n'+
                #                                      'Адрес: : '+str(geo)+'\n'+
                #                                      str(url))
                os.remove(filename)
                f.close()
                asyncio.sleep(5)



if __name__ == '__main__':
    DataBase().set_connection()
