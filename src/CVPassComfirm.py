import random  
import time  
  
from playwright.sync_api import sync_playwright  
import cv2  
import requests  
import ddddocr
import cv2

#====================================================================================
#这个函数是用来获取滑块的移动距离的，这个函数是通过opencv来实现的
#此处有一个问题，就是有些时候使用opencv进行识别的时候会由于验证码的迷惑度比较高而导致验证失败
#====================================================================================


def GetXtoMove(image_path, template_path, image_height, image_width, template_height, template_width):  
    # 背景图  
    image = cv2.imread(image_path)  
    image_resize = cv2.resize(image, (image_width, image_height))  
    # 处理图像，保留大部分白色  
    ret, thresholded_image = cv2.threshold(image_resize, 220, 255, cv2.THRESH_BINARY)  
    
    # 灰度图像  
    gray_image1 = cv2.cvtColor(thresholded_image, cv2.COLOR_BGR2GRAY)  
    cv2.imshow("MethodCV: gray_image1",gray_image1)
    cv2.waitKey(0)
    
    # # 提高对比度  
    denoised_image1 = cv2.equalizeHist(gray_image1)  
    # 边缘检测  
    image_canny = cv2.Canny(denoised_image1, threshold1=500, threshold2=900)  
    cv2.imshow("MethodCV: image_canny",image_canny)
    cv2.waitKey(0)
    #===============================================================
    #在调试的时候一定要注意，如果不加waitkey(0)的话，会导致窗口一闪而过，看不到效果
    #===============================================================
    # 滑动图  
    template = cv2.imread(template_path)  
    template_resize = cv2.resize(template, (template_width, template_height))  
    template_gray = cv2.cvtColor(template_resize, cv2.COLOR_BGR2GRAY)  
    denoised_image2 = cv2.equalizeHist(template_gray)  
    template_canny = cv2.Canny(denoised_image2, threshold1=650, threshold2=900)  
    cv2.imshow("MethodCV: template_canny",template_canny)
    cv2.waitKey(0)
    
    
    # # 进行模板匹配  
    # MatchTemplate(InputArray image, InputArray templ, OutputArray result, int method);

    # image：输入一个待匹配的图像，支持8U或者32F。

    # templ：输入一个模板图像，与image相同类型。

    # result：输出保存结果的矩阵，32F类型。

    # method：要使用的数据比较方法。
    result = cv2.matchTemplate(image_canny, template_canny, cv2.TM_CCOEFF_NORMED)  
  
    # 获取匹配结果的位置  
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)  
  
    top_left2 = max_loc  
    bottom_right2 = (top_left2[0] + template_resize.shape[1], top_left2[1] + template_resize.shape[0])  
    # 在输入图像上绘制矩形标记  
    cv2.rectangle(image_resize, top_left2, bottom_right2, (0, 0, 255), 2)  
    cv2.imwrite('./result/'+str(int(time.time()))+'.jpg', image_resize)  
    # x位置  
    return max_loc[0]  

    #====================================================================================
    #这种办法的精准度太低，使用ddddocr进行识别
    #====================================================================================

    # det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)

    # with open(template_path, 'rb') as f:
    #     target_bytes = f.read()

    # with open(image_path, 'rb') as f:
    #     background_bytes = f.read()

    # res = det.slide_match(target_bytes, background_bytes, simple_target=True)
    # return res['target'][0]


if __name__ == '__main__':
    print(GetXtoMove("../resources/basic.jpeg", "../resources/action.png", 344, 552, 110, 110))

#=====================================================================
#注意一个报错，这个报错和函数本身无关，问题是图片路径有问题，没读取到图片
#所以报错，不要被迷惑了
#=====================================================================
# [ WARN:0@0.102] global loadsave.cpp:248 cv::findDecoder imread_('./resource/2.png'): can't open/read file: check file path/integrity
# Traceback (most recent call last):
#   File ".\CVPassComfirm.py", line 45, in <module>
#     GetXtoMove("./resource/2.png", "./resource/1.png", 212, 340, 68, 68)
#   File ".\CVPassComfirm.py", line 14, in GetXtoMove
#     image_resize = cv2.resize(image, (image_width, image_height))
# cv2.error: OpenCV(4.9.0) D:\a\opencv-python\opencv-python\opencv\modules\imgproc\src\resize.cpp:4152: error: (-215:Assertion failed) !ssize.empty() in function 'cv::resize'



#=====================================================================
#下面的代码是测试部分，单独运行可以观察opencv识别出的结果和效果
#=====================================================================
# image1 = cv2.imread("./resources/2.png")
# image1_resize = cv2.resize(image1, (340, 212))
# image2 = cv2.imread("./resources/1.png")
# image2_resize = cv2.resize(image2, (68, 68))
# # image1_resize = cv2.imread("./resources/2.png")
# # image2_resize = cv2.imread("./resources/1.png")
 
# # 背景图
# # 处理图像，保留大部分白色
# ret, thresholded_image = cv2.threshold(image1_resize, 220, 255, cv2.THRESH_BINARY)
# # 灰度图像
# gray_image1 = cv2.cvtColor(thresholded_image, cv2.COLOR_BGR2GRAY)
# # 提高对比度
# denoised_image1 = cv2.equalizeHist(gray_image1)
# # 边缘检测
# edges = cv2.Canny(denoised_image1, threshold1=500, threshold2=900)
 
# # 滑块图片
# gray_image2 = cv2.cvtColor(image2_resize, cv2.COLOR_BGR2GRAY)
# denoised_image2 = cv2.equalizeHist(gray_image2)
# edges2 = cv2.Canny(denoised_image2, threshold1=650, threshold2=900)
 
# # 进行形状匹配
# result = cv2.matchTemplate(edges, edges2, cv2.TM_CCOEFF_NORMED)
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
# top_left2 = max_loc
# bottom_right2 = (top_left2[0] + edges2.shape[1], top_left2[1] + edges2.shape[0])
 
# # 在输入图像上绘制矩形标记
# cv2.rectangle(image1_resize, top_left2, bottom_right2, (0, 0, 255), 2)
 
# cv2.imshow("denoised_image2", denoised_image2)
# cv2.imshow("edges2", edges2)
# cv2.imshow("denoised_image1", denoised_image1)
# cv2.imshow("edges", edges)
# cv2.imshow('Target Image', image1_resize)
 
 
# cv2.waitKey(0)