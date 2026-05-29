import tkinter as tk
from ..setting.setting import AppConfig
from ..speaker.speaker import Speaker
from ..core.__main__ import main as main_ocr_loop

class APP(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.sp = Speaker()
        self.config_manager = AppConfig()
        
        # 1. 启动默认全屏
        self.attributes("-fullscreen", True)
        
        # 绑定 ESC 键退出程序（强烈建议保留，防止全屏后无法退出）
        self.bind("<Escape>", lambda event: self.destroy())

        # 2. 配置网格布局，使 2x3 的网格均匀填满整个窗口
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # 3. 设置超大字体与统一样式
        huge_font = ("SimHei", 160, "bold") 
        
        # 使用字典统一定义按钮样式，方便维护
        btn_style = {
            "font": huge_font,
            "bg": "#E0E0E0",               # 常态背景颜色 (浅灰色)
            "activebackground": "#000000", # 按下时的背景颜色 (亮蓝色，体现按下效果)
            "fg": "#333333",               # 常态文字颜色
            "activeforeground": "#FFFFFF"  # 按下时的文字颜色
        }

        # 4. 创建并放置六个按钮
        # 增加了 padx 和 pady 留下按钮间隙，让按下时的颜色变化更加分明
        
        # 左上角：语速+
        self.btn_speed_add = tk.Button(self, text="语速+", command=self.on_speed_add, **btn_style)
        self.btn_speed_add.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # 中上角：音量+
        self.btn_vol_add = tk.Button(self, text="音量+", command=self.on_volume_add, **btn_style)
        self.btn_vol_add.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # 右上角：开始
        self.btn_start = tk.Button(self, text="开始", command=self.on_start, **btn_style)
        self.btn_start.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # 左下角：语速-
        self.btn_speed_sub = tk.Button(self, text="语速-", command=self.on_speed_sub, **btn_style)
        self.btn_speed_sub.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # 中下角：音量-
        self.btn_vol_sub = tk.Button(self, text="音量-", command=self.on_volume_sub, **btn_style)
        self.btn_vol_sub.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # 右下角：退出 (直接调用自带的 self.destroy 方法关闭窗口)
        self.btn_exit = tk.Button(self, text="重置", command=self.on_reset, **btn_style)
        self.btn_exit.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        self.sp.add_sentence(f"当前参数（音量{self.config_manager.volume},速度{self.config_manager.speed}）")
        self.sp.add_sentence("注意，更改后的语速在重新启动后生效，设置过程中读出的语音提示并没有反映实时设置的语速")

    # --- 按钮对应的功能回调函数 ---
    
    def on_speed_add(self):
        self.config_manager.speed += 5
        self.sp.add_sentence(f"设置语速: {self.config_manager.speed}")

    def on_speed_sub(self):
        self.config_manager.speed -= 5
        self.sp.add_sentence(f"设置语速: {self.config_manager.speed}")

    def on_volume_add(self):
        self.config_manager.volume += 5
        self.sp.add_sentence(f"设置音量: {self.config_manager.volume}")

    def on_volume_sub(self):
        self.config_manager.volume -= 5
        self.sp.add_sentence(f"设置音量: {self.config_manager.volume}")

    def on_start(self):
        # 此处可以替换为实际的启动逻辑
        self.sp.add_sentence("5秒钟后开始")
        self.destroy()
        
    def on_reset(self):
        self.config_manager.volume = 100
        self.config_manager.speed = 200
        self.sp.add_sentence(f"参数重设（音量{self.config_manager.volume},速度{self.config_manager.speed}）")
        
    


if __name__ == "__main__":
    app = APP()
    app.mainloop()
    main_ocr_loop()