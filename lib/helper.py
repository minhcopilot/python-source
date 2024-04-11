def find_k_largest_number(numbers,k=2):
    numbers.sort()
    return numbers[-k:]

def find_k_smallest_number(numbers,k=3):
    numbers.sort()
    return numbers[:k]

def find_NumberOfUnits(numbers):
    return [num for num in numbers if num%2 ==0 ]

def find_even_number(numbers):
    if numbers%2==0:
        return True
    else:
        return False
    
def find_char_e_r(sequence):
    if 'e' in sequence or 'r' in sequence:
        return True
    else:
        return False
def find_char_e_r_2(char):
    letters=['e','r']
    if char in letters:
        return True
    else:
        return False
    
def double_number(number):
    if number%2 ==0:
        return number*number
    else:
        return number*2

def add_two_list(nums1,nums2):
    return [n+m for n,m in zip(nums1,nums2)]