import requests
url = 'https://p6-catpcha.byteimg.com/tos-cn-i-188rlo5p4y/27f052252dfb430caffcc8d1d5cb3d8a~tplv-188rlo5p4y-2.jpeg'
res = requests.get(url)
with open('test.jpg', 'wb') as f:
    f.write(res.content)
