from datetime import datetime, date
import requests
from realty.control.data_service import DataService
from realty.db.db import DataBase


class YandexParser():
    def get_json(self):
        params = (
            ('sort', 'DATE_DESC'),
            ('rgid', '319712'),
            ('type', 'SELL'),
            ('category', 'APARTMENT'),
            ('_pageType', 'search'),
            ('_providers',
             ['seo', 'queryId', 'forms', 'filters', 'filtersParams', 'direct', 'mapsPromo', 'newbuildingPromo',
              'refinements', 'search', 'react-search-data', 'searchHistoryParams', 'searchParams', 'searchPresets',
              'serpDirectPicType', 'showSurveyBanner', 'seo-data-offers-count', 'related-newbuildings', 'breadcrumbs',
              'ads', 'categoryTotalOffers', 'footer-links', 'site-special-projects']),
            ('crc', 'ub4b3629c2dbff5260206290ba1c4fdcf'),
        )
        response = requests.get('https://realty.yandex.ru/gate/react-page/get/', params=params)
        return response.json()

    def get_offers(self, data):
        offers = []
        entities = data['response']['search']['offers']['entities']
        for item in entities:
            offer = {}
            offer['price'] = item['price']['value']
            rooms = item['roomsTotalKey']
            floors_total = item['floorsTotal']
            floors_offered = item['floorsOffered'][0]
            area = item['area']['value']
            if(rooms == 'studio'):
                title = 'Студия, ' + str(area) + ' м², ' + str(floors_offered) + '/' + str(
                    floors_total) + ' эт.'
            else:
                title = str(rooms) + '-к. квартира, '+ str(area) +' м², '+ str(floors_offered)+'/'+str(floors_total)+' эт.'
            offer['title'] = title
            offer['url'] = item['shareUrl']
            offer['geo'] = item['location']['geocoderAddress']

            if item.get('updateDate'):
                offer_date = datetime.strptime(item['updateDate'], '%Y-%m-%dT%H:%M:%SZ')
                offer_date = datetime.strftime(offer_date, '%d.%m.%Y в %H:%M')
            else:
                offer_date = datetime.strptime(item['creationDate'], '%Y-%m-%dT%H:%M:%SZ')
                offer_date = datetime.strftime(offer_date, '%d.%m.%Y в %H:%M')

            offer['offer_date'] = offer_date
            offer['image'] = ' http:'+str(item['mainImages'][0])
            today = date.today()
            d1 = today.strftime("%d.%m.%Y")
            if offer['offer_date'].split(" ")[0] == d1:
                offers.append(offer)

        return offers

    def main(self):
        data = self.get_json()

        offers = self.get_offers(data)
        print('Yandex: '+str(len(offers)))
        DataBase().add_offers_to_db(offers)





if __name__ == '__main__':
    YandexParser().main()
