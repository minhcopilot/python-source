data =  open("text2.txt", "r")
list_strFile = data.readlines()
for element in list_strFile:
    list_strData = element.split(' ')
    for item_str in list_strData:
     if '@' in item_str:
        print( f'fount an email {item_str}')