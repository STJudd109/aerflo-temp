#python3

import csv
import argparse
import codecs


# devlog = csv.reader(open('devlog_4_2018_07_05_142040.csv', newline=''), delimiter=',', quotechar='|')
# spamReader = csv.reader(open('devlog_4_2018_07_05_142040.csv', newline=''), delimiter=',', quotechar='|')
#import two files

#fitmate tsv

#devlog csv

class TestParticipant():
    def __init__(self, testdata):
        self.testdata = testdata[0]
        self.testdata_H = testdata[1]
        self.name = ''
        self.age = 0
        self.height = 0
        self.weight = 0
        self.hr = 0
        print(self.testdata)
    
    def make_file_name(self):
        name = "aerflo - {}-{}.csv".format(self.name,self.age)
        return name
    
    def sort_headers(self):
        return None

    def sort_data(self):
        return None



class TestRes():
    def __init__(self, devlog, fitmate):
        self.devlog_file = devlog
        self.fitmate_file = fitmate
        self.devlog_arr = []
        self.fitemate_arr = []
        self.testdata = TestParticipant(self.extract_test_info())
        self.offset = 0

        self.build_arrs()


    def build_file(self):
        headers = ["Time","Rf" "b/min","VE l/min","VO2 ml/min","VO2/Kg ml/Kg/min","FeO2 %","Phase","HR bpm","PA mmHg","Load watt","Speed kmh","Grade %","SBP mmHg","DBP mmHg","EVC l","RPE","O2gain","KMix"]
        outfile = csv.writer(open('test_out.csv', 'w', newline=''), dialect='excel')
        outfile.writerow(headers)

        return None

    def extract_test_info(self):
        testdata = ''
        testdata_H = ''
        for row in self.devlog_file:
            testdata = row[len(row)-1]
            testdata_H = row[len(row)-2]
            break
        print('Testdata extracted from headers')
        outdata = [testdata, testdata_H]

        return outdata
    
    def build_arrs(self):
        cnt = 0
        for row in self.devlog_file:
            if cnt == 0:
                cnt = cnt + 1
            else:
                self.devlog_arr.append(row)
        
        for row in self.fitmate_file:
            if cnt != 4:
                cnt = cnt + 1
            else:
                self.fitemate_arr.append(row)
        
        print('Arrays built from logs')

    def find_offset_row(self):
        cnt = 0
        for row in devlog_arr:
            cnt = cnt +1
            if row[0] === self.offset
                return cnt

        


def main(args):

    csvdevlog = open(args.devlog, encoding='utf-8', errors='ignore')
    # dev_dialect = csv.Sniffer().sniff(csvdevlog.read(1024))
    # csvdevlog.seek(0)
    devlog = csv.reader(csvdevlog, dialect='excel')

    csvfitmate = open(args.fitmate, encoding='utf-8', errors='ignore')
    # fit_dialect = csv.Sniffer().sniff(csvfitmate.read(1024))
    # csvdevlog.seek(0)
    fitmate = csv.reader(csvfitmate)

    test = TestRes(devlog, fitmate)
    print('built test object')

    test.build_file()






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpret test data')
    parser.add_argument('--d', type=str, default='devlog_4_2018_07_05_142040.csv', dest='devlog', help='the equation in plain text')
    parser.add_argument('--t', type=str, default='Fitmate 2018-07-05 Rhett Pratt.csv', dest='fitmate', help='the equation in plain text')

    args = parser.parse_args()

    main(args)