# BuildWordMap.py
#
# Creates a CSV file mapping words to emotion values from input data
#
# Remove dictionary check in order to train values for slang terms.
# emotion order anger disgust fear joy sadness surprise

from WordFilter import WordFilter
from tqdm import tqdm


def buildWordMap(reset, textFile, valueFile):
    if reset:
        resetWord = open('./data/WordMap.csv', 'w')
        resetWord.close()
        resetFreq = open('./data/Frequency.csv', 'w')
        resetFreq.close()
        resetPrior = open('./data/Priors.csv', 'w')
        resetPrior.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        resetPrior.close()

    freq = extractData('./data/Frequency.csv')
    with open('./data/Priors.csv', 'r+') as priorFile:
        data = priorFile.readline().strip().split(',')
        trainSize = int(data[0])
        priors = [float(x) * trainSize for x in data[1:]]

    wf = WordFilter()

    for line in tqdm(zip(textFile, valueFile)):
        trainSize += 1
        emotionValues = line[1].strip().split(',')[1:]
        priors = [float(x) + float(y) for x, y in zip(priors, emotionValues)]

        words = wf.filterWords(line[0])

        for w in words:
            freq = updateFreq(freq, str(w), emotionValues)

    vocabSize = len(freq)
    classTotal = classCount(freq, vocabSize)
    wordMap = calcProb(freq, classTotal)
    updateFile('./data/Frequency.csv', freq)
    updateFile('./data/WordMap.csv', wordMap)

    priors = [str(x / trainSize) for x in priors]
    with open("./data/Priors.csv", "w") as priorFile:
        priorFile.write("{},".format(trainSize))
        priorFile.write(','.join(priors))

    print "\nTotal number of entries in Vocabulary: {}\n".format(len(freq))


def extractData(file):
    output = []
    with open(file, 'a+') as inFile:
        inFile.seek(0)
        for i in inFile:
            output.append(i.strip())
    return output


def updateFreq(data, word, emotionValues):
    for lineNo in range(len(data)):
        line = data[lineNo].strip().split(',')
        if line[0] == word:
            line[1:] = [int(i) for i in line[1:]]
            value = [int(i) for i in emotionValues]

            line[1] += 1
            for i in range(2, 15):
                line[i] += value[i - 2]
            line[1:] = [str(i) for i in line[1:]]
            data[lineNo] = ','.join(line)
            return data

    data.append(word + ',1,' + ','.join(emotionValues))
    return data


def classCount(data, vocab):
    output = [0] * 13
    for row in data:
        output = [float(x) + float(y) + 1 for x, y in zip(row.split(',')[2:], output)]
    return output


def calcProb(data, classCount):
    output = []
    for row in data:
        row = row.split(',')
        output.append(row[0] + ',' + ','.join([str((float(x) + 1) / y) for x, y in zip(row[2:], classCount)]))

    return output


def updateFile(file, data):
    with open(file, 'w') as outFile:
        for line in data:
            outFile.write(line + '\n')
