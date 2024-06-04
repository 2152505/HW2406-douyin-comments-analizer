import ddddocr

det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)

with open('./resources/action.png', 'rb') as f:
    target_bytes = f.read()

with open('./resources/basic.jpeg', 'rb') as f:
    background_bytes = f.read()

res = det.slide_match(target_bytes, background_bytes, simple_target=True)
print(res)
