from .ocr_fither import OCR 
from .speaker import Speaker
from PIL import ImageGrab

def main():
    ocr = OCR()
    sp = Speaker()
    text,textLast = '初始化',None
    while True:
        im = ImageGrab.grab()
        ocr_result = ocr.OCR_image(im)
        if ocr_result:
            text = ocr_result.text
        if text != textLast:
            sp.add_sentence(text)
            textLast = text

if __name__ =="__main__":
    main()