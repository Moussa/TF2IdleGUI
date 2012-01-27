from Encrypt import AESObject

ini = open('tf2idle.ini', 'rb').read()

object = AESObject('mykey')

f = open('test.txt', 'wb')
f.write(object.encrypt(ini))
f.close()