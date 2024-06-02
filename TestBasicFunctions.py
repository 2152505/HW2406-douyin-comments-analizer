from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

import asyncio
# 基本使用方法
# 测试同步模式
def test_sync():
    with sync_playwright() as p:
    # playwright执行默认运行的浏览器是chromium！
    # Chromium不是我们熟知的Chrome！Chromium OS是一个开源项目，主要由开发人员使用，其代码可供任何人检出、修改和构建。
    # 可以简单的理解二者的区别：Chromium 是开源的，Chrome 是闭源的，Chrome 特性更丰富。
        browser = p.chromium.launch(channel="msedge",headless=False)
        #如果使用参数headless=False，那么浏览器不会启动，会以无头模式运行脚本。
        page = browser.new_page()
        page.goto('https://www.douyin.com/?recommend=1')
        print(page.title)
        browser.close()
# 测试异步模式
async def test_async():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://www.baidu.com")
        print(await page.title())
        await browser.close()