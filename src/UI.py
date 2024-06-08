
import tkinter as tk
from tkinter import messagebox, PhotoImage
from tkinter import ttk, messagebox
from playwright.sync_api import sync_playwright

import CatchAndAnalyze
from PIL import Image, ImageTk# 创建PhotoImage对象
# 创建PhotoImage对象
def perform_analysis():
    url = url_entry.get()
    keyword = keyword_entry.get()

    if not url or not keyword:
        messagebox.showerror("Error", "Please enter both URL and keyword.")
        return
    
    url=url
    URLlist=[]
    
    search_word=keyword
    with sync_playwright() as p:
        result_urls= CatchAndAnalyze.run(p, url, search_word)
        URLlist=result_urls
    
    total = len(URLlist) # 事件的总数
    for i,url_i in enumerate(URLlist):
        # 处理当前事件
        print("\n\n=============================================")
        print("开始执行第{i}个页面的分析:".format(i=i))
        result = CatchAndAnalyze.CatshAndAnalyze(url_i, keyword)
        print("=============================================")
        # 更新进度条的值，并显示百分比
        progress.step(100 / total)
        percent.set('{:.0f}%'.format(progress['value']))
        root.update_idletasks() # 立即更新界面
        # 等待 50 毫秒，以便用户能看到进度条的变化
        root.after(50)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)


#========================================================================================================
#==========================================这里遇到的问题=================================================
# # 设置背景图片
# 图片文件的路径不正确。请确保../resources/bg.jpg是图片文件的正确路径，并且这个路径是相对于当前Python脚本的路径。
# 如果图片文件在Python脚本的同一目录下，您只需要提供文件名，例如bg.jpg。
# 图片文件的格式不被Tkinter支持。Tkinter的PhotoImage类只支持GIF和PPM/PGM格式的图片。如果您的图片是JPEG或PNG格式，
# 您需要使用PIL库的ImageTk.PhotoImage类来打开它。
#========================================================================================================
root = tk.Tk()
root.geometry("450x287")
# 打开图片文件
image = Image.open("../resources/bg.png")
# image.show()
# 创建PhotoImage对象
bg_image = ImageTk.PhotoImage(image)
# 使用PhotoImage对象作为背景
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# 创建其他小部件
tk.Label(root, text="URL:", font=("Arial", 14)).place(x=0, y=0)
url_entry = tk.Entry(root, font=("Arial", 14))
url_entry.place(x=0,y=23)

#=======================================================================================================
#==========================================这里遇到的问题================================================
# _tkinter.TclError: image "../resources/1.gif" doesn't exist
#=======================================================================================================
# 这个错误可能是由于Tkinter无法找到指定的图片文件导致的。在这种情况下，您需要确保X://DOCS//CODES//CRAWLER
# //douyin-comments-analizer//resources//1.gif是图片文件的正确路径。
# 如果路径是正确的，那么问题可能在于如何使用Label类的image参数。image参数需要一个PhotoImage或BitmapImage对象，
# 而不是一个文件路径。您需要首先创建一个PhotoImage对象，然后将其传递给image参数
#=======================================================================================================
# image1 = tk.PhotoImage(file="X://DOCS//CODES//CRAWLER//douyin-comments-analizer//resources//1.gif")
# tk.Label(root, text="Keyword:", image=image1, font=("Arial", 14)).pack()
tk.Label(root, text="Keyword:", font=("Arial", 14)).place(x=0, y=60)
keyword_entry = tk.Entry(root, font=("Arial", 14))
keyword_entry.place(x=0,y=83)

tk.Label(root, text="©copyright@2152505 Luan Xueyu", font=("Arial", 7)).place(x=160, y=270)

# 设置按钮
style = ttk.Style()
style.configure('TButton', font=("Arial", 14), borderwidth='4')
style.map('TButton', foreground=[('pressed', 'black'), ('active', 'blue')],
           background=[('pressed', '!disabled', 'black'), ('active', 'lightgreen')])



# 创建一个 Label 对象，用于显示进度百分比
percent = tk.StringVar()
percent_label = tk.Label(root, textvariable=percent, bg='white', font=('Arial', 10))

# 创建一个 ttk.Progressbar 对象，用于显示进度条
progress = ttk.Progressbar(root, mode='determinate', orient='horizontal', length=200)
progress.pack()
# 创建处理事件的函数
# 显示进度条和百分比，并启动处理事件的函数
progress['value'] = 0
percent.set('0%')
root.update_idletasks() # 立即更新界面

analyze_button = ttk.Button(root, text="Analyze", command=perform_analysis, style='TButton')
analyze_button.place(x=0,y=110)
# 打开图片文件
image2 = Image.open("../resources/transparent.png")
# image.show()
# 创建PhotoImage对象
bg_trans_image = ImageTk.PhotoImage(image2)
# 在按钮和主循环之间添加以下代码
result_text = tk.Text(root, font=("Arial", 14))
# result_text.image_create('end', image=bg_trans_image)  # 使用透明的图片作为背景
# # result_text.pack()
# tk.Label(root, text="Keyword:", font=("Arial", 14)).pack(): 这行代码创建了一个标签小部件。
# root是这个标签的父窗口。text="Keyword:"设置了标签的文本为"Keyword:"。font=("Arial", 14)设置
# 了标签的字体为Arial，字号为14。pack()方法是一种布局管理器，它会自动调整小部件的大小和位置。
# keyword_entry = tk.Entry(root, font=("Arial", 14)): 这行代码创建了一个输入框小部件，并将它赋值给
# keyword_entry变量。root是这个输入框的父窗口。font=("Arial", 14)设置了输入框的字体为Arial，字号为14。
# keyword_entry.pack(): 这行代码使用pack()方法来管理输入框的布局。pack()方法会自动调整小部件的大小和位置。
root.mainloop()