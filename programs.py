
class Schedule:
    def __init__(self, programs_data):
        self.programs_data = programs_data
        self.programs_data = programs_data.to_dict('records')
        # self.time = str(self.programs_data['time'])
        # self.name = self.programs_data['name']
        # self.info = self.programs_data['info']

    def search_info(self, what: str):
        for info in self.programs_data:
            for key, text in info.items():
                if key == 'category':
                    if what in text:
                        yield info['time'], info['name'], info['info']

    def print_data(self):
        for info in self.programs_data:
            yield info['time'], info['name'], info['info']


# programs_10_day = Schedule(pandas.read_excel('programs.xlsx', sheet_name='10'))
# programs_11_day = Schedule(pandas.read_excel('programs.xlsx', sheet_name='11'))

# for data in programs_11_day.search_info('дети'):
#     t = datetime.strptime(str(data[0]), "%H:%M:%S")
#     time = t.strftime('%H:%M')
#     name = data[1]
#     info = data[2]
#     print(time, name,info)