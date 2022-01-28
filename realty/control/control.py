from realty.platform.avito import AvitoParser
from realty.platform.cian import CianParser
from realty.control.data_service import DataService
from realty.platform.yandex import YandexParser


class Control:

    def run_services(self):
        #AvitoParser().main()
        CianParser().main()
        #YandexParser().main()
        return DataService().get_data_services()

    # def add_offers_to_database(self, offers):
    # for entity in offers:
    # if





if __name__ == '__main__':
    Control().run_services()
    # Control().add_offers_to_db({'price': 8888888, 'title': 'Студия, 25 м², 7/10 эт.',
    #                                  'url': 'https://realty.yandex.ru/offer/7203310982811562241',
    #                                  'geo': 'Россия, Алтайский край, Барнаул, Песчаная улица, 190',
    #                                  'offer_date': '13.01.2022 в 03:01'})
    #from realty.avito import AvitoParser
    # print(AvitoParser().get_length())
    # for entity in DataService().get_data_services():
    #     print(entity)
    # print(len(Control.data_services))