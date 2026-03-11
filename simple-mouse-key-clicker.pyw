import tkinter as tk
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import threading
import time

class AutoClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("连点器")
        self.root.geometry("320x420")
        
        # 变量初始化
        self.is_running = False
        self.interval_ms = tk.IntVar(value=100)  # 默认100毫秒
        self.use_left_click = tk.BooleanVar(value=True)
        self.use_middle_click = tk.BooleanVar(value=False)
        self.use_right_click = tk.BooleanVar(value=False)
        self.key_to_press = tk.StringVar(value="")
        self.mode = tk.StringVar(value="hold")  # "hold" for F6, "toggle" for F7
        
        self.mouse_controller = Controller()
        self.setup_ui()
        
        # 监听快捷键
        self.keyboard_listener = None
        self.hold_pressed = False  # 用于跟踪F6是否被按住
        
    def setup_ui(self):
        # 间隔设置
        tk.Label(self.root, text="点击间隔(毫秒):").pack(pady=5)
        interval_frame = tk.Frame(self.root)
        interval_frame.pack(pady=5)
        tk.Entry(interval_frame, textvariable=self.interval_ms, width=10).pack(side=tk.LEFT)
        tk.Label(interval_frame, text="ms").pack(side=tk.LEFT)
        
        # 鼠标按钮选择
        tk.Label(self.root, text="鼠标按键:").pack(pady=5)
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        
        tk.Checkbutton(button_frame, text="左键", variable=self.use_left_click).pack(side=tk.LEFT)
        tk.Checkbutton(button_frame, text="中键", variable=self.use_middle_click).pack(side=tk.LEFT)
        tk.Checkbutton(button_frame, text="右键", variable=self.use_right_click).pack(side=tk.LEFT)
        
        # 键盘按键设置
        tk.Label(self.root, text="键盘按键(留空则不按):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.key_to_press).pack(pady=5)
        
        # 模式选择
        tk.Label(self.root, text="工作模式:").pack(pady=5)
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=5)
        
        tk.Radiobutton(mode_frame, text="F6按住启用", variable=self.mode, value="hold").pack(anchor=tk.W)
        tk.Radiobutton(mode_frame, text="F7切换启用", variable=self.mode, value="toggle").pack(anchor=tk.W)
        
        # 控制按钮
        self.status_label = tk.Label(self.root, text="状态: 停止", fg="red")
        self.status_label.pack(pady=10)
        
        self.start_button = tk.Button(self.root, text="启动", command=self.start_clicking)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(self.root, text="停止", command=self.stop_clicking, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        # 信息显示
        self.info_text = tk.Text(self.root, height=9, width=40)
        self.info_text.pack(pady=10)
        self.update_info()
        
        # 启动键盘监听
        self.start_keyboard_listener()
    
    def update_info(self):
        self.info_text.delete(1.0, tk.END)
        info = f"""当前设置:
间隔: {self.interval_ms.get()} 毫秒 ({self.interval_ms.get()/1000.0:.3f} 秒)
鼠标按键: {"左" if self.use_left_click.get() else ""}{"中" if self.use_middle_click.get() else ""}{"右" if self.use_right_click.get() else ""}
键盘按键: {self.key_to_press.get() or "无"}
工作模式: {"F6按住启用" if self.mode.get()=="hold" else "F7切换启用"}
状态: {"运行中" if self.is_running else "停止"}"""
        self.info_text.insert(tk.END, info)
    
    def start_clicking(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="状态: 运行中", fg="green")
            self.update_info()
    
    def stop_clicking(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="状态: 停止", fg="red")
            self.update_info()
    
    def start_keyboard_listener(self):
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.keyboard_listener.start()
    
    def on_key_press(self, key):
        try:
            if key == keyboard.Key.f6 and self.mode.get() == "hold":
                self.hold_pressed = True
                self.start_clicking()
            elif key == keyboard.Key.f7 and self.mode.get() == "toggle":
                if self.is_running:
                    self.stop_clicking()
                else:
                    self.start_clicking()
        except Exception:
            pass
    
    def on_key_release(self, key):
        try:
            if key == keyboard.Key.f6 and self.mode.get() == "hold":
                self.hold_pressed = False
                self.stop_clicking()
        except Exception:
            pass
    
    def run(self):
        # 启动自动点击线程
        click_thread = threading.Thread(target=self.run_auto_clicker, daemon=True)
        click_thread.start()
        self.root.mainloop()
    
    def run_auto_clicker(self):
        while True:
            if self.is_running:
                # 执行点击操作
                # 执行鼠标点击
                if self.use_left_click.get():
                    self.mouse_controller.click(Button.left, 1)
                if self.use_middle_click.get():
                    self.mouse_controller.click(Button.middle, 1)
                if self.use_right_click.get():
                    self.mouse_controller.click(Button.right, 1)
                
                # 执行键盘按键
                if self.key_to_press.get():
                    keyboard.Controller().press(self.key_to_press.get())
                    keyboard.Controller().release(self.key_to_press.get())
                
                # 转换毫秒到秒
                time.sleep(self.interval_ms.get() / 1000.0)
            else:
                time.sleep(0.01)  # 减少CPU占用

if __name__ == "__main__":
    app = AutoClicker()
    app.run()
