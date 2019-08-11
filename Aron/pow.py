from hashlib import sha1, sha256, sha512, sha224, md5, sha384

hexs = 6
cusu = 0
to_find = '544869'

while True:
    res = md5(str(cusu)).hexdigest()[-hexs:]
    if res == to_find:
        print(cusu)
        break
    cusu +=1
