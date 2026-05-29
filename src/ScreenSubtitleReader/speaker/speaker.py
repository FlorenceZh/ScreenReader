import pyttsx3
import queue
import time
import threading
from ..setting.setting import AppConfig

class Speaker:
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
    
    def __init__(self,volum = None ,speed = None) -> None:
        if self._initialized:
            return
        
        config_manager = AppConfig()
        self.volum = volum if volum else config_manager.volume
        self.speed = speed if speed else config_manager.speed
        
        self.voice_tasks = queue.Queue()
        
        # 启动工作线程
        self.thread = threading.Thread(target=self.speak_text_block_thread, daemon=True)
        self.thread.start()
        
        self._initialized = True
        
    def add_sentence(self, sentence: str):
        self.voice_tasks.put(sentence)
    
    def speak_text_block_thread(self):
        # 【关键修改】在子线程内部初始化引擎
        engine = pyttsx3.init()
        engine.setProperty('rate',self.speed ) 
        
        while True:
            # queue.get() 默认是阻塞的，没有任务时会一直等在这里，不会消耗CPU
            speak_sentence = self.voice_tasks.get()
            
            if speak_sentence:
                engine.say(speak_sentence)
                engine.runAndWait()
            
            # 通知队列当前任务已处理完毕（良好的队列使用习惯）
            self.voice_tasks.task_done()
                
if __name__ == "__main__":
    sp = Speaker()
    for i in range(99):
        sp.add_sentence(f"阿巴阿巴阿巴 {i}")
        
    time.sleep(100)