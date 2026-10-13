# def filter_postive(numbers):
#     return list(filter(lambda x:x>=0,numbers))
# numbers=[1,2,-3,4,-2,8,-5,9]
# print(filter_postive(numbers))


# from functools import reduce
# def calculate_factorial(n):
#     return reduce(lambda x,y:x*y,range(1,n+1))
# n=5
# print(calculate_factorial(n))


from functools import reduce
def count_vowels(s):
    return reduce(lambda x,y: x+(y in "aeiou"),s,0)
print(count_vowels("sravaniroyal"))

        
