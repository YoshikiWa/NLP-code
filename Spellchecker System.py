import operator
from tkinter import *
import nltk
from nltk import *
from nltk import ngrams
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
global v, w, s, p

# make dictionary
TxtContent = open("big.txt", 'r').read()
TxtContent = re.sub('[^a-zA-Z]+', ' ', TxtContent)
wordList = set(TxtContent.lower().split())
wordList = sorted([w for w in wordList if len(w) > 3])

# N-Grams are used to process words(ngram and bigram)
Bigram1 = list(ngrams(TxtContent.lower().split(), 2))
Ngram = list(ngrams(TxtContent.lower().split(), 1))

Ngram = nltk.FreqDist(Ngram)
Bigram2 = nltk.FreqDist(Bigram1)
Fdist = Bigram2.keys()
ngram_counts = Counter(Ngram)
ngram_elements = ngram_counts.most_common()
bigram_counts = Counter(Bigram2)
bigram_elements = bigram_counts.most_common()

topNgrams = {}
bigramCount = {}
def Convert(tup, di):
    for a, b in tup:
        di.update({a[0]: b})
    return di

topNgrams = Convert(ngram_elements, topNgrams)

def getWords(tup, di):
    for a, cnt in tup:
        di.update({(a[0], a[1]): cnt})
    return di

bigramCount = getWords(bigram_elements, bigramCount)

# GUI
root = Tk()
root.title('Spellchecker System')
root.geometry("650x550+20+10")
root.config(background="lightblue")

label_title = Label(root, text="Enter your text here.", font=("Arial", 20, "bold"), bg="lightyellow", fg="black")
label_title.grid(column = 0, row = 0, sticky = W)


label_title2 = Label(root, text="Dictionary")
label_title2.grid(column = 1, row = 0, sticky = W)

def DeclareWord_CharCountFunc():

    TextContent = input_text.get("1.0", END)
    # Turn The Contents (String) to a Number Value
    CharactersInTextBox = len(TextContent)
    WordsInTextBox = len(TextContent.split())
    # Update the Display Label to Show Number of Characters the Words in TextBox
    DisplayLabel.config(text=str(CharactersInTextBox - 1) + " Characters, " + str(WordsInTextBox) + " Words")

def InitWord_CharCount():
    DeclareWord_CharCountFunc()
    DisplayLabel.after(1000, InitWord_CharCount)


input_text = tkinter.Text(root, width = 90, height = 35, font=("Arial", 8), wrap = WORD)
input_text.grid(column = 0, row = 2, sticky = W)


DisplayLabel = Label(root, text="", font=("Arial", 10))
DisplayLabel.grid(row=5, column=0, padx=15)

label_search = Label(root, text="Search")
label_search.grid(column = 1, row = 4, sticky = W)


label_title3 = Label(root, text="NoneWE = RED")
label_title3.grid(column = 0, row = 4, sticky = W)


label_title4 = Label(root, text="RealWE = BLUE")
label_title4.grid(column = 0, row = 5, sticky = W)


txt_search = Entry(root)
txt_search.grid(column = 1, row = 5)
search_list = Listbox(root, width = 25, height = 18, bg="lightpink")
search_list.grid(column = 1, row = 2, sticky = W)
for word in wordList:
    search_list.insert(tkinter.END, word)

# Calculate Edit distance
def minDistance(target, source):
    n = len(target)
    m = len(source)
    insert_cost = 1
    subs_cost = 1
    delete_cost = 1
    transposition_cost = 1

    distance = numpy.zeros((len(source) + 1, len(target) + 1), dtype=int)

    for i in range(1, m + 1):
        distance[i, 0] = distance[i - 1, 0] + delete_cost

    for j in range(1, n + 1):
        distance[0, j] = distance[0, j - 1] + insert_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            tmpSub_cost = subs_cost
            if source[i - 1] == target[j - 1]:
                tmpSub_cost = 0

            distance[i, j] = min(distance[i, j - 1] + insert_cost,
                                 distance[i - 1, j] + delete_cost,
                                 distance[i -1, j - 1] + tmpSub_cost)

            if i > 1 and j > 1 and source[i - 1] == target [j - 2] and source[i - 2] == target[j - 1]:
                distance[i, j] = min(distance[i, j],
                                     distance[i - 2, j - 2,] + transposition_cost)
    return distance[m, n]

