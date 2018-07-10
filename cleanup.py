#python3

import csv
import argparse
import codecs

class TestParticipant():
    def __init__(self, testdata):
        self.testdata = testdata[0]
        self.testdata_H = testdata[1]
        self.name = ''
        self.age = 0
        self.height = 0
        self.weight = 0
        self.hr = 0
        self.sex = ''
        self.id = 0
        print(self.testdata)

        self.sort_data()
    
    def make_file_name(self):
        name = "aerflo - {}-{}.csv".format(self.name,self.id)
        return name

    def sort_data(self):
        data = self.testdata.split('-')
        self.name = "{}{}".format(data[1],data[2])
        self.id = "{}".format(data[3])
        self.age = "{}".format(data[4])



class TestRes():
    def __init__(self, devlog, fitmate, offset, converted=False):
        self.devlog_file = devlog
        self.fitmate_file = fitmate
        self.devlog_arr = []
        self.fitemate_arr = []
        self.testdata = TestParticipant(self.extract_test_info())
        self.offset = offset
        self.final_data_arr = []

        self.build_arrs(converted)

        self.offset_adj = self.find_offset_adj()
        self.expected_len = len(self.devlog_arr[0])
        print(self.expected_len)


    def build_file(self):
        filename = self.testdata.make_file_name()
        headers = ["MILLIS","X","Y","Z","MIC","PRESSURE","RR","CADENCE","O2","BPM","PI","PVI","Time","Rf" "b/min","VE l/min","VO2 ml/min","VO2/Kg ml/Kg/min","FeO2 %","Phase","HR bpm","PA mmHg","Load watt","Speed kmh","Grade %","SBP mmHg","DBP mmHg","EVC l","RPE","O2gain","KMix","fitmate"]
        outfile = csv.writer(open(filename, 'w', newline=''), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        outfile.writerow(headers)
        print('Estimated time: {} min'.format(len(self.devlog_arr)/60000))
        self.prep_new_data()

        print('attempting to write {} lines'.format(len(self.devlog_arr)))
        for row in self.devlog_arr:
            outfile.writerow(row)
        

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
    
    def build_arrs(self,converted=False):
        cnt = 0
        #issue with conversion
        if converted:
            cnt_stop = 4
        else:
            cnt_stop = 3

        for row in self.devlog_file:
            if cnt == 0:
                cnt = cnt + 1
            else:
                self.devlog_arr.append(row)
        
        for row in self.fitmate_file:
            if cnt != cnt_stop:
                cnt = cnt + 1
            else:
                self.fitemate_arr.append(row)
        
        print('Arrays built from logs')
    
    def find_offset_adj(self):
        return self.offset
        # return self.offset - time_to_milli(self.fitemate_arr[0][0])
    
    def prep_new_data(self):
        count = 0
        new_data = []
        ext = ["true"]
        uniq = False
        last_append = self.fitemate_arr[0]
        # first_row = self.fitemate_arr[0]
        print(last_append)
        for dev_row in self.devlog_arr:
            milli_time = int(dev_row[0])
            for fit_row in self.fitemate_arr:
                found = 0
                fit_milli_time = time_to_milli(fit_row[0]) + self.offset_adj
                if fit_milli_time >= self.offset and milli_time-20 <= fit_milli_time and fit_milli_time <= milli_time+20:
                    count = count+1
                    print('Total found: {} -- milli_time: {} - fit_milli_time: {} '.format(count, milli_time, fit_milli_time))
                    # dev_row.extend(fit_row)
                    uniq = True
                    if fit_row == last_append:
                        uniq = False
                        count = count-1
                    last_append = fit_row
                    break

            dev_row.extend(last_append)
            if uniq:
                dev_row.extend(ext)
            else:
                dev_row.extend(["false"])
            uniq = False
                    
            # if len(dev_row) < self.expected_len:
            #     if last_append == '':
            #         dev_row.extend(first_row)
            #     else:
            #         dev_row.extend(last_append)
        
        print('compiled data, now attepting to build....')
                
                    

#Helper utils
def time_to_milli(time):
    time = str(time)
    out = sum(int(x) * 60 ** i for i,x in enumerate(reversed(time.split(":"))))
    return out * 1000


#start of main program
def main(args):

    csvdevlog = open(args.devlog, encoding='utf-8', errors='ignore')
    devlog = csv.reader(csvdevlog, dialect='excel')

    try:
        csvfitmate = open(args.fitmate, encoding='utf-8')
        fitmate = csv.reader(csvfitmate, dialect='excel-tab')
        converted = False
        for row in fitmate:
            if len(row) < 2:
                fitmate = None
                csvfitmate.close()
                #de ref vars
                raise ValueError('error in file encoding')
            else:
                break
    except Exception as e:
        print(e)
        print('Trying to convert file to utf-8')
        try:
            source_file = open(args.fitmate, 'rb')
            contents = source_file.read()
            with open(args.fitmate, 'w+b') as dest_file:
                dest_file.write(contents.decode('utf-16').encode('utf-8'))

            csvfitmate = open(args.fitmate, encoding='utf-8')
            fitmate = csv.reader(csvfitmate, dialect='excel-tab')
            converted = True
        except Exception as er:
            print(er)
            print('still didnt work, try manual conversion')
            exit

    test = TestRes(devlog, fitmate, args.offset, converted)
    print('built test object')
    print('Starting file build...may take some time...')
    test.build_file()
    print('File Built!')




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpret test data')
    parser.add_argument('--d', type=str, default='devlog.csv', dest='devlog', help='devlog.csv file name or path')
    parser.add_argument('--t', type=str, default='Fitmate.TXT', dest='fitmate', help='fitmate.txt filename or path')
    parser.add_argument('--s', type=int, default=108128, dest='offset', help='starting timestamp of test from devlog')
    args = parser.parse_args()

    main(args)