#Extract text from article
#Main lib: pip install pypdf

import re
import sys
from pypdf import PdfReader

def main():
    if len(sys.argv) != 2: #standard input
        print("Error. Run: $ python3 extractTextFromArticle.py <article path>")
        sys.exit(1)

    pathFile = sys.argv[1]

    stringTarget = "Abstract" #extract until Abstract

    reader = PdfReader(pathFile)
    numPages = len(reader.pages)

    finalText = ""

    with open("article.txt", "w", encoding="utf-8") as file:
        for i in range(1, numPages):
            currentPage = reader.pages[i]
            currentText = currentPage.extract_text()

            if currentText and currentText.strip(): #check if current page can be extracted
                if stringTarget in currentText: #extract text until Abstract
                    cutText = currentText.split(stringTarget, 1)[0]
                    finalText += cutText
                    break
                else:
                    finalText += currentText
            else:
                print(f"Can't extract text from {i} page")                

        finalText = re.sub(r'\s+\d+\s+\.', '.', finalText) #ignore article references as "comunidade¹"
        #finalText = re.sub(r'(?<=\w)\s+\d+(?:,\d+)*', '', finalText) #ignore article references as "recreativas ilícitas²⁰,²¹" but also ignore "45%"
        file.write(finalText)

    file.close()

if __name__ == "__main__":
    main()
