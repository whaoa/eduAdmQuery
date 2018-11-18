from PIL import Image
import io
# import requests
import pytesseract

def getVCode(imgdata):
    # imgdata = requests.get('http://202.207.247.44:8089/validateCodeAction.do?random=0.6170589789777645')

    # 通过 io 模块实现模拟文件读取操作，让Image.open读取爬取的图片数据
    image = Image.open(io.BytesIO(imgdata))

    # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    img = image.convert('L')
    vcode = pytesseract.image_to_string(img, lang='eng', config='--psm 7 ')
    vcode = ''.join(list(filter(str.isalnum, vcode)))
    return vcode