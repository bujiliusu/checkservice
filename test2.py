import codecs
import os

outputpath='./'
fhanzi1 = codecs.open(os.path.join(outputpath, "test8.properties"), "r")
fhanzi = codecs.open(os.path.join(outputpath, "hanzi.txt"), "w")

result_f = codecs.EncodedFile(fhanzi1,'ascii', 'utf-8')

for chars in result_f:
    fhanzi.write(chars)

fhanzi1.close()
fhanzi.close()

os.remove(os.path.join(outputpath, "hanzi1.txt"))