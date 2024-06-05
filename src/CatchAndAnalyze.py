from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import seaborn as sns
import CreateStopList
import matplotlib.font_manager

def CatshAndAnalyze():
    fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

    print('fonts: \n'.join(fonts))
    # 使用Playwright打开掘金网站，并搜索"红楼梦"
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge",headless=False)
        #要带参不然浏览器不会启动
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://juejin.cn/")
        page.wait_for_timeout(3000)
        
        
        page.get_by_placeholder("探索稀土掘金").click()
        page.wait_for_timeout(1000)
        page.get_by_placeholder("搜索文章/小册/标签/用户").fill("红楼梦")
        
        page.get_by_role("search").get_by_role("img").click()
        with page.expect_popup() as page1_info:
            page.get_by_role("link", name="图解 Vue 3 组件通信：红楼梦剧情演绎版", exact=True).click()
        page1 = page1_info.value
        page1.get_by_role("heading", name="生拉硬扯：从红楼梦到 Vue").click()
        print(page1)
        #=====================================================================
        #这里还是要点评以下，写playwright简本最好的办法就是使用codegen工具
        #=====================================================================
        html=page.content()
        
        context.close()
        browser.close()



    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('div', class_='content-box')
    text = ' '.join(article.get_text() for article in articles)
    print("text: ",text)
    # 清洗数据
    CreateStopList.creatStopList()

    stopwords = set(line.strip() for line in open('../resources/stopwords.txt', 'r', encoding='utf-8').readlines())
    seg_list = jieba.cut(text, cut_all=False)
    seg_text = ' '.join(seg for seg in seg_list if seg not in stopwords)

    print("seg_text: ",seg_text)

    # 使用TextBlob进行情感分析
    blob = TextBlob(text)
    print(f"情感极性: {blob.sentiment.polarity}")
    # 假设documents是一个包含多个字符串的列表，每个字符串代表一个文档
    documents = seg_text.split()

    vectorizer = CountVectorizer(stop_words='english')
    data_vectorized = vectorizer.fit_transform(documents)

    # 使用LDA进行主题建模
    lda_model = LatentDirichletAllocation(n_components=5)
    lda_model.fit(data_vectorized)

    # 显示每个主题的前10个关键词
    def print_top_words(model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            message = "Topic #%d: " % topic_idx
            message += " ".join([feature_names[i]
                                for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(message)
    print("Dir: ",dir(vectorizer))
    print_top_words(lda_model, vectorizer.get_feature_names_out(), 10)

    # 显示词云
    wc = WordCloud(font_path='simhei.ttf', background_color='white', width=800, height=600)
    wordcloud = wc.generate(seg_text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    # 显示情感极性分布
    blob = TextBlob(seg_text)
    sentiment_polarity = [sentence.sentiment.polarity for sentence in blob.sentences]
    sns.displot(sentiment_polarity, kde=True)
    plt.title('Emotion distribution')
    plt.show()
