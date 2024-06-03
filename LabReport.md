# 2152505 实验报告

## 实验背景和目的

为了爬取抖音评论并进行分析

## 技术栈

python

pandas

numpy

matplotlib

## 实验过程

1. 分析掘金网站结构，登录窗口的滑块验证js方式

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

2. 编写爬虫代码，通过selenium库模拟浏览器行为，获取滑块验证码图片，并调用第三方库识别滑块验证码

![](./resources/LabImage2.png)

3. 编写爬虫代码，通过selenium库模拟浏览器行为，获取滑块验证码图片，并调用第三方库识别滑块验证码

![](./resources/LabImage3.png)

4. 清洗数据

5. 分析数据

## 实验结果

1. 爬取到的评论数据

2. 清洗后的数据

3. 分析结果

## 实验总结

本次实验让我对爬虫有了更深入的理解，学会了如何爬取抖音评论并进行数据分析。

## 实验不足

本次实验只爬取了抖音评论，没有爬取抖音用户信息。

## 实验建议

可以尝试爬取抖音用户信息，并进行分析。

## 实验参考资料
