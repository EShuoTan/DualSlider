from DualSlider import *

# 创建主窗口
root_window = tk.Tk()
root_window.geometry("1200x300")

# 占位
label = tk.Label(root_window, text="DualSlider", font=("Arial", 15))
label.grid(row=0, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")
slider_1 = DualSlider(root_window, (0, 50), 1, ("red", "green"), "darkgray")
slider_1.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
slider_2 = DualSlider(root_window, (0, 255), 1, ("blue", "red"), "darkgray")
slider_2.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")


label_pro = tk.Label(root_window, text="DualSlider_pro", font=("Arial", 15))
label_pro.grid(row=2, column=0, rowspan=2, padx=0, pady=0, sticky="nsew")
slider_pro1 = DualSliderPro(root_window, (0, 50), 1, ("red", "green"), "darkgray")
slider_pro1.grid(row=2, column=1, padx=0, pady=0, sticky="nsew")
slider_pro2 = DualSliderPro(root_window, (-128, 127), 1, ("blue", "red"), "darkgray")
slider_pro2.grid(row=3, column=1, padx=0, pady=0, sticky="nsew")

# 配置权重
row_weights = [1,
               1,
               1,
               1
               ]
columns_weights = [1, 30, 1]
for row, weight in enumerate(row_weights):
    root_window.grid_rowconfigure(row, weight=weight)
for col, weight in enumerate(columns_weights):
    root_window.grid_columnconfigure(col, weight=weight)
# 运行主循环
root_window.mainloop()
