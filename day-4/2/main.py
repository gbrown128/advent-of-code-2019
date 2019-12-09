# Retry this on day 9!

# This is a really inefficient approach, but computing is cheap!

from collections import Counter

start = 256310
stop = 732736

def number_valid(number):
    num = list(str(number))
    last = 0
    for digit in num:
        digit = int(digit)
        if digit < last:
            return False
        last = digit
    count = Counter(num)
    if 2 in count.values():
        return True
    return False

valid = 0

for idx in range(start, stop+1):
    if number_valid(idx):
        valid += 1
        print(idx)

print("Result: {}".format(valid))
