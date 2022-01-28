class DataService():
    __data_services = []

    def get_data_services(self):
        return self.__data_services

    def set_data_services(self, entity):
        self.__data_services.append(entity)

    def contains_to_store(self, element):
        for entity in self.__data_services:
            for value in entity.values():
                if str(value).__contains__(str(element)) or str(element).__contains__(str(value)) and len(
                        str(element)) > 11:
                    return True
                else:
                    return False

    def add_data_to_store(self, offers):
        for entity in offers:
            index = 1
            for value in entity.values():
                if not self.contains_to_store(value) and index == len(entity):
                    self.set_data_services(entity)

                elif self.contains_to_store(value):
                    break
                index += 1
        print('_data_services=' + str(len(DataService().get_data_services())))