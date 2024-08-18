import jieba


def loadDict(file: str, score: int) -> dict:
    '''
    加载积极/消极/否定词词典
    '''
    wordDict = {}
    with open(file, 'r', encoding='UTF-8') as f:
        for line in f:
            word = line.strip()
            wordDict[word] = score
    f.close()
    return wordDict


def loadSenseDict(file: str) -> dict:
    '''
    加载情感词词典,其中给出词典共分为6级
    '''
    wordDict = {}
    level = 0
    with open(file, 'r', encoding='UTF-8') as f:
        for line in f:
            if line[0] == '1' or line[0] == '2' or line[0] == '3' or line[0] == '4' or line[0] == '5' or line[0] == '6':
                level = int(line[0])
                continue
            word = line.strip()
            wordDict[word] = level
    return wordDict


def scanText(text: list, startPos: int) -> int:
    global lastSensePos, lastPuncPos, lastInversePos, score
    if startPos == len(text):
        return score

    if text[startPos] in puncDict:  # 如为标点符号，更新最后标点符号，并递归
        lastPuncPos = startPos
        scanText(text, startPos+1)

    elif text[startPos] in inverseDict:  # 同理
        lastInversePos = startPos
        scanText(text, startPos+1)

    elif text[startPos] in senseDict:
        lastSensePos = (startPos, senseDict[text[startPos]])
        scanText(text, startPos+1)

    elif text[startPos] in posiDict:
        if lastSensePos[0] < lastPuncPos and lastInversePos < lastPuncPos:
            score += 1
            scanText(text, startPos+1)

        deltaScore = 1

        if lastSensePos[0] > lastPuncPos:
            deltaScore += lastSensePos[1]
            lastSensePos = (-1, 0)

        if lastInversePos > lastPuncPos:
            deltaScore *= -1
            lastInversePos = -1

        score += deltaScore

        scanText(text, startPos+1)

    elif text[startPos] in negaDict:
        if lastSensePos[0] < lastPuncPos and lastInversePos < lastPuncPos:
            score -= 1
            scanText(text, startPos+1)

        deltaScore = -1

        if lastSensePos[0] > lastPuncPos:
            deltaScore -= lastSensePos[1]
            lastSensePos = (-1, 0)

        if lastInversePos > lastPuncPos:
            deltaScore *= -1
            lastInversePos = -1

        score += deltaScore

        scanText(text, startPos+1)

    else:
        scanText(text, startPos+1)


# Main
posiDict = loadDict("./docs/tunaposi.txt", -1)  # 积极词典
negaDict = loadDict("./docs/tunanega.txt", 1)  # 消极词典
inverseDict = loadDict("./docs/inverse.txt", -1)  # 否定词典
puncDict = loadDict("./docs/punc.txt", 1)  # 标点符号
senseDict = loadSenseDict("./docs/sense.txt")  # 情绪词词典
lastSensePos: tuple = (0, 0)  # 记录最后情感词位置以及程度，-1代表没有未使用的情感词
lastInversePos: int = 0  # 记录最后否定词位置，-1意义同上
lastPuncPos: int = 0  # 记录最后标点符号位置
score: int = 0  # 记录情感得分

text = input("sentence:").strip()
textCut = list(jieba.cut(text, cut_all=False))  # 分词

scanText(textCut, 0)
# print(textCut)
print(score)
