a = "Hi my name is Abdullah"
len(a)  # this will return the length of the string a
print(len(a))

a = "            Hi my name is Abdullah              "

print(
    a.strip()
)  # this will remove the leading and trailing whitespace from the string a
print(a.lstrip())  # this will remove the leading whitespace from the string a
print(a.rstrip())  # this will remove the trailing whitespace from the string a

a = "###$#$#$#Hi my name is Abdullah###$#$#$######"
print(
    a.strip("#$")
)  # this will remove the leading and trailing # and $ from the string a
print(a.lstrip("#$"))  # this will remove the leading # and $ from the string a
print(a.rstrip("#$"))  # this will remove the trailing # and $ from the string

b = "i am the goat 4ever"
print(
    b.title()
)  # this will convert the first character of each word to uppercase and the rest to lowercase

print(
    b.capitalize()
)  # this will convert the first character of the string to uppercase and the rest to lowercase
