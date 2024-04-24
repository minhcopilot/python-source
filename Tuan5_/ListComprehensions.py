# lists = ['a','b','c','d']
# list_new =[]
# for char in lists:
#     char = char.upper()
#     list_new.append(char)
# print(list_new)

# #1. [f(x) for x in list]
# upper_letters = [x.upper() for x in lists]
# print(upper_letters)

# numbers = [1,2,3,4]
# binhPhuong =[num*num for num in numbers]
# print(binhPhuong)

# #2. [f(x) for x in list if condition(x)]
# binhPhuong2 = [num*num for num in numbers if num <4]
# print(binhPhuong2)

# #3. [f(x) if condition(x) else y(x) for x in list]
# binhPhuong3 = [num*num if num <4 else num*2 for num in numbers]
# print(binhPhuong3)

# #Bài tập 1: Use list comprehension to construct a new list but add 6 to each item.
# listEx1=[1,34,5,7,3,57,356]
# listOutEx1 = [num+6 for num in listEx1]
# print(listOutEx1)

# #Bài tập 2: Using list comprehension, construct a list from the squares of each element in the list, if the square is greater than 50.
# square=[num*num for num in listEx1 if num*num > 50]
# print(square)

# #Bài tập 3: Given a list fruits = ['mango', 'kiwi', 'strawberry', 'guava', 'pineapple', 'mandarin orange']
# fruits = ['mango', 'kiwi', 'strawberry', 'guava', 'pineapple', 'mandarin orange']
# #- Make a list that contains each fruit with more than 5 characters
# fruitMore5 = [fruit for fruit in fruits if len(fruit) > 5]
# print(fruitMore5)
# #- Make a variable named fruits_with_letter_a that contains a list of only the fruits that contain the letter "a"
# fruits_with_letter_a =[fruit for fruit in fruits if 'a' in fruit]
# print(fruits_with_letter_a)

#- Make a variable named fruits_with_two_a that contains a list of only the fruits that contain more than two letter "a"
# fruits_with_two_a =[fruit for fruit in fruits if fruit.count('a') > 2]
# print(fruits_with_two_a)

# color=['C', 'B', 'R','Ch']
# att =['2','3','4','5','6','7','8','9','10','J','Q','K','A']
# Cards=[a+c for c in color for a in att]
# print(Cards)

#output 
color=['C', 'B', 'R','Ch']
att=['1','2','3','4']

Cards =[a+c for c,a in zip(color,att)  ]
print(Cards)