# Execution process of the program
# Check if the word is correct and return a list of suggestions
def checkSpelling(words):
    word_dic = {}
    initial_Word = words.split()
    initial_Word = [i.strip() for i in initial_Word]
    word_list = words.split()
    p = round(100 / len(word_list), 2)
    item = 0
    cnTP = 0
    lastCall = False
    for i in word_list:
        cnTP += 1
        if cnTP == len(word_list):
            lastCall = True
        item = round(item + p, 2)
        k = i
        k = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", ' ', k)
        k = k.lower().strip()

        if (not (k in wordList) and not (k in stop_words)):
            tmpWord_dic = checkCorrection(k)
            m = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", ' ', i)
            word_dic.update({m.strip(): tmpWord_dic})
        elif (k in stop_words):
            m = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", ' ', i)
            word_dic.update({m: {}})
        elif (k in wordList):
            m = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", ' ', i)
            word_dic.update({m.strip(): {}})
    return checkNonWordError(word_list, initial_Word, word_dic), word_dic, word_list, initial_Word

# Edit distance algorithm is used to calculate the distance between the wrong word and the proposed correction word
def checkCorrection(word):
    words_dic = {}
    for i in wordList:
        distance = minDistance(word, i)
        if i in topNgrams:
            words_dic.update({i: int(distance)})
    words_dic = sorted(words_dic.items(), key=operator.itemgetter(1))
    return words_dic

# Check for real word errors
def checkNonWordError(word_list, unChangeWord, word_dic):
    real_wordError = {}
    li = []
    p = round(100 / len(word_list), 2)
    item = 0
    cnTP = 0
    lastCall = False
    for i in range(0, len(word_list)):
        cnTP += 1
        if cnTP == len(word_list):
            lastCall = True
        item = round(item + p, 2)
        if (i > 0):
            key = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", '', word_list[i])
            if key in word_dic:
                if (len(word_dic[key]) == 0):
                    prevWord = i - 1
                    Word1 = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", ' ', word_list[i])
                    Word1 = Word1.lower().strip()
                    Word2 = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", ' ', word_list[prevWord])
                    Word2 = Word2.lower().strip()
                    endOfsen = word_list[prevWord]
                    if (endOfsen[-1] != '.'):
                        probability = bigramWords(Word2, Word1)
                        if (probability <= 0):
                            key = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", ' ', word_list[prevWord])
                            if key in word_dic:
                                if (len(word_dic[key]) == 0):
                                    li = getCorrectionsRealWord(Word2, Word1)
                                else:
                                    li = getCorrectionsRealWord(Word1, Word1)
                            else:
                                pass
                            if len(li) == 0: li.append("No corrections found")
                            m = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", ' ', word_list[i])
                            real_wordError.update({(i, m.strip()): li})
            else:
                pass
    return real_wordError

# Calculate the probability of the existence of two words
def bigramWords(prevWord, word):
    Probability = 0.0
    if (prevWord, word) in bigramCount:
        return bigramCount[prevWord, word] / topNgrams[prevWord]
    else:
        return Probability

# Suggested set of word modifications
def getCorrectionsRealWord(prevWord, currentWord):
    real_wordError = []
    for i in wordList:
        real_wordError.append(i)
    real_wordError = checkCorrection(currentWord)
    return real_wordError[:7]

