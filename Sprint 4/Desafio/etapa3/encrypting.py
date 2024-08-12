import hashlib as hs

while True:
    try:
        string = input()
        if string != "":
            print(hs.sha1(string=string.encode("utf-8")).hexdigest())
    except Exception as e:
        print(e)




