tree = { (None, 5): {'0': (None,2), '1': ('A',3)}, (None,2): {'0': ('B',1), '1':('C',1)} }
s = "1001011"
root = (None, 5)
i = 0
d = ""

def decode_huff(tree, s, i, key, d):
    if i < len(s):
        if key in tree:
            if s[i] in tree[key]:
                next_key = tree[key][s[i]]
                print(f'next_key={next_key} i={i} s[i]={s[i]} d={d}')
                decode_huff(tree, s, i+1, next_key, d)
            else:
                return
        else:
            d += key[0]
            key = root
            print(f'found leaf i={i} s[i]={s[i]} d={d}')
            decode_huff(tree, s, i, key, d)
    return

decode_huff(tree, s, i, (None, 5), d)