# GUI interaction
# Identify incoming text and highlight words that need to be modified in blue and words that don't exist in red
def get_text():
    tag1 = "wordError"
    tag2 = "realWord"
    text = (input_text.get(1.0, END))
    text1 = text.split()

    if (len(text1) > 500):
        remove = len(text1) - 500
        if (remove == 1):
            remove = 2
            input_text.delete(1.0, END)
            input_text.insert(1.0, text[:-remove])
    text = (input_text.get(1.0, END))
    global corrections, realWord, word_list

    realWord, corrections, word_list, unChanged = checkSpelling(text)
    input_text.delete(1.0, END)
    for i in range(0, len(word_list)):
        key = key = re.sub(r"[-()\"#@:<>{}`+=~|.?!,1234567890]", '', word_list[i])
        if (key in corrections and len(corrections[key]) > 0):
            endOfsen = word_list[i]
            endOfsen = endOfsen[-1]
            w = word_list[i]
            if endOfsen[-1] == '.' or endOfsen[-1] == ',' or endOfsen[-1] == '?':
                w = word_list[i]
                w = w[:-1]
                endOfsen = endOfsen[-1] + " "
            else:
                endOfsen = " "
            input_text.insert(INSERT, w, tag1)
            input_text.tag_configure(tag1, foreground="red")
            input_text.insert(INSERT, endOfsen)
        elif ((i, key) in realWord):
            endOfsen = word_list[i]
            endOfsen = endOfsen[-1]
            w = word_list[i]
            if endOfsen[-1] == '.' or endOfsen[-1] == ',' or endOfsen[-1] == '?':
                w = word_list[i]
                w = w[:-1]
                endOfsen = endOfsen[-1] + " "
            else:
                endOfsen = " "
            input_text.insert(INSERT, w, tag2)
            input_text.tag_configure(tag2, foreground="blue")
            input_text.insert(INSERT, endOfsen)
        else:
            endOfsen = word_list[i]
            endOfsen = endOfsen[-1]
            w = word_list[i]
            if endOfsen[-1] == '.' or endOfsen[-1] == ',' or endOfsen[-1] == '?':
                w = word_list[i]
                w = w[:-1]
                endOfsen = endOfsen[-1] + " "
            else:
                endOfsen = " "
            input_text.insert(INSERT, w)
            input_text.insert(INSERT, endOfsen)
    print("Check Done")

# The right mouse button displays the correction suggestion
def show_popup(e):
    count = 0
    try:
        text = input_text.selection_get().strip()
        corrections_menu.delete(0, 'end')
        text = re.sub(r"[-()\"#/@:;<>{}`+=~|.!?,]", '', text)
        if (text in corrections and len(corrections[text]) > 0):
            for i in corrections[text]:
                count += 1
                if count > 7:
                    break
                corrections_menu.add_command(label=i[0])
            corrections_menu.post(e.x_root, e.y_root)
        else:
            for i in range(0, len(word_list)):
                if ((i, text) in realWord):
                    l = realWord[i, text]
                    for k in l:
                        corrections_menu.add_command(label = k[0])
                    break
            corrections_menu.post(e.x_root, e.y_root)
    except:
        pass

# Search the word in the dictionary
def search():
    search_list.itemconfig(0, foreground='', background='')
    search_list.delete(0, tkinter.END)
    for word in wordList:
        search_list.insert(tkinter.END, word)
    text = txt_search.get()
    search_list.config(state=NORMAL)
    tmp = wordList

    if (text.strip() in tmp):
        num = tmp.index(text.strip())
        search_list.delete(num)
        search_list.insert(0, text.strip())
        search_list.itemconfig(0, foreground='green', background='yellow')
    else:
        search_list.insert(0, "ITEM NOT FOUND")
        search_list.itemconfig(0, foreground='red', background="yellow")

btn_search = Button(root, text='Search', command=search)
btn_search.grid(column=1, row=6)
btn_Get = Button(root, text = 'Check for corrections', command = get_text)
btn_Get.grid(column = 0, row = 6)
corrections_menu = Menu(root)

root.bind("<Button-3>", show_popup)
InitWord_CharCount()
root.mainloop()