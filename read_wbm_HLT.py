import csv
import re
import sys


def round(num):
    if (num > 0):
        return int(num+.5)
    else:
        return int(num-.5)

ratedir = "./runs/" + sys.argv[1] + "/"
TnP = False

reg = r'>([0-9.]+)</a><'
pre_reg = r'RIGHT"?>([0-9.]+)</[tT][dD]'

with open('path_rates.csv', 'w') as csvOutFile:
    csvwriter = csv.writer(csvOutFile)
    with open('path_list.csv') as paths:
        csvwriter.writerow(["#path", "avgRate", "Prescale"])
        for path in paths:
            path = path.strip()
            if path == "":
                TnP = True
                continue
            print path
            with open(ratedir + "HLTSummary.html") as HLT_html:
                for line in HLT_html:
                    if path in line:
                        # print line
                        searched = re.findall(reg, line)
                        print searched
                        search_pre = re.findall(pre_reg, line)
                        print search_pre
                        pre = round(float(search_pre[0]) / float(search_pre[1]))
                        csvwriter.writerow([path, searched[0], pre])
                        break
