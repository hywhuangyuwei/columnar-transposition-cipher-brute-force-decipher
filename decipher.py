from pycipher import ColTrans  # a library for columnar transposition cipher

# YOUR INPUT HERE
cipherText = 'vuyufllniemeencraaieeyrxbiyivsevbtosogtcychrriixiassst'
dicFilename = '1-1000.txt'
maxKeyLength = 9
# USE `PYTHON DECIPHER.PY` TO START DECIPHERING


def bruteForceDecipher(cipherText, perms, dic):
    '''
    params: cipherText, permutations, dictionary

    return: decipher result with score by brute force method
    '''
    index = 0
    ranked = []

    # seach all possible keys
    for key in perms:
        index += 1
        if (index % 10000 == 0):
            print(index, 'th', end=' ')
            print('Key:', key)

        # input: key, cipherText
        # output: plainText
        plainText = ColTrans(key).decipher(cipherText)

        # get a `score` for the key
        # score = the number of words exist both in the plainText and in the dictionary
        score = 0
        wordFound = []
        for word in dic:
            _cnt = plainText.count(word)
            if _cnt > 0:
                score += _cnt
                wordFound.append(word.lower())
        ranked.append([score, plainText, ','.join(wordFound)])

    return ranked


def getAllPermutation(n):
    '''
    params: n

    return: a list of all permutations of n, each item is a string
    '''
    global _perms

    def perm(n, begin, end):
        global _perms
        if begin >= end:
            _perms += n
        else:
            i = begin
            for num in range(begin, end):
                n[num], n[i] = n[i], n[num]
                perm(n, begin + 1, end)
                n[num], n[i] = n[i], n[num]
    a = []
    for i in range(1, n+1):
        a.append(i)
    perm(a, 0, n)
    res = []
    temp = 1
    for w in range(1, n+1):
        temp *= w
    for j in range(0, temp):
        tmp = _perms[j*n:j*n+n]
        tmp = list(map(str, tmp))
        tmp = ''.join(tmp)
        res.append(tmp)

    print('Total:', len(res))

    return res


def importWords(filename):
    '''
    input: filename of dictionary

    output: a list containing all words IN UPPER CASE in the dictionary
    '''
    dic = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            line = line[:-1].upper()
            dic.append(line)
            line = file.readline()
        return dic


ranked = []

print('Importing dictionary...')
dic = importWords(dicFilename)

for i in range(1, maxKeyLength+1):
    _perms = []
    print('=====\nPermutation (n = %d)...' % i)
    perms = getAllPermutation(i)
    print('Brute force decipher...')
    ranked += bruteForceDecipher(cipherText, perms, dic)

print('=====\nSorting result by score...')
ranked = sorted(ranked, key=lambda item: item[0], reverse=True)
for i in range(50):
    print(ranked[i][1].lower(), 'score=' + str(ranked[i]
                                               [0]), 'word=' + ranked[i][2], sep='|')
