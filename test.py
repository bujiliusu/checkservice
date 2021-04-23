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

f = open('test6.properties', 'rb')
data = f.read()
print(chardet.detect(data))
f.close()
print('...........')
# f = codecs.open('test2.properties', 'r+')
# s = f.read()
# u = s.encode().decode('utf-8')
# print('u:',u)
# f.close()
# print('........')

with open('test5.properties', 'rb') as f:
    s = f.read()
    # print(chardet.detect(s))
    print(type(s))
    print(s)
    print(s.decode('utf-8'))
    print(s.decode('ascii'))
    print(s.decode('ISO-8859-1'))
    # s.encode('ascii').decode('unicode_escape')
    # print(s == "你")
    # print(s.decode('utf-8'))
name = "\u4F60"
name.encode().decode('unicode_escape')
print(name)