from playwright.sync_api import sync_playwright 
# from fake_useragent import UserAgent
         
import RequestforImages
import requests
import random
import CVPassComfirm
def LogInWebsite():
    with sync_playwright() as p:  
        browser = p.chromium.launch(channel="msedge",headless=False)  
        #browser = p.chromium.launch(headless=False)  
        context = browser.new_context()  
        page = browser.new_page()  
        page.goto("https://juejin.cn/")  
        page.wait_for_timeout(1000)  
        page.get_by_role("button", name="登录 注册").click()  
        page.wait_for_timeout(1000)  
        page.get_by_text("密码登录").click()  
        page.wait_for_timeout(1000)  
        
        #如果验证码在前，则在这里进行滑块识别，例如抖音
        # imageEL = page.locator("#captcha-verify-image")  
        # # 保存图片  
        # resp = requests.get(imageEL.get_attribute("src"))  
        # with open('bg.jpeg', 'wb') as f:  
        #     f.write(resp.content)
        # page.pause()  

        page.get_by_placeholder("手机号").click()  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("手机号").fill("13394208751")  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("请输入密码").click()  
        page.wait_for_timeout(1000)  
        page.get_by_placeholder("请输入密码").fill("Lxy252799")  
        page.wait_for_timeout(1000)  
        
        #page.get_by_role("submit", name="登录", exact=True).click()  
        #注意如果是爬取抖音，这里会出现button的重复问题，需要使用submit作为标识符
        page.get_by_role("button", name="登录", exact=True).click()  
        
        #=====================================================================================
        #当元素位于iframe内置窗口下的时候，直接对元素定位是定位不到的，需要先切换到该窗口下：
        # 这个问题困扰了我很久，原本这个位置一直抓取不到对应标签，后来f12分析之后发现标签位于
        # iframe 内置窗口下，所以需要先切换到该窗口下，然后才能对该标签进行定位。
        # 整体来说滑块的解决需解决以下3个问题：
        # 1.得到滑块背景图
        # 2.计算缺口位置
        # 3.滑动轨迹（绕过防爬机制）
        # 不同的网站滑块也有区别，特别是某东的网站滑块操作防爬机制级别很高，还需要去自己写个滑动轨迹。
        # （滑块问题不是复制粘贴代码就能解决的，还需要根据实际情况去慢慢调试，比较耗时，耗经历,很费劲
        #======================================================================================
        
        #======================================================================================
        #这里记录一下心路历程，一直在这里磨蹭了好久，想找到解决办法，奈何关于iframe定位方式，网上的资料太少
        #实际上由一种更为简洁的解决方式，就是使用其自带的codegen记录然后参照写出处理方式
        
        #具体而言代码如下：
        # browser = playwright.chromium.launch(headless=False)
        # context = browser.new_context()
        # page = context.new_page()
        # page.goto("https://juejin.cn/")
        # page.get_by_role("button", name="登录 注册").click()
        # page.get_by_text("密码登录").click()
        # page.get_by_placeholder("请输入邮箱/手机号（国际号码加区号）").click()
        # page.get_by_placeholder("请输入邮箱/手机号（国际号码加区号）").fill("13394208751")
        # page.get_by_placeholder("请输入密码").click()
        # page.get_by_placeholder("请输入密码").fill("Lxy252799")
        # page.get_by_role("button", name="登录", exact=True).click()
        # page.frame_locator("iframe").locator(".captcha-slider-btn").click()
        # page.frame_locator("iframe").locator(".captcha-slider-btn").click()
        # page.frame_locator("iframe").get_by_role("img", name="basicImg").click()
        # page.frame_locator("iframe").get_by_role("img", name="actionImg").click()

        # # ---------------------
        # context.close()
        # browser.close()
        #======================================================================================
        # 原本的思路：
        # iframe = page.frame_locator('//iframe[contains(@src,"https://rmc.bytedance.com")]')
        # print(iframe) 
        #     # 滑动按钮
        # page.frame_locator('div.dragger-item')
        # print(page)
        #====================================================================================== 
        page.wait_for_timeout(3000)  
        #================================================================================================
        #这个地方一定要等待，不然iframe在没有加载出来之前就进行读取会无法读到，这个问题很隐蔽，但是一定要注意
        #很多地方出现问题的根源都是这个，时间太短没有加载到位，因此而产生的问题都可以使用wait_for_timeout来解决
        #================================================================================================
        login_flag = False  
        count = 2  
        while not login_flag and count>0:  
            basicimg=page.frame_locator("iframe").get_by_role("img", name="basicImg")
            actionimg=page.frame_locator("iframe").get_by_role("img", name="actionImg")
            
            #======================================================================================
            # 获取滑块背景图和滑块图片加载路径                                                      
            #======================================================================================
            #实际上由一种更为简洁的解决方式,就是使用其自带的codegen记录然后参照写出处理方式            
            #不好意思,没忍住，又说了一遍,因为这个方法太简便了,简直是专业对口                          
            #======================================================================================
            #print("basicimg src:",basicimg.get_attribute("src"))                                 
            #print("actionimg src:",actionimg.get_attribute("src"))|
            #======================================================================================
            
            UrlAndDst=[('./resources/basic.jpeg',basicimg.get_attribute("src")),
           ('./resources/action.png',actionimg.get_attribute("src"))]

            print("当前验证码背景图片网页地址：",basicimg.get_attribute("src"))
            print("当前验证码移动滑块网页地址：",actionimg.get_attribute("src"))
            
            BasicWidth,BasicHeight,ActionWidth,ActionHeight=RequestforImages.GetImages(UrlAndDst)
            X=CVPassComfirm.GetXtoMove("./resources/basic.jpeg","./resources/action.png",BasicHeight,BasicWidth,ActionHeight,ActionWidth)
            
            #X=X+ActionWidth/2
            #这里是不需要进行修正的，如果修正会多出一部分
            print("x: ",X)
        
            #Button = page.frame_locator("iframe").locator(".captcha-slider-btn")
            #Button.click()
            DraggerBox = page.frame_locator("iframe").locator(".captcha-slider-box > .dragger-box").bounding_box()
            
            StartX=DraggerBox["x"]
            StartY=DraggerBox["y"]
            print("StartX: ",StartX)
            print("StartY: ",StartY)
            
            
            #===============================================================================================
            #test for click测试一下button获取的位置是否正确
            #page.frame_locator("iframe").locator(".captcha-slider-btn").click()
            page.frame_locator("iframe").locator(".captcha-slider-btn").hover()
            page.mouse.down()
            # 移动鼠标  
            # 生成30次移动x轴的坐标  
            start = 1  
            end = X  
            step = (end - start) / 10 # 计算递增步长  
            for i in range(10):  
                if i == 9:  
                    number = X  
                else:  
                    number = start + i * step  
                page.mouse.move(DraggerBox["x"] + number, DraggerBox["y"] + random.randint(-10, 10), steps=4)  
            #page.mouse.move(DraggerBox["x"] + X, DraggerBox["y"] + random.randint(-10, 10), steps=6)  
            
            page.mouse.up()  
     
            # page.wait_for_timeout(2000)  
            try:  
                page.frame_locator("iframe").locator("a").filter(has_text="刷新").wait_for(timeout=1000)  
                count = count - 1  
            except Exception as e:  
                print("登录成功")  
                login_flag = True 
            #注意，下面这种写法的行为是不对的：
            #Button = page.frame_locator("iframe").locator(".captcha-slider-btn")
            #Button.click()
        page.wait_for_timeout(30000)
            #================================================================================================
            #这个地方也一定要等待，不然iframe在没有加载出来之前就进行读取会无法读到，这个问题很隐蔽，但是一定要注意
            #很多地方出现问题的根源都是这个，时间太短没有加载到位，因此而产生的问题都可以使用wait_for_timeout来解决
            #================================================================================================
            
            
            # resp_basicimg=requests.get(url=basicimg.get_attribute("src"))
            # with open('./resources/basicimg.png','wb') as f:
            #     f.write(resp_basicimg.content)
            
            # resp_actionimg=requests.get(url=actionimg.get_attribute("src"))
            # with open('./resources/actionimg.png','wb') as f:
            #     f.write(resp_actionimg.content)
            # page.frame_locator("iframe").locator(".captcha-slider-btn").click()
            
            # 计算滑块位置
            # 这里需要使用到cv2库，cv2库是opencv的python版本，需要先安装
            
if __name__ == "__main__":
    LogInWebsite()