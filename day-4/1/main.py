# Input Range 256310 - 732736
# Has two similar adjacent digits.
# Digits are always ascending or staying the same.

# Bound input range manually to 256666 - 699999

# To construct a valid number, starting with 256666

# Check if the number is in range.
# if the last digit is 10
    # Move up a place, add 1
    # if the result isn't 10 then:
        # Pad the rest of the number with that digit
    # else:
        # Move up another digit, add 1.
    # subtract 1
    # goto the start of the loop
# if the number satisfies the double digit condition
    # Increment the count
# Increment the number by 1 and goto start


idx = 256666
end = 699999

possible = 0

passcode = [6,6,6,6,5,2]
#passcode = [0,0,0,0]
idx = 0

def roll_up(passcode):
    idx = 1
    #  Carry up until we stop overflowing.
    while True:
        passcode[idx] += 1
        if passcode[idx] >= 10:
            idx += 1
            continue
        else:
            break
    padval = passcode[idx]
    idx -= 1
    # Now carry the value down to pad the number out.
    while idx >= 0:
        passcode[idx] = padval
        idx -= 1
    return

def is_valid(passcode):
    idx = 0
    valid = False
    last = passcode[0]
    for idx in range(1, len(passcode)):
        if last == passcode[idx]:
            valid = True
            break
        else:
            last = passcode[idx]
    return valid

def ppc():
    global passcode
    for idx in range(5,-1,-1):
        print(passcode[idx], end="")
    print("")


while passcode[5] < 7:
    if passcode[0] >= 10:
        roll_up(passcode)
    if is_valid(passcode):
        possible += 1
        ppc()
    passcode[0] += 1

# Above logic identifies 777777 as valid, remove it!
possible -= 1

print(possible)


