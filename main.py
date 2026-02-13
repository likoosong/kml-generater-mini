import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from settings.constant import UPLOAD_PATH
from view.line_tour_interface import LineTourView


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KML线路浏览生成器 v0.0.1")
        self.root.iconbitmap("img/likoosong.ico")
        self.root.geometry("400x600")
        self.root.configure(bg='#f0f0f0')
        
        # 创建主框架
        self.main_frame = tk.Frame(root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标题
        self.title_label = tk.Label(
            self.main_frame, 
            text="线路浏览", 
            font=('Microsoft YaHei', 16, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.title_label.pack(pady=(0, 10))
        
        # 创建线路浏览界面
        self.line_tour_view = LineTourView(self.main_frame)
        self.line_tour_view.pack(fill=tk.BOTH, expand=True)
    
    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = MainApp(root)
    app.run()


if __name__ == '__main__':
    main()
