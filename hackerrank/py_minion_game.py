import sys

def calc_score(word, string):
    found = 0
    count = 0
    while found > -1:
        found = string.find(word, found)
        if found > -1:
            count += 1
            found += 1
    return count
            

def match(s, substr, score, size, string):
    if size < len(substr):
        score = match(s, substr, score, size+1, string)
    score += calc_score(s+substr[:size], string) 
    print("match", s, substr[:size], score)
    return score

def minion_game(string):
    # your code goes here
    vowels = ['A','E','I','O','U']
    scores = [0,0] # stuart and kevin
    seens = [[], []]
    print('start', string)
    for i, s in enumerate(string):
        if s not in vowels:
            # this is for stuart
            if s not in seens[0]:
                scores[0] += calc_score(s, string)
                print('stuart', s, scores[0])
                scores[0] = match(s, string[i+1:], scores[0], 1, string)
                seens[0].append(s)
        else:
            # this is for kevin
            if s not in seens[1]:
                scores[1] += calc_score(s, string)
                print('kevin', s, scores[1])
                scores[1] = match(s, string[i+1:], scores[1], 1, string)
                seens[1].append(s)
                
    #if scores[0] > scores[1]:
    print("Stuart", scores[0])
    #elif scores[1] > scores[0]:
    print("Kevin", scores[1])
    #else:
    #    print("Draw")

if __name__ == '__main__':
    string = "BANANA"
    if len(sys.argv) > 1:
        string = sys.argv[1]
    minion_game(string)
