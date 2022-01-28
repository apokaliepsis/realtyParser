import json
import requests
from selectolax.parser import HTMLParser
from urllib.parse import unquote
from datetime import datetime, date
from realty.control.data_service import DataService
from realty.db.db import DataBase

SITE = 'https://www.avito.ru/'


class AvitoParser():
    def get_offers(self, data):
        offers = []
        for key in data:
            if 'bx-single-page' in key:
                items = data[key]['data']['catalog']['items']
                for item in items:
                    if item.get('id'):
                        offer = {}
                        offer['price'] = item['priceDetailed']['value']
                        offer['title'] = item['title']
                        offer['url'] = SITE + item['urlPath']
                        timestamp = datetime.fromtimestamp(item['sortTimeStamp'] / 1000)
                        timestamp = datetime.strftime(timestamp, '%d.%m.%Y в %H:%M')
                        offer['offer_date'] = timestamp
                        city = item['location']['name']
                        address = item['geo']['formattedAddress']
                        offer['geo'] = city + ', ' + address
                        offer['image'] = item['gallery']['imageLargeUrl']
                        today = date.today()
                        d1 = today.strftime("%d.%m.%Y")
                        if offer['offer_date'].split(" ")[0] == d1:
                            offers.append(offer)
        return offers

    def get_json(self, url):
        data = {}
        response = requests.get(url)
        html = response.text

        tree = HTMLParser(html)
        scripts = tree.css('script')
        for script in scripts:
            if 'window.__initialData__' in script.text():
                jsontext = script.text().split(';')[0].split('=')[-1].strip()
                jsontext = unquote(jsontext).replace(u'\xa0', u' ')
                jsontext = jsontext[1:-1]
                data = json.loads(jsontext)
                self.get_offers(data)
                #with open('avito.json', 'w', encoding='utf-8') as file: json.dump(data, file, ensure_ascii=False)
        return data

    def main(self):
        url = "https://www.avito.ru/barnaul/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1"
        data = self.get_json(url)
        offers = self.get_offers(data)
        print('Avito: '+str(len(offers)))
        DataBase().add_offers_to_db(offers)

        for entity in offers:
            print(entity)

    def get_length(self):
        return len(DataService.__data_services)
if __name__ == '__main__':
    AvitoParser().main()

