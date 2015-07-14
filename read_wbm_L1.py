import csv
import re
import sys

ratedir = "./runs/" + sys.argv[1] + "/"
TnP = False

reg = r'<[bB]>([0-9,.]+)</[bB]>'

with open('L1_rates.csv', 'w') as csvOutFile:
    csvwriter = csv.writer(csvOutFile)
    with open('L1_list.csv') as paths:
        csvwriter.writerow(["#path", "avgRate", "Prescale"])
        for path in paths:
            path = path.strip()
            if path == "":
                TnP = True
                continue
            path_parsed = '>' + path + '<'
            print path
            with open(ratedir + "L1Summary.html") as L1_html:
                for line in L1_html:
                    if path_parsed in line:
                        searched = re.findall(reg, line)
                        searched_nocomma = []
                        for s in searched:
                            s_nocomma = re.sub(',', '', s)
                            searched_nocomma.append(s_nocomma)
                        print searched_nocomma
                        csvwriter.writerow([path, searched_nocomma[2], searched_nocomma[3]])
                        break
