import csv
import browserhistory as bh


class searchData:
    def __init__(self):
        self.history_dict = dict()

    def getHistory(self) -> None:
        print('====================\nRetrieving browser data...')
        self.history_dict = bh.get_browserhistory()

    def writeToCSV(self) -> None:
        self.getHistory()
        print("\n...\nwriting to csv file...")
        for browser, history in self.history_dict.items():
            with open('./searchHistory/history.csv', mode='w', encoding='utf-8', newline='') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
                for data in history:
                    csv_writer.writerow(data)
        print("\n...\njob finished successfully!")


if __name__ == '__main__':
    sd = searchData()
    sd.writeToCSV()
