# -*- coding: utf-8 -*-
# GETS A HASH FROM A WEBSIDE, EXTRACTS IT
# TRIES TO CRACK THE HASH USING hashcat

import urllib2
import os
import time

def getMsg(raw):

    print "[getMsg: ] Now parsing html ..."
    startPattern = ""
    endPattern = ""

    startIndex = raw.find(startPattern) + len(startPattern) + 4
    raw = raw[startIndex:]
    endIndex = raw.find(endPattern)
    raw = raw[:endIndex]

    return raw

cookie = "cookie"
getUrl = ""
hashcatCommand = "hashcat -a 3 -m 100 hash.txt ?d?d?d?d -o out.txt --outfile-format=2"

print "[*] Establishing Connection"

opener = urllib2.build_opener()
opener.addheaders.append(("Cookie", cookie))

f = opener.open(getUrl)
ts1 = time.time()

msg = getMsg(f.read())

print "[*] Successfully received and parsed!"

fi = open("hash.txt", "w")
print "[**] Hash: " + msg
fi.write(msg)
fi.close()

fi = open("out.txt", "rw")

print "[**] Wrote hash to hash.txt"
print "[*] Starting shellcall"

os.system(hashcatCommand)

cracked = fi.read()[1:]
fi.close()

print "[**] Cracked: " + cracked
