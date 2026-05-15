import fasttext

# 1. 加载下载好的模型文件 (请确保路径正确)
model = fasttext.load_model('lid.176.ftz')

def identify_language(text):
    # 去除换行符，因为 fasttext 默认按行处理
    text = text.replace('\n', ' ')
    
    # 2. 进行预测
    # k=1 表示只返回概率最高的一个结果
    # 如果想看前三个可能的语言，可以设置 k=3
    predictions = model.predict(text, k=1)
    
    # predictions 的格式为: (('__label__zh',), array([0.98]))
    language_code = predictions[0][0].replace('__label__', '')
    confidence = predictions[1][0]
    
    return language_code, confidence

# --- 测试 ---
samples = [
    "禁止入内1995从",
    "5、 这样我们就是友好绑定的犯罪者了",
    "乙0世界必载科香必了龙笑丽C"
]

for s in samples:
    lang, score = identify_language(s)
    print(f"文本: {s}")
    print(f"识别语种: {lang} | 置信度: {score:.4f}\n")