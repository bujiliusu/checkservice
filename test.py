import os
u = '中文'
str00 = u.encode('gb2312')
u1 = str00.decode('gb2312')
print('u1', u1)
print(type(str00))
print(type(u))
print(type(u1))

# u2 = str00.decode('utf-8')
# print('u2',u2)
import codecs, chardet
f = codecs.open('test2.properties', 'w+', encoding='utf-8')
f.write('显示成功')
f.close()
print('..........')

f = open('test5.properties', 'rb')
data = f.read()
print(chardet.detect(data))