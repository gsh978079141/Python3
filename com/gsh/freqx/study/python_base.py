a = [1, 2]
c, d = a
print(c)
print(d)
array = 1, 2
print(type(array))
# e,f 交换
e, f = 1, 2
e, f = f, e
print(e, f)

list_a = [1, 2, 3, 5, 5]
list_new_a = list(set(list_a))

print(list_new_a)

print("for : ")
persons = ["张三", "李四", "王五"]

for person in enumerate(persons):
    # tuple(0,"张三")...
    print(person)

for index, person in enumerate(persons):
    # index = 0, person = 张三 ...
    print(person)

# item = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
item = [item for item in range(10)]