# from helper import find_k_largest_number,find_k_smallest_number
# from helper import *
# numbers=[1,7,9,10,2,6,4]
# print( f'K largest numbers are :{find_k_largest_number(numbers)}')
# print( f'K largest numbers are :{find_k_smallest_number(numbers)}')

# import helper 
# numbers=[1,7,9,10,2,6,4]
# print( f'K largest numbers are :{helper.find_k_largest_number(numbers)}')
# print( f'K largest numbers are :{helper.find_k_smallest_number(numbers)}')

# import lib.helper as h
# numbers=[1,7,9,10,2,6,4]
# print( f'K largest numbers are :{h.find_k_largest_number(numbers)}')
# print( f'K largest numbers are :{h.find_k_smallest_number(numbers)}')

# Cách hay sử dụng
# from lib.helper import find_k_largest_number,find_k_smallest_number,find_NumberOfUnits,find_even_number
# numbers=[1,7,9,10,2,6,4]
# print( f'K largest numbers are :{find_k_largest_number(numbers)}')
# print( f'K largest numbers are :{find_k_smallest_number(numbers)}')
# print( f'Number of Units :{find_NumberOfUnits(numbers)}')
# output=list(filter(find_even_number,numbers))
# print(output)

# from lib.helper import find_char_e_r
# sequence =['g','e','e','j','k','s','p','r']
# filtered = list(filter(find_char_e_r,sequence))
# print(filtered)

# from lib.helper import double_number
# numbers =[1,2,3,4]
# output =list(map(double_number,numbers))
# print(output)
# # using lambda function
# output1=list(map(lambda x:x*2,numbers))
# print(output1)
# output2=list(filter(lambda x:(x%2==0),numbers))
# print(output2)

# exercise 4
# from lib.helper import double_number
# numbers =[1,2,3,4]
# output =list(map(double_number,numbers))
# print(output)
# # using lambda function
# output1=list(map(lambda x:x*x if(x%2==0) else x*2,numbers))
# print(output1)

# #exercise 5
# nums1=[1,2,3]
# nums2=[4,5,6]
# output=list(map(lambda n,m:(n+m) ,nums1,nums2))
# print(output)

# #exercise 2
my_list =["geeks","geeg","keegs","pratice","aa"]
list_char=['e','g','s','k']
# output1 = list(filter(lambda  x:'e' in x and 'g' in x and 'k' in x and 's' in x,my_list))
output1 = list(filter(lambda  x:all([char in x for char in list_char]),my_list))
print(output1)

# exercise 1
my_list =["geeks","geeg","keek","pratice","aa"]
output =list(filter(lambda x :x ==x[::-1],my_list))
print(output)
