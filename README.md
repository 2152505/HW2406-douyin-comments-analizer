# douyin-comments-analizer
douyin comments analizer
实际上，开发是根据juejin来进行的。

# 2152505 实验报告

## 实验背景和目的

掘金是一个专注于技术的网站，用户可以在上面分享和讨论技术相关的文章、教程、问答等内容。为了更好地了解用户对掘金网站的体验和偏好，我们编写了一个爬虫程序，用于爬取掘金网站上特定主题的文章，并进行多类分析。

爬取掘金特定主题文章并进行多类分析从本质上来讲并无特殊新意，但通过爬取和分析，我们可以了解用户对掘金网站的体验和偏好，进而改进网站的设计和功能。同时网上关于playwright过反扒二维码机制的文章并不多，本实验尝试使用opencv和ddddocr库进行过关，并尝试使用playwright进行自动化爬取，以期获得更好的爬取效果。

同时我们使用词云技术对爬取到的文章内容进行可视化处理，以展示文章内容的整体结构和分布情况。

最后使用tkinter进行UI设计，以实现一个完整的爬虫程序。


## 技术栈

- **js逆向技术**：用于绕过网站的前端加密和反爬虫机制。
- **xpath分析**：用于解析网页，快速定位和提取网页中的数据。
- **Playwright技术**：自动化测试工具，用于模拟浏览器行为，实现自动化爬取网页数据。
- **OpenCV技术**：用于处理可能遇到的图像验证码。
- **ddddocr技术**：一个OCR库，用于识别和处理图像中的文字信息。
- **Tkinter UI界面**：使用Tkinter为基础进行UI界面设计，同时提供了Tkinter+Figma设计的可能性，在resources文件夹中提供了build文件夹下提供了Figma文件，您可以通过Figma进行UI界面设计。
- **WordCloud词云技术**：用于对爬取到的文章内容进行可视化处理，以展示文章内容的整体结构和分布情况。
- **情感分析技术**：用于对爬取到的文章内容进行情感倾向性判断。

## 实验过程
### 1. 环境准备

- 安装Node.js、Python和相关库（Playwright、OpenCV、ddddocr等）。
### 2. 网站分析

- 使用浏览器的开发者工具分析掘金网站的结构和反爬机制。
- 确定需要使用js逆向的地方，以及可以应用xpath进行数据提取的结构。
- 分析掘金网站结构，登录窗口的滑块验证方式

![](./resources/LabImage1.png)
![](./resources/iframe1.png)

```python
# 获取frame
from playwright.sync_api import sync_playwright
p=sync_playwright().start()
browser=p.chromium.launch(headless=False)
page=browser.new_page()
page.goto("https://cdn2.byhy.net/files/selenium/sample2.html")
frame = page.frame_locator("iframe[src='sample1.html']")

# 再 在其内部进行定位
lcs = frame.locator('.animal').all()
```

定位之后截获图片的url获取图片

![](./resources/action.png)
![](./resources/basic.jpeg)

注意，每次获取得到的图片都不会一样，要注意。

### 3. 数据爬取

- 对遇到的图像验证码，使用OpenCV和ddddocr技术进行处理和识别。编写爬虫代码，通过playwright库模拟浏览器行为，获取滑块验证码图片，并调用第三方库识别滑块验证码

![](./result/1717489415.jpg)

<video src="./resources/SuccesOne.mp4"></video>

- 当然，您也可以使用登录之后将cookies保留，进行登录使用，我们提供了这种方式。您只需要第一次进行登
录，然后就可以免登录进行内容爬取和分析，如果给您试图构建一个完全自动化的工具，本文提供的openc精度可能并不足以支持完全自动化，因此建议您改进CVPassconfirm文件中的验证码识别之后再进行构建。我们使用了两种方式进行识别，opencv templatematch的精度大约能到每七次，正确一次，ddddocr大约五次中可以正确一次。

- 使用Playwright模拟用户登录、浏览特定话题的文章。
- 应用xpath分析技术提取文章标题、作者、发布时间和内容等信息。

### 4. 数据处理和情感分析

- 对爬取到的文章内容进行预处理，包括去除HTML标签、特殊字符等。
- 获取到的URLS在控制台输出：
![](../douyin-comments-analizer/resources/URLS.png)

- 获取到的文章标题在控制台输出：
![](../douyin-comments-analizer/resources/title.png)

- 使用情感分析库或模型对文章内容进行情感倾向性判断。

### 5.UI界面设计

![](./resources/UI.png)

## 实验结果

- 成功爬取了掘金网站上特定话题下的100篇文章。
- 通过情感分析，发现大部分文章呈现积极正面的情绪，少部分文章中性或略带负面情绪。

## 参考博客  
您可以直接点击对应标题，博客是本地资源，您可以直接查看，这些都是在写代码的时候所遇到的技术问题。

[端口号使用问题](./reference/[端口号问题]使用git时遇到Failed%20to%20connect%20to%20github.com%20port%20443%20after%2021090%20ms_%20Couldn‘t%20connect%20to%20server_git%20couldn't%20connect%20to%20server.html)

[codeRunner配置](./reference/codeRunner%20配置.html)

[GH103报错github](./reference/GH103报错github.html)

[iframe理解](./reference/iframe理解.html)

[locator.filter()过滤定位器](./reference/locator.filter()过滤定位器.html)

[playwright使用指令集锦](./reference/playwright使用指令集锦.html)
[playwright基本定位方式](./reference/playwright基本定位方式.html)

[playwright安装](./reference/playwright安装.html)

[python多进程处理](./reference/python多进程处理.html)

[xpath定位方法](./reference/xpath定位方法.html)

[【playwright】拖动功能基础参数](./reference/【playwright】拖动功能基础参数.html)

[关闭代理解决pip安装第三方包时因 SSL 报错](./reference/关闭代理%20解决%20pip%20安装第三方包时因%20SSL%20报错_pip%20ssl.html)

[将多个参数传递给pool](./reference/将多个参数传递给pool.map().html)

[异步asyncio库导入基础异步了解](./reference/异步asyncio库导入%20基础异步了解.html)

[模糊匹配标签](./reference/模糊匹配标签.html)

[详解Playwright启动edge、chrome和firefox的正确方法](./reference/详解Playwright启动edge、chrome和firefox的正确方法.html)

[重复可被定位元素报错](./reference/重复可被定位元素报错.html)

