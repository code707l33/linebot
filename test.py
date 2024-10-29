import random


def generate_light_hex_color():
    # 每個顏色通道（R, G, B）設定在 128 到 255 的範圍內，確保顏色偏淺
    r = random.randint(128, 255)
    g = random.randint(128, 255)
    b = random.randint(128, 255)
    # 將 RGB 值轉換成 16 進制格式
    return f"#{r:02x}{g:02x}{b:02x}"


# 測試產生隨機淺色顏色
print(generate_light_hex_color())
