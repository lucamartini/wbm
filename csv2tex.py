import glob
import re
import csv
import sys


L1file = "L1_rates.csv"
HLTfile = "path_rates.csv"


run = sys.argv[1]
lumi = float(sys.argv[2])
factor = 5./lumi

print "run lumi =", lumi, "factor =", factor


def getCell(path, column, file):
    with open(file, 'r') as rates:
        ratereader = csv.reader(rates)
        for row in ratereader:
            if (path in row[0]) or ("LMNR" in path and "LowMass" in row[0]):
                return row[column]
    print "did not find", path


texFiles = glob.glob("./*_DEF.tex")
for texFile in texFiles:
    print texFile
    outFileName = texFile.replace("_DEF", "")
    outFile = open(outFileName, "w")

    with open(texFile, 'r') as tabular:
        for line in tabular:
            # print line
            reg = r'^\ *\\rowcolor\{[a-zA-Z0-9]+\} ([a-zA-Z0-9\_\\]+)\ +\&'
            pathreg = re.search(reg, line)

            if pathreg:
                path = pathreg.group(1).replace('\\', '')
                if 'L1' in texFile:
                    inputFile = L1file
                else:
                    inputFile = HLTfile
                rate = getCell(path, 1, inputFile)
                if 'L1' not in texFile:
                    rate = str(float(rate) * factor)
                prescale = getCell(path, 2, inputFile)
                DEF_reg = r'(DEF)\ *\\\\$'
                rep = str("\\\\num{" + rate + "} & \\\\num{" + prescale + "} \\\\\\\\")

                line = re.sub(DEF_reg, rep, line)
                print line
            outFile.write(line)
    outFile.close()


with open("news/news_DEF.tex") as news:
    outFile = open("news/news.tex", 'w')
    reg_run = "(RUN)"
    reg_lumi = "(LUMI)"
    reg_factor = "(FACTOR)"
    for line in news:
        found = re.search(reg_run, line)
        if found:
            line = re.sub(reg_run, run, line)

        found = re.search(reg_lumi, line)
        if found:
            line = re.sub(reg_lumi, str(lumi), line)

        found = re.search(reg_factor, line)
        if found:
            line = re.sub(reg_factor, str(factor), line)
        outFile.write(line)
    outFile.close()
