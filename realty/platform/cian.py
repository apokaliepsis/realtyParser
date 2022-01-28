from datetime import datetime, date

import requests
from realty.control.data_service import DataService
from realty.db.db import DataBase


class CianParser():
    def get_json(self):
        headers = {
            'authority': 'api.cian.ru',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
            'sec-ch-ua-platform': '"Linux"',
            'content-type': 'text/plain;charset=UTF-8',
            'accept': '*/*',
            'origin': 'https://barnaul.cian.ru',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://barnaul.cian.ru/',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': '_CIAN_GK=833cbe30-d55f-40f0-95dd-57a04c84ac61; adb=1; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; _gcl_au=1.1.1646568276.1641637673; uxfb_usertype=searcher; _ga=GA1.2.1555264283.1641637673; uxs_uid=a3477c40-706d-11ec-a0c8-69f2cc95f660; tmr_lvid=8bd603bfa34876463dc24a219b079227; tmr_lvidTS=1641637673484; afUserId=32fbfd41-d258-4962-af25-0037ee87c8dd-p; AF_SYNC=1641637674506; first_visit_time=1641637684097; pview=1; serp_registration_trigger_popup=1; sopr_session=3f45bac87414474e; _gid=GA1.2.148143561.1641781346; is_push_declined=true; __cf_bm=0mt6lxtT2AN5ilF6veTM7kmWDCJWDcS1eocd3aLpb9o-1641785088-0-ASRu1mou41hxmKOp2dhyu2qj3yfurvsnYf3iVm7cAfLbOUvqSIp7fHghkLJ22Sux2rYSgEYCLc5DPhMYsTAzCik=; session_region_id=4668; session_region_name=%D0%91%D0%B0%D1%80%D0%BD%D0%B0%D1%83%D0%BB; forever_region_id=4668; forever_region_name=%D0%91%D0%B0%D1%80%D0%BD%D0%B0%D1%83%D0%BB; session_main_town_region_id=4668; cto_bundle=o4EUiF92b1ZKSnNUZU5ZTFQzZ2F6end6aWh5eDQyU1A1YThJU011dE1hVTdHNjNLaXlvaWFXY2Z2JTJGcFQlMkJaJTJCM0p6c0c5ZUtMRWpJOFA4JTJGVElKSEFUZCUyRkw5alc5UlZMVEdqd3NqOEJ3UlQ1c2RwRmloN1ZNUklkZU9abE5SWEJJdXhWaW5jTTJnOHFrVjV3Q3pjb1pJWVdvUnZRJTNEJTNE; tmr_reqNum=162; _dc_gtm_UA-30374201-1=1',
        }

        data = '{"jsonQuery":{"region":{"type":"terms","value":[4668]},"_type":"flatsale","engine_version":{"type":"term","value":2},"room":{"type":"terms","value":[1,2]},"sort":{"type":"term","value":"creation_date_desc"}}}'

        response = requests.post('https://api.cian.ru/search-offers/v2/search-offers-desktop/', headers=headers,
                                 data=data)
        return response.json()

    def get_offers(self, data):
        offers = []
        for item in data['data']['offersSerialized']:
            offer = {}
            offer['price'] = item['bargainTerms']['priceRur']
            rooms = item['roomsCount']
            area = item['totalArea']
            floors_count = item['building']['floorsCount']
            floor = item['floorNumber']
            title = str(rooms) + '-к. квартира, '+ str(area) +' м², '+ str(floor)+'/'+str(floors_count)+' эт.'

            offer['title'] = title
            offer['url'] = item['fullUrl']
            offer['geo'] = item['geo']['userInput']
            timestamp = datetime.fromtimestamp(item['addedTimestamp'])
            timestamp = datetime.strftime(timestamp, '%d.%m.%Y в %H:%M')
            offer['offer_date'] = timestamp
            print(title)
            if len(item['photos'])>0:
                offer['image'] = item['photos'][0]['thumbnail2Url']

            today = date.today()
            d1 = today.strftime("%d.%m.%Y")
            if offer['offer_date'].split(" ")[0] == d1:
                offers.append(offer)
                print(offer)

        return offers

    def main(self):
        data = self.get_json()
        offers = self.get_offers(data)
        print('Cian: '+str(len(offers)))
        DataBase().add_offers_to_db(offers)
        # for item in offers:
        #     print(item)


if __name__ == '__main__':
    CianParser().main()
