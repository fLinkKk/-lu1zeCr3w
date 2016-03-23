import binascii
import base64
import sys

def text_to_bits(text, encoding='utf-8', errors='neverhappen'):
    bits= " ".join(reversed( [i+j for i,j in zip( *[ ["{0:04b}".format(int(c,16))
                        for c in reversed("0"+binascii.hexlify(text))]
                        [n::2] for n in [1,0] ] ) ] ))
    return bits

def xorBytes_string(byte1, byte2):
    byte1_int = int(byte1,2)
    byte2_int = int(byte2,2)
    xored = byte1_int ^ byte2_int

    return text_to_bits(chr(xored))

###########START##############
if len(sys.argv) == 2:
    inputRaw = sys.argv[1]
else:
    print "[!!!] Usuage: stringToCrypt\naborting"
    sys.exit(1)

print "[*] Trying to crypt ... "

listPlain_bin = []
listEncr_bin = []

for p in inputRaw:
    listPlain_bin.append(text_to_bits(p))

print "[**] plaintext in bin is : "
print listPlain_bin

key = "11010001" #209
IV  = "10101110" #174

I = IV
counter = 0
c = ""
########ENCRYPTION###############
for p in listPlain_bin:
    I = xorBytes_string(key,I)
    c = xorBytes_string(p, I)
    listEncr_bin.append(c)
    counter = counter + 1
########END-ENCRYPTION############

print "[**] encrtext in bin is : "
print listEncr_bin

encrStr = ""
for c in listEncr_bin:
    encrStr = encrStr + chr(int(c,2))

encrStrBase64 = base64.encodestring(encrStr)
print "[!!!] ENCR IN BASE 64 : \n\t" + encrStrBase64
