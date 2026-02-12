import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from settings.constant import UPLOAD_PATH
from utlis.my_thread import ThreadLine
from utlis.parser_line_coords import parser_line_coords, parser_line_distance


class LineTourView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#f0f0f0')
        self.filepath_coords = None
        self.filepath_length = None
        self.filepath_distance = None
        self.kmlname = None
        self.thread_line = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # 主容器框架
        main_container = tk.Frame(self, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 文件名输入
        name_frame = tk.Frame(main_container, bg='#f0f0f0')
        name_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            name_frame, 
            text="KML文件名:",
            font=('Microsoft YaHei', 11),
            bg='#f0f0f0',
            width=15,
            anchor='e'
        ).pack(side=tk.LEFT, padx=5)
        
        self.kmlname_entry = tk.Entry(
            name_frame, 
            font=('Microsoft YaHei', 11),
            relief='solid',
            bd=1
        )
        self.kmlname_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.kmlname_entry.insert(0, "")
        
        # 浏览方式选择
        tour_frame = tk.Frame(main_container, bg='#f0f0f0')
        tour_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            tour_frame, 
            text="浏览方式:", 
            font=('Microsoft YaHei', 11),
            bg='#f0f0f0',
            width=15,
            anchor='e'
        ).pack(side=tk.LEFT, padx=5)
        
        self.tour_type_var = tk.StringVar(value="生长路线-固定视角")
        self.tour_type_combo = ttk.Combobox(
            tour_frame,
            textvariable=self.tour_type_var,
            values=["生长路线-固定视角", "生长路线-环绕视角", "生长路线-跟随视角"],
            font=('Microsoft YaHei', 11),
            state='readonly'
        )
        self.tour_type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 图片模型选择
        flag_frame = tk.Frame(main_container, bg='#f0f0f0')
        flag_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            flag_frame, 
            text="图片模型:", 
            font=('Microsoft YaHei', 11),
            bg='#f0f0f0',
            width=15,
            anchor='e'
        ).pack(side=tk.LEFT, padx=5)
        
        self.flag_var = tk.IntVar(value=1)  # 1=模型, 2=图片
        tk.Radiobutton(
            flag_frame,
            text="模型",
            variable=self.flag_var,
            value=1,
            font=('Microsoft YaHei', 11),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(
            flag_frame,
            text="图片",
            variable=self.flag_var,
            value=2,
            font=('Microsoft YaHei', 11),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT, padx=5)
        
        # 移动时间输入
        time_frame = tk.Frame(main_container, bg='#f0f0f0')
        time_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            time_frame, 
            text="移动时间:", 
            font=('Microsoft YaHei', 11),
            bg='#f0f0f0',
            width=15,
            anchor='e'
        ).pack(side=tk.LEFT, padx=5)
        
        self.tour_time_entry = tk.Entry(
            time_frame, 
            font=('Microsoft YaHei', 11),
            relief='solid',
            bd=1,
            width=10
        )
        self.tour_time_entry.pack(side=tk.LEFT, padx=5)
        self.tour_time_entry.insert(0, "30")
        
        tk.Label(
            time_frame, 
            text="秒", 
            font=('Microsoft YaHei', 11),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT)
        
        # 文件上传
        file_frame = tk.Frame(main_container, bg='#f0f0f0')
        file_frame.pack(fill=tk.X, pady=5)
        
        self.upload_btn = tk.Button(
            file_frame,
            text="选择文件",
            font=('Microsoft YaHei', 10),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.on_file_select
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
        self.file_label = tk.Label(
            file_frame,
            text="请选择上传的文件",
            font=('Microsoft YaHei', 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.file_label.pack(side=tk.LEFT, padx=10)
        
        # 确定按钮
        button_frame = tk.Frame(main_container, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=20)
        
        self.download_btn = tk.Button(
            button_frame,
            text="生成 KML",
            font=('Microsoft YaHei', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            relief='flat',
            cursor='hand2',
            width=15,
            height=1,
            command=self.on_generate
        )
        self.download_btn.pack(pady=10)
        
        # 状态标签
        self.status_label = tk.Label(
            main_container,
            text="",
            font=('Microsoft YaHei', 10),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.status_label.pack(pady=10)
    
    def on_file_select(self):
        """选择文件"""
        try:
            filename = filedialog.askopenfilename(
                title='选择坐标文件',
                initialdir=UPLOAD_PATH,
                filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("KML Files", "*.kml")]
            )
            if filename:
                show_file_name = os.path.basename(filename)
                self.file_label.config(text=show_file_name, fg='#333333')
                self.filepath_coords = parser_line_coords(filename)
                
                # 路线的坐标数量，路线的距离
                self.filepath_length, self.filepath_distance = parser_line_distance(self.filepath_coords)
                self.kmlname = show_file_name
                self.status_label.config(text=f"文件已加载: {show_file_name}", fg='#4CAF50')
        except Exception as e:
            messagebox.showerror("错误", f"上传文件不正确!\n{str(e)}")
            self.status_label.config(text="文件加载失败", fg='#f44336')
    
    def on_generate(self):
        """生成 KML 文件"""
        if self.filepath_coords is None:
            messagebox.showwarning("提示", "请先选择上传文件!")
            return
        
        try:
            tour_time = int(self.tour_time_entry.get())
        except ValueError:
            messagebox.showerror("错误", "移动时间必须是数字!")
            return
        
        self.download_btn.config(state='disabled')
        self.status_label.config(text="正在生成 KML 文件...", fg='#2196F3')
        
        # 创建线程
        self.thread_line = ThreadLine(
            kmlname=self.kmlname_entry.get() or self.kmlname,
            is_mode=(self.flag_var.get() == 1),
            tour_type=self.tour_type_var.get(),
            tour_time=tour_time,
            coords=self.filepath_coords,
            length=self.filepath_length,
            distance=self.filepath_distance
        )
        self.thread_line.on_complete = self.on_download_complete
        self.thread_line.start()
    
    def on_download_complete(self, status):
        """下载完成回调"""
        if status:
            self.status_label.config(text="KML 文件生成成功!", fg='#4CAF50')
            messagebox.showinfo("成功", "KML 文件生成成功!")
        else:
            self.status_label.config(text="KML 文件生成失败!", fg='#f44336')
            messagebox.showerror("错误", "KML 文件生成失败!")
        self.download_btn.config(state='normal')
