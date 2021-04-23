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

f = open('test3', 'rb')
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

with open('test3', 'r') as f:
    s = f.read()
    # print(chardet.detect(s))
    print(s)
    # s.encode('ascii').decode('unicode_escape')
    # print(s == "你")
    # print(s.decode('utf-8'))
name = "\u4F60"
name.encode().decode('unicode_escape')
print(name)

with open('test8.properties', 'r', encoding='ascii') as f:
    s = f.read()
    a= s.encode().decode('unicode_escape')
    with open('test8.properties.bak', 'w', encoding='utf-8') as f:
        f.write(a)