# (""""""This is a multi-line string.
# It can span multiple lines.)

print(
    """hi
my name is Abdullah
I am the GOAT"""
)

print(
    """no
one
can
stop
me"""
)

# Indexing And Slicing

# Indexing is the process of accessing individual characters in a string using their position (index). In Python, string indexing starts at 0, meaning the first character of the string is at index 0, the second character is at index 1, and so on. Negative indexing allows you to access characters from the end of the string, where -1 refers to the last character, -2 refers to the second-to-last character, and so on.

# Slicing is the process of extracting a portion of a string by specifying a range of indices. The syntax for slicing is string[start:stop:step], where start is the index to begin slicing (inclusive), stop is the index to end slicing (exclusive), and step is the interval between characters to include in the slice (optional). If start is omitted, it defaults to 0. If stop is omitted, it defaults to the length of the string. If step is omitted, it defaults to 1.

# Example of indexing and slicing in Python:

mystring = "I Love Python"

print(mystring[0])  # print the first character of the string

print(mystring[2])  # print the third character of the string

print(mystring[-1])  # print the last character of the string

print(mystring[2:6])  # print characters from index 2 to 5

print(mystring[:6])  # print the first 6 characters of the string

print(mystring[7:])  # print characters from index 7 to the end of the string

print(mystring[::1])  # print the string with a step of 1 (default)

print(mystring[::2])  # print the string with a step of 2 (every other character)

print(mystring[::-1])  # print the string in reverse order

print(mystring[1:10:2])  # print characters from index 1 to 9 with a step of 2

print(mystring[-10:-1])  # print characters from index -10 to -2
