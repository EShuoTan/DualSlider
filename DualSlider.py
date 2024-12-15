import tkinter as tk
from tkinter import ttk


class DualSlider(tk.Frame):
    def __init__(self, parent, Range: tuple[any, any], step, SlideColor: tuple[str, str], BarColor: str):
        super().__init__(parent)
        self.bar_min, self.bar_max = Range  # 滑条范围
        self.step = step  # 步进
        self.SlideColor = SlideColor  # 滑块颜色
        self.BarColor = BarColor  # 滑条颜色
        # 回调函数
        self.call_fun = None
        # 当前两个滑块的位置
        self.sliderMin_val = self.bar_min
        self.sliderMax_val = self.bar_max
        # 用于实现的画布
        self.__canvas = tk.Canvas(self, width=0, height=0)
        self.__canvas.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.__sliderWidth = 0  # 滑块的宽度，不是bar的宽度

        # 滑条和两个滑块
        self.__bar = self.__canvas.create_rectangle(0, 0, 0, 0, fill=self.BarColor, width=0)
        self.__sliderMin = self.__canvas.create_rectangle(0, 0, 0, 0, fill=self.SlideColor[0], tags="sliderMin",
                                                          width=0)
        self.__sliderMax = self.__canvas.create_rectangle(0, 0, 0, 0, fill=self.SlideColor[1], tags="sliderMax",
                                                          width=0)
        # 绑定滑块拖动事件
        self.__canvas.tag_bind("sliderMin", "<B1-Motion>", self.__on_drag_sliderMin)
        self.__canvas.tag_bind("sliderMax", "<B1-Motion>", self.__on_drag_sliderMax)

        # 绑定窗口大小变化事件
        self.bind("<Configure>", self.__update_size)

    def __update_size(self, event):
        f"""{event}"""
        """绘制滑动条和滑块"""
        width = self.winfo_width()
        height = self.winfo_height()
        self.__sliderWidth = round(width / 50)
        # 滑条
        self.__canvas.coords(self.__bar, 0, int((height / 2) - max((height / 15), 2)),
                             width, int((height / 2) + max((height / 15), 2)))
        # 两个滑块
        self.__draw_sliderMin()
        self.__draw_sliderMax()

    def __on_drag_sliderMin(self, event):
        """更新滑块的位置"""
        # 线性插值
        slider_val_float = self.__interp(event.x + (self.__sliderWidth // 2),
                                         (self.__sliderWidth, self.winfo_width() - self.__sliderWidth),
                                         (self.bar_min, self.bar_max - 1))
        # 步进量化
        tmp_slider_val = self.__Step_Quantization(slider_val_float, (self.bar_min, self.bar_max - 1), self.step)
        self.sliderMin_val = min(tmp_slider_val, self.sliderMax_val - self.step)
        self.__draw_sliderMin()
        if self.call_fun is not None:
            self.call_fun("min", self.sliderMin_val)

    def __draw_sliderMin(self):
        sliderX = round(self.__interp(self.sliderMin_val,
                                      (self.bar_min, self.bar_max - 1),
                                      (self.__sliderWidth, self.winfo_width() - self.__sliderWidth)))
        self.__canvas.coords(self.__sliderMin, sliderX - self.__sliderWidth, 0, sliderX, self.winfo_height())

    def __on_drag_sliderMax(self, event):
        """更新滑块的位置"""
        # 线性插值
        slider_val_float = self.__interp(event.x - (self.__sliderWidth // 2),
                                         (self.__sliderWidth, self.winfo_width() - self.__sliderWidth),
                                         (self.bar_min + 1, self.bar_max))
        # 步进量化
        tmp_slider_val = self.__Step_Quantization(slider_val_float, (self.bar_min + 1, self.bar_max), self.step)
        self.sliderMax_val = max(tmp_slider_val, self.sliderMin_val + self.step)
        self.__draw_sliderMax()
        if self.call_fun is not None:
            self.call_fun("max", self.sliderMax_val)

    def __draw_sliderMax(self):
        sliderX = int(self.__interp(self.sliderMax_val,
                                    (self.bar_min + 1, self.bar_max),
                                    (self.__sliderWidth, self.winfo_width() - self.__sliderWidth)))
        self.__canvas.coords(self.__sliderMax, sliderX, 0, sliderX + self.__sliderWidth, self.winfo_height())

    def set_min_val(self, val):
        float_val = min(max(val, self.bar_min), self.sliderMax_val - self.step)
        self.sliderMin_val = self.__Step_Quantization(float_val, (self.bar_min, self.bar_max), self.step)
        self.__draw_sliderMin()
        return self.sliderMin_val

    def set_max_val(self, val):
        float_val = min(max(val, self.sliderMin_val + self.step), self.bar_max)
        self.sliderMax_val = self.__Step_Quantization(float_val, (self.bar_min, self.bar_max), self.step)
        self.__draw_sliderMax()
        return self.sliderMax_val

    def get_min_val(self):
        return self.sliderMin_val

    def get_max_val(self):
        return self.sliderMax_val

    @staticmethod
    def __interp(event_val, src_range, dst_range):
        """计算线性插值"""
        min_x, max_x = src_range
        min_y, max_y = dst_range
        return max(min((event_val - min_x) / (max_x - min_x) * (max_y - min_y) + min_y, max_y), min_y)

    @staticmethod
    def __Step_Quantization(value, Range, step):
        """步进量化"""
        min_val, max_val = Range
        return round((value - min_val) / step) * step + min_val


class DualSliderPro(tk.Frame):
    def __init__(self, parent, Range: tuple[any, any], step, SlideColor: tuple[str, str], BarColor: str):
        super().__init__(parent)
        self.Range = Range
        self.step = step
        self.call_fun = None

        # 创建主框架布局
        self.spin_min = ttk.Spinbox(self, from_=Range[0], to=Range[1], increment=step, width=4, font=("Arial", 13),
                                    command=lambda: self.__on_spin_change(self.spin_min, self.slider.set_min_val))
        self.spin_min.bind("<Return>", lambda event: self.__on_spin_change(self.spin_min, self.slider.set_min_val))

        self.slider = DualSlider(self, Range, step, SlideColor, BarColor)
        self.slider.call_fun = self.__on_slider_change

        self.spin_max = ttk.Spinbox(self, from_=Range[0], to=Range[1], increment=step, width=4, font=("Arial", 13),
                                    command=lambda: self.__on_spin_change(self.spin_max, self.slider.set_max_val))
        self.spin_max.bind("<Return>", lambda event: self.__on_spin_change(self.spin_max, self.slider.set_max_val))

        self.spin_min.grid(row=0, column=0, padx=(0, 2), pady=0)
        self.slider.grid(row=0, column=1, padx=(0, 2), pady=0, sticky="nsew")
        self.spin_max.grid(row=0, column=2, padx=(2, 0), pady=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=200)
        self.grid_columnconfigure(2, weight=1)

        # 初始化 Spinbox 值
        self.spin_min.set(self.slider.get_min_val())
        self.spin_max.set(self.slider.get_max_val())

        # 绑定窗口大小变化事件
        self.bind("<Configure>", self.__update_size)

    def __update_size(self, event):
        """根据控件高度调整 Spinbox 字体大小"""
        f"""{event}"""
        height = self.winfo_height()
        font_size = min(max(13, height // 4), 30)
        new_font = ("Arial", font_size)
        self.spin_min.config(font=new_font)
        self.spin_max.config(font=new_font)

    def __on_spin_change(self, spin, set_fun):
        spin.set(set_fun(float(spin.get())))
        str_tmp = "min"
        if spin == self.spin_max:
            str_tmp = "max"
        if self.call_fun is not None:
            self.call_fun(str_tmp, float(spin.get()))

    def __on_slider_change(self, slider_type, value):
        if slider_type == "min":
            self.spin_min.set(value)
            if self.call_fun is not None:
                self.call_fun("min", float(self.spin_min.get()))
        elif slider_type == "max":
            self.spin_max.set(value)
            if self.call_fun is not None:
                self.call_fun("max", float(self.spin_max.get()))
