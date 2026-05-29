import json
import threading
from pathlib import Path
# 如果尚未安装，可以运行: pip install platformdirs
from platformdirs import user_data_dir

class AppConfig:
    _instance = None
    _lock = threading.Lock()  # 确保线程安全的单例模式

    def __new__(cls, *args, **kwargs):
        """单例模式：确保全局只有一个配置实例"""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    # 标记是否已经初始化，防止 __init__ 重复调用
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, app_name="ScreenSubtitleReader"):
        if self._initialized:
            return
        
        # 1. 确定跨平台的 AppData 存储路径
        # 在 Windows 上通常是: C:\Users\用户名\AppData\Local\MyTkinterApp
        self.config_dir = Path(user_data_dir(app_name))
        self.config_file = self.config_dir / "config.json"
        
        # 2. 默认属性
        self._volume = 100
        self._speed = 270
        
        # 3. 启动初始化：自动读取或创建文件
        self._load_or_create_config()
        self._initialized = True

    def _load_or_create_config(self):
        """读取配置文件，如果不存在则创建默认配置"""
        try:
            if self.config_file.exists():
                # 文件存在，读取数据
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 使用 get 提供降级容错，防止 JSON 被人为改坏导致崩溃
                    self._volume = int(data.get("volume", 100))
                    self._speed = int(data.get("speed", 270))
                print(f"成功加载配置: {self.config_file}")
            else:
                # 文件不存在，保存当前的默认值
                self.save()
                print(f"创建默认配置文件: {self.config_file}")
        except Exception as e:
            print(f"配置加载或初始化失败，使用默认值。错误: {e}")

    def save(self):
        """将当前属性序列化并自动存盘"""
        try:
            # 确保应用数据文件夹存在（不存在则自动递归创建）
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            data = {
                "volume": self._volume,
                "speed": self._speed
            }
            # 写入文件
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("配置已自动保存到磁盘。")
        except Exception as e:
            print(f"配置保存失败: {e}")

    # --- 使用 Property 属性装饰器，既能像属性一样访问，又能触发自动存盘 ---
    @property
    def volume(self) -> int:
        return self._volume

    @volume.setter
    def volume(self, value: int):
        if not isinstance(value, int):
            raise TypeError("音量必须是整型 (int)")
        self._volume = value
        self.save()  # 更改时自动存盘

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value: int):
        if not isinstance(value, int):
            raise TypeError("语速必须是整型 (int)")
        self._speed = value
        self.save()  # 更改时自动存盘
        
if __name__ == "__main__":
    apc = AppConfig()
    print(apc.speed)