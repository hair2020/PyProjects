import sys
from PIL import Image, ImageDraw, ImageFont
import win32ui
def fill_words(filein, fileout, txt, font):
    # imgSrc = Image.open(sys.argv[1])                        # 打开源图像
    imgSrc = Image.open(filein)
    w, h = imgSrc.size  # 源图像宽和高

    CHILD_W = CHILD_H = 16  # 子图的尺寸，宽和高都是16像素

    imgChild = Image.new("RGB", (CHILD_W, CHILD_H))  # 新建子图

    imgDst = Image.new("RGB", (CHILD_W * w, CHILD_H * h))  # 创建目标图像的空图，待填充

    textW, textH = font.getsize("迷")  # 取得单个文字的宽、高信息
    offsetX = (CHILD_W - textW) >> 1  # 文字水平居中绘制
    offsetY = (CHILD_H - textH) >> 1  # 文字垂直居中绘制

    charIndex = 0  # 序号，代表当前绘制哪个汉字
    draw = ImageDraw.Draw(imgChild)  # 取得小图的绘图对象，用于绘制文字
    for y in range(h):
        for x in range(w):
            draw.rectangle((0, 0, CHILD_W, CHILD_H), fill='lightgray')  # 灰色背景效果比外色略好

            draw.text((offsetX, offsetY), txt[charIndex], font=font, fill=imgSrc.getpixel((x, y)))

            imgDst.paste(imgChild, (x * CHILD_W, y * CHILD_H))  # 把绘制好的子图填到imgDst里

            charIndex += 1  # 序号加1，从而依次绘制每个字
            if charIndex == len(txt):  # 循环绘制
                charIndex = 0

    imgDst.save(fileout)  # 保存图片

# 修改图片尺寸
def ResizeImage(filein, fileout, width, height, type):
  img = Image.open(filein)
  out = img.resize((width, height),Image.ANTIALIAS)
  #resize image with high-quality
  out.save(fileout, type)

# win手动选择文件
def get_file(ori_dir):
    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    dlg.SetOFNInitialDir(ori_dir)  # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename = dlg.GetPathName()  # 获取选择的文件名称
    # print(filename)
    return filename

def only_one():
    ResizeImage('', '', 480, 480, 'jpg')

    txt = 'some words'  # 输出内容
    font = ImageFont.truetype('AliPuHui-Bold.ttf', 16)  # 字体及大小,选用粗体字体效果更好

    fill_words('', '', txt, font)
# 程序入口
if __name__ == '__main__':
    get_file('.')








