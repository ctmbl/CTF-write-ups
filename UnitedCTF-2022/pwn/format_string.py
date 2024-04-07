

def separate(s):
    a = ""
    for i in range(0,len(s)-1,2):
        a += s[i] + s[i+1] + " "
    return a

def inverse(list_of_little_endian): # Caution!!! this only works in 32bits
    a = ""
    for i in list_of_little_endian:
        if len(i) not in [2, 4, 6, 8]:
            print("Error i is size: ", len(i))
        if len(i) == 8:
            a += i[6:8] + i[4:6] + i[2:4] + i[0:2]
        if len(i) == 6:
            a += i[4:6] + i[2:4] + i[0:2] + "00"
    return a
