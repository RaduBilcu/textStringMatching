import csv
from itertools import accumulate
from Levenshtein import distance as levenshtein_distance
from Levenshtein import hamming as levenshtein_hamming

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #inNameCSV = "E:/3WorkAndTechnical/SWdevelopment/Matlab/Betting/names_la_liga.csv"
    #outNameCSV = "E:/3WorkAndTechnical/SWdevelopment/Matlab/Betting/names_la_liga_Matched_Python.csv"

    inNameCSV = "E:/3WorkAndTechnical/SWdevelopment/Matlab/Betting/names_Ligue_1.csv"
    outNameCSV = "E:/3WorkAndTechnical/SWdevelopment/Matlab/Betting/names_Ligue_1_Matched_Python.csv"

    inNameCSV = "E:/3WorkAndTechnical/SWdevelopment/Matlab/Betting/names_serie_A.csv"
    outNameCSV = "E:/3WorkAndTechnical/SWdevelopment/Matlab/Betting/names_serie_A_Matched_Python.csv"

    with open(inNameCSV, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)  #Just to consume the header of the csv file
        content = []
        for row in csvreader:
            content.append(row[0:3])
    #*****We count the number of betting websites and their number of games, in the input csv file*****
    websiteName = content[0][0]#Take the name of the first betting website
    pagesCount = 0#The counter which counts the number of betting websites
    gamesCount = []#The list which keeps the number of games in each website
    gamesCount.append(1)#Initialize the list with 1 in the first position since we have at least one line in the csv file which means at least one website with one game
    for index in range(1, len(content)):#Search the entire content of the csv file and count the websites and their games
        websiteNameTemp = content[index][0]
        if websiteName == websiteNameTemp:
            gamesCount[pagesCount] = gamesCount[pagesCount] + 1
        else:
            pagesCount = pagesCount + 1
            gamesCount.append(1)
            websiteName = websiteNameTemp
    pagesCount = pagesCount + 1
    print('Found a number of ', pagesCount, ' webpages in the Excell file')
    print('Found a number of ', gamesCount, ' footbal games in those pages.')
    #**************************************************************************************************
    corespondenceMatrix = [[0]*pagesCount for _ in range(gamesCount[0])]#This matrix will have a number of lines equal to the number of games in the first webpage and the number
                                                        #of columns equal to the number of webpages
    corespondenceCell = [[' ']*3 * pagesCount for _ in range(gamesCount[0])]#This is the cell which contains the corresponding games between the different webpages
    firstPageData = [[0] * 3 for _ in range(gamesCount[0])]  # This is the cell which contains the corresponding games between the different webpages
    name1FirstPage = []
    name2FirstPage = []
    for index in range(0, gamesCount[0]):
        corespondenceMatrix[index][0] = index
        corespondenceCell[index][0] = content[index][0]
        corespondenceCell[index][1] = content[index][1]
        corespondenceCell[index][2] = content[index][2]
        firstPageData[index][0] = content[index][0]
        firstPageData[index][1] = content[index][1]
        firstPageData[index][2] = content[index][2]
        name1FirstPage.append(content[index][1])
        name2FirstPage.append(content[index][2])
