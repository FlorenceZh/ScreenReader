from .ui.ui import APP
from .core.__main__ import main as main_ocr_loop

def main():
    app = APP()
    app.mainloop()
    main_ocr_loop()
    
if __name__ =="__main__":
    main()