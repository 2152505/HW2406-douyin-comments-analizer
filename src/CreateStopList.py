stopwords = ['的', '了', '在', '是', '我', '有', '和', '就', 
             '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', 
             '去', '你', '会', '着', '看', '没有', '好', '自己', '这']
def creatStopList():
    with open('../resources/stopwords.txt', 'w', encoding='utf-8') as f:
        for word in stopwords:
            f.write(word + '\n')