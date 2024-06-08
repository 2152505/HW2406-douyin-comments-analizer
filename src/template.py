from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(channel="msedge",headless=False)
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

    # 对每个搜索结果页面进行分析
    for url in result_urls:
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
        print(title)
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

with sync_playwright() as playwright:
    run(playwright)