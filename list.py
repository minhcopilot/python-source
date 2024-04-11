# numbers =[10,20,30,40,50,60]
# for num in numbers:
#     if (num/10) % 2 != 0:
#         num=num*2
#print(num)

# numbers =[10,21,30,41,50,61]
# for idx in range(len(numbers)):
#     if (numbers[idx]% 20) != 0:
#         numbers[idx]=numbers[idx]*2
# print(numbers)
    
# list_a =[10, 20, 30, 20, 20, 10, 50, 60, 40, 80, 50, 40]
# list_b= []

# for num in list_a:
#     if(num not in list_b):
#         list_b.append(num)
# print(list_b)

# list =['a', 'b']
# list_new = []
# n =5
# i=1
# while i <= n :
#     list_new.append(list[0]+str(i))
#     list_new.append(list[1]+str(i))
#     i=i+1
# print(list_new)

list_a =[[1,2],3,[4,5],7,8]
for idx,item in enumerate(list_a):
    if type(item) ==list:
        for sub_idx, sub_item in enumerate(item):
            if isinstance(sub_item, int) and sub_item % 2 != 0:
                list_a[idx][sub_idx] *= 2
    else:
        if item%2 !=0:
            list_a[idx] = list_a[idx]*2
print(list_a)