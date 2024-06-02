from playwright.sync_api import sync_playwright  

def LogInWebsite():
    with sync_playwright() as p:  
        browser = p.chromium.launch(headless=False)  
        context = browser.new_context()  
        page = browser.new_page()  
        page.goto("https://juejin.cn/")  
        page.wait_for_timeout(1000)  
        page.get_by_role("button", name="登录 注册").click()  
        page.wait_for_timeout(1000)  
        page.get_by_text("密码登录").click()  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("请输入邮箱/手机号（国际号码加区号）").click()  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("请输入邮箱/手机号（国际号码加区号）").fill("13394208751")  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("请输入密码").click()  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("请输入密码").fill("Lxy252799")  
        page.wait_for_timeout(1000)  
        page.get_by_role("button", name="登录", exact=True).click()  
      
        page.pause()  


if __name__ == "__main__":
    LogInWebsite()