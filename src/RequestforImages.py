# from fake_useragent import UserAgent
import cv2
import requests
import time
import itertools
from multiprocessing import Pool
#ua=UserAgent()                     
#实例化 
#print(ua.chrome)
#获取谷歌浏览器的headers，每次打印结果是不一样的
#请求头就可以写成,毕竟是自己电脑，改为装还是要伪装一下的，ip被封了就麻烦了
#headers={"User-Agent":ua.random} 
UrlAndDst=[('./resources/basic.jpeg',"https://p6-catpcha.byteimg.com/tos-cn-i-188rlo5p4y/27f052252dfb430caffcc8d1d5cb3d8a~tplv-188rlo5p4y-2.jpeg"),
           ('./resources/action.png',"https://p6-catpcha.byteimg.com/tos-cn-i-188rlo5p4y/832163e6cef049b7ad14849d4d04526f~tplv-188rlo5p4y-1.png")]
#basic action

def DownLoadImages(dstPath,ImageURL):
    # response = requests.get(ImageURL,headers=headers)
    response = requests.get(ImageURL)
    #请求网站
    content = response.content
    with open(dstPath,'wb') as f:
            f.write(content)
        

    
def GetImages(UrlAndDst):      
    if UrlAndDst != "":  
        pool=Pool(2)
        pool.starmap(DownLoadImages,UrlAndDst)
        print("图片下载完成")
    else:
        print("图片地址为空")
    
    
    # 读取图像
    BasicImage = cv2.imread('./resources/basic.jpeg')
    ActionImage = cv2.imread('./resources/action.png')

    # 获取图像尺寸
    BasicHeight, BasicWidth, channels = BasicImage.shape
    ActionHeight, ActionWidth, channels = ActionImage.shape
    # 打印图像尺寸
    print("背景图像的宽度：", BasicWidth)
    print("背景图像的高度：", BasicHeight)
    print("行动图像的宽度：", ActionWidth)
    print("行动图像的高度：", ActionHeight)
    
    return BasicWidth,BasicHeight,ActionWidth,ActionHeight
        
        
#============================================================================================================================
#测试用例：
#============================================================================================================================
# 其实用request方式应该是最快的，但是这个网址下载就是很慢，不知道为什么
# 因此这里使用了多线程进行下载，可以提高20s左右，没错，访问这个网址需要25s左右

# 在实习地点的网速很快，此图片的下载只需要不到5s，有时候还不到3s，有趣有趣
if __name__ == "__main__":
    GetImages(UrlAndDst)
#============================================================================================================================


#====================================================================================================================
#遇到这类报错无论是在git还是编写代码，不用怀疑，就是代理的问题，开了代理就会有网络的问题
#====================================================================================================================
# urllib3.exceptions.SSLError: TLS/SSL connection has been closed (EOF) (_ssl.c:1135)
# The above exception was the direct cause of the following exception:
# urllib3.exceptions.ProxyError: ('Unable to connect to proxy', SSLError(SSLZeroReturnError(6, 'TLS/SSL connection 
# has been closed (EOF) (_ssl.c:1135)')))
# The above exception was the direct cause of the following exception:
# Traceback (most recent call last):
#   File "D:\SoftWare\VSCode\Anaconda3\envs\Web\lib\site-packages\requests\adapters.py", line 486, in send
#     resp = conn.urlopen(
#   File "D:\SoftWare\VSCode\Anaconda3\envs\Web\lib\site-packages\urllib3\connectionpool.py", line 847, in urlopen
#     retries = retries.increment(
#   File "D:\SoftWare\VSCode\Anaconda3\envs\Web\lib\site-packages\urllib3\util\retry.py", line 515, in increment
#     raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
# urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='p6-catpcha.byteimg.com', port=443): Max retries exceeded
# with url: /tos-cn-i-188rlo5p4y/27f052252dfb430caffcc8d1d5cb3d8a~tplv-188rlo5p4y-2.jpeg (Caused by ProxyError('Unable 
# to connect to proxy', SSLError(SSLZeroReturnError(6, 'TLS/SSL connection has been closed (EOF) (_ssl.c:1135)'))))
#=====================================================================================================================