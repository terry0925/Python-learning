from PIL import Image


code_lib = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def transform(image_file):
    image_file = image_file.convert("L")  # 转换为黑白图片 L 为参数
    str_content = ''
    # 通过双循环遍历所有的点，并且获得点的坐标 size【1】 表示纵方向，size【0】 表示横方向
    for i in range(0, image_file.size[1]):
        for j in range(0, image_file.size[0]):
            grey = image_file.getpixel((j, i))  # 取每个点的灰度
            str_content = str_content + code_lib[int((len(code_lib)*grey)/256)]  # 根据灰度比例映射字符串集
        str_content = str_content + '\n'  # 添加换行符
    return str_content




with open('IMG_4602.JPG', mode='rb') as f:
    image_file = Image.open(f)
    txt_pic = transform(image_file)

with open('str.txt', mode='w') as fp:
    fp.write(txt_pic)