#    print('corespondenceMatrix=', corespondenceMatrix)
    scoreMatrix = [[float('inf')]*pagesCount for _ in range(gamesCount[0])]#The matrix of the game matching scores
    gamesCountCum = gamesCount.copy()#Take a copy of the gameCount list
    gamesCountCum = list(accumulate(gamesCountCum))
    print(gamesCount)
    print(gamesCountCum)
    for indexPage in range(1, pagesCount):
        print('indexPage=', indexPage)
        otherPageData = [[0] * 3 for _ in range(gamesCount[indexPage])]  # The matrix of the game matching scores
        name1_OtherPage = []
        name2_OtherPage = []
        for i in range(gamesCountCum[indexPage-1], gamesCountCum[indexPage]):
            otherPageData[i-gamesCountCum[indexPage-1]][0] = content[i][0]#Take the whole data of the next website
            otherPageData[i-gamesCountCum[indexPage-1]][1] = content[i][1]  # Take the whole data of the next website
            otherPageData[i-gamesCountCum[indexPage-1]][2] = content[i][2]  # Take the whole data of the next website
            name1_OtherPage.append(content[i][1])
            name2_OtherPage.append(content[i][2])
        for indexFirstPage in range(0, gamesCount[0]):
            curentName1_FirstPage = name1FirstPage[indexFirstPage]
            curentName2_FirstPage = name2FirstPage[indexFirstPage]
            scoreLev = []
            for indexOtherPage in range(gamesCount[indexPage]):
                curentName1_OtherPage = name1_OtherPage[indexOtherPage]
                curentName2_OtherPage = name2_OtherPage[indexOtherPage]
                levName1 = (levenshtein_distance(curentName1_OtherPage, curentName1_FirstPage, weights=(1, 1, 2)) - levenshtein_distance(curentName1_OtherPage, curentName1_FirstPage, weights=(1, 1, 1))) / len(curentName1_OtherPage)
                levName2 = (levenshtein_distance(curentName2_OtherPage, curentName2_FirstPage, weights=(1, 1, 2)) - levenshtein_distance(curentName2_OtherPage, curentName2_FirstPage, weights=(1, 1, 1))) / len(curentName2_OtherPage)
                levName1_1 = (levenshtein_distance(curentName1_FirstPage, curentName1_OtherPage, weights=(1, 1, 2)) - levenshtein_distance(curentName1_FirstPage, curentName1_OtherPage, weights=(1, 1, 1))) / len(curentName1_FirstPage)
                levName2_1 = (levenshtein_distance(curentName2_FirstPage, curentName2_OtherPage, weights=(1, 1, 2)) - levenshtein_distance(curentName2_FirstPage, curentName2_OtherPage, weights=(1, 1, 1))) / len(curentName2_FirstPage)
                scoreLev.append(levName1 + levName2 + levName1_1 + levName2_1)
            minimScore = min(scoreLev)
            if minimScore < 1:#We found at least a minimum
                I = []
                for ind in range(len(scoreLev)):
                    if scoreLev[ind] == minimScore:
                        I.append(ind)
                if len(I) == 1:
                    corespondenceMatrix[indexFirstPage][indexPage] = I
                    scoreMatrix[indexFirstPage][indexPage] = minimScore
                    corespondenceCell[indexFirstPage][3*indexPage] = otherPageData[I[0]][0]
                    corespondenceCell[indexFirstPage][3 * indexPage + 1] = otherPageData[I[0]][1]
                    corespondenceCell[indexFirstPage][3 * indexPage + 2] = otherPageData[I[0]][2]
    for indexColumn in range(1, pagesCount):
        for indexLine in range(gamesCount[0]-1):
            corrCurent = corespondenceMatrix[indexLine][indexColumn]
            if corrCurent != 0:
                for indexSubLine in range(indexLine + 1, gamesCount[0]):
                    if corespondenceMatrix[indexSubLine][indexColumn] == corrCurent:
                        if scoreMatrix[indexSubLine][indexColumn] < scoreMatrix[indexLine][indexColumn]:#We found a match which is close
                            scoreMatrix[indexLine][indexColumn] = float('inf')#We put the score of the larger element in Inf
                            corespondenceMatrix[indexLine][indexColumn] = 0
                            corespondenceCell[indexLine][3*indexColumn] = ' '
                            corespondenceCell[indexLine][3 * indexColumn + 1] = ' '
                            corespondenceCell[indexLine][3 * indexColumn + 2] = ' '
                            break
                        else:
                            scoreMatrix[indexSubLine][indexColumn] = float('inf')
                            corespondenceMatrix[indexSubLine][indexColumn] = 0
                            corespondenceCell[indexSubLine][3*indexColumn] = ' '
                            corespondenceCell[indexSubLine][3 * indexColumn + 1] = ' '
                            corespondenceCell[indexSubLine][3 * indexColumn + 2] = ' '
    print(scoreMatrix)
    with open(outNameCSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(corespondenceCell)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
