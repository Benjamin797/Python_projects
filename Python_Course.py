#static method & class method can be used without create an object


#The map function can be used to apply a function to every element in a given list :

def f1(x):
    return x + x/2

nums = [1,5,6,7,2]

newList = list(map(f1, nums))

#This will create a new list where each element at index i is f1(nums[i])


#The filter function is similar to the map function. They both make use of a function and and a list.
# The filter function will pass every element of the given list into a function that returns a Boolean value.
# If the function returns True for a given element that element will be added to the new returned list.
# Otherwise it will not.

def isAOne(x):
    return x == 1

nums = [1,1,6,7,8,0,1,1]

newList = list(filter(isAOne,nums))

# newList is [1,1,1,1]

myList = [1,4,6,7,8,11,3,4,6]

#Avec un lambda
newList = list(filter(lambda x:  x > 5, myList))
# newList is [6,7,8,11,6]

newList2 = list(map(lambda x: x+1, myList))
# newList 2 is [2,5,7,8,9,12,4,5,7]

#collections
import collections
from collections import Counter

c = Counter("hello")
# This will print Counter({'h':1, 'e':1, 'l':2, 'o':1})
#Counter renvoie un dico
c = Counter([1,1,1,3,4,5,6,7, 7])

c.most_common(1)  # returns [(1, 3)] | la 1 est présent 3 fois
c.most_common(2)  # returns [(1, 3), (7, 2)] | la 1 est présent 3 fois et le 7, 2 fois

d = [1,1,3, 4, 4]

c.subtract(d)

print(c)  # prints Counter({1:1, 3:0, 4:-1, 5:1, 6:1, 7:2})

d = [1,1,3]

c.update(d)

print(c)  # prints Counter({1:5, 3:2, 4:1, 5:1, 6:1, 7:2})
c.clear()
print(c)  # prints Counter()

from collections import namedtuple

Point = namedtuple("name", "paramater1, parameter2, parameterx")

p = Point(1,4,5)

print(p)  # prints name(parameter1=1 ,parameter2=4 , parameterx=5)

"""
Point = namedtuple("Point", "x y")

p = Point(1,4)

print(p.x)  # prints 1
print(p.y)  # prints 4
print(p)  # prints Point(x=1, y=4)
"""

from collections import deque

d = deque("hello")  # Takes and iterable argument
print(d)  # prints deque(["h", "e", "l", "l","o"])

d.appendleft(5)  # d is now deque([5, "h", "e", "l","l", "o"])
d.append(4)  # d is now deque([5, "h", "e", "l","l", "o", 4])

d.pop()  # would return 4
d.popleft()  # would return 5

d.extend("12")
d.extend([7,8])
d.extendleft(100)

print(d) # prints deque([100,"h", "e", "l", "l", "o","1", "2", 7, 8])

d.rotate(1)

print(d) # prints deque(["o", "h", "e", "l", "l"])

d.rotate(-2)

print(d)  # prints deque(["e", "l", "l", "o", "h"])
