from wrap import WrapSession

session = WrapSession()

lines = session.process("HTML5的canvas元素使用JavaScript在网页上“绘制”图像，画布是一个矩形区域!")

for line in lines:
    print("|".join(line))
