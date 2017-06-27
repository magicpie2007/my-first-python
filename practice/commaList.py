# Insert comma to list

def insertCommaTo(list):
    list_count = len(list)
    list_str = ''
    for i in range(list_count - 1):
        list_str = list_str + str(list[i]) + ', '

    list_str = list_str + 'and ' + str(list[len(list) - 1])

    return list_str


print(insertCommaTo([1,2,3,4]))
print(insertCommaTo([1.0, 2.0, 3.0, 4.0, 5.0]))
print(insertCommaTo(["apple", "banana", "peach", "orange"]))
print(insertCommaTo([[1,2,3,4], [5, 6, 7, 8]]))

