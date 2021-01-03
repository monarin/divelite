import sys
s = sys.argv[1]

vowels = 'AEIOU'

kevsc = 0
stusc = 0
for i in range(len(s)):
    if s[i] in vowels:
        kevsc += (len(s)-i)
        print('kevin', s[i], kevsc)
    else:
        stusc += (len(s)-i)
        print('stuart', s[i], stusc)


print(kevsc, stusc)
if kevsc > stusc:
    print("Kevin", kevsc)
elif kevsc < stusc:
    print("Stuart", stusc)
else:
    print("Draw")
