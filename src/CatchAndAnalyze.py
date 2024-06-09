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



def run(playwright,url,search_word):
    browser = playwright.chromium.launch()
    #要带参不然浏览器不会启动
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://juejin.cn")
    page.wait_for_timeout(3000)
        
        
    page.get_by_placeholder("探索稀土掘金").click()
    page.wait_for_timeout(1000)
    page.get_by_placeholder("搜索文章/小册/标签/用户").fill("红楼梦")
        
    page.get_by_role("search").get_by_role("img").click()

    # 等待搜索结果页面加载
    page.wait_for_load_state("networkidle")

    # 提取搜索结果页面的URL
    result_urls = page.eval_on_selector_all('a.title', 'nodes => nodes.map(n => n.href)')
    print("=======================================")
    print("访问URL： ")
    print("=======================================")
    for i in result_urls:
        print(i)
    print("=======================================")
    # 对每个搜索结果页面进行分析
    print("=======================================")
    print("\n\n\n\n文章标题： ")
    print("=======================================")
    for i, url in enumerate(result_urls):
        page.goto(url)
        page.wait_for_timeout(3000)
        #=======================================================================
        #Attention!!!!!
        #=======================================================================
        #这个wait贼tm重要，和之前验证码环节的延时是一样的，如果没有就会因为堵塞而报错
        #=======================================================================
        #在使用playwright的时候出现问题，首要考虑的就是wait_for_timeout的问题
        # 因为执行存在时间差，而页面分析是由时序的，所以需要等待页面加载完成
        #=======================================================================
        # 在这里进行URL的分析
        # 例如，提取每个页面的标题
        title = page.eval_on_selector('h1', 'node => node.innerText')
        
        print("{i}.".format(i=i+1),title)
        
    print("=======================================")
    print("©copyright@2152505 Luan Xueyu")
        
        #=====================================================================================================================================
        # 这段代码的主要目的是从搜索结果页面提取所有文章的URL，然后访问每个URL并提取文章的标题。
        # result_urls = page.eval_on_selector_all('a.title', 'nodes => nodes.map(n => n.href)')：这行代码使用eval_on_selector_all函数来查找所有的<a>标签，这些标签的类名为"title"。
        # 然后，它使用JavaScript箭头函数nodes => nodes.map(n => n.href)来获取每个<a>标签的href属性，也就是URL。所有的URL都被存储在result_urls列表中。
        # for url in result_urls:：这行代码开始一个循环，对result_urls列表中的每个URL进行操作。
        # page.goto(url)：这行代码访问每个URL。
        # title = page.eval_on_selector('h1', 'node => node.innerText')：这行代码使用eval_on_selector函数来查找<h1>标签，然后使用JavaScript箭头函数node => node.innerText
        # 来获取<h1>标签的文本，也就是文章的标题。标题被存储在title变量中。
        # 总的来说，这段代码的工作流程是：首先从搜索结果页面提取所有文章的URL，然后访问每个文章的URL，最后提取每篇文章的标题。
        #=====================================================================================================================================

    context.close()
    browser.close()
    return result_urls





def CatshAndAnalyze(url, keyword="红楼梦"):
    fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    # url=url
    # search_word=keyword
    # with sync_playwright() as p:
    #     result_urls=run(p,url,search_word)
    #     print(result_urls)
    #print('fonts: \n'.join(fonts))
    # 使用Playwright打开掘金网站，并搜索"红楼梦"
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge",headless=False)
        #要带参不然浏览器不会启动
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(1000)  
        page.get_by_role("button", name="登录 注册").click()  
        page.wait_for_timeout(1000)  
        page.get_by_text("密码登录").click()  
        page.wait_for_timeout(1000)  
            
        page.get_by_placeholder("手机号").click()  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("手机号").fill("13394208751")  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("请输入密码").click()  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("请输入密码").fill("Lxy252799")  
        page.wait_for_timeout(1000)  

        page.get_by_role("button", name="登录", exact=True).click() 
             
                # 判断是否登陆成功
        page.wait_for_timeout(10000)
        
        
        page.get_by_placeholder("探索稀土掘金").click()
        page.wait_for_timeout(1000)
        page.get_by_placeholder("搜索文章/小册/标签/用户").fill("红楼梦")
        
        page.get_by_role("search").get_by_role("img").click()
        with page.expect_popup() as page1_info:
            page.get_by_role("link", name="图解 Vue 3 组件通信：红楼梦剧情演绎版", exact=True).click()
            #page.get_by_role("link", exact=True).click()
        page1 = page1_info.value
        #page1.get_by_role("heading", name="生拉硬扯：从红楼梦到 Vue").click()
        print(page1)
        #=====================================================================
        #这里还是要点评以下，写playwright简本最好的办法就是使用codegen工具
        #=====================================================================
        html=page.content()
        #print(html)
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
    # print("Dir: ",dir(vectorizer))
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



if __name__ == '__main__':
    #CatshAndAnalyze("https://juejin.cn/post/7249706085937496123?searchId=20240606160715E7EA1098A0948911FB4E")
    CatshAndAnalyze("https://juejin.cn/")