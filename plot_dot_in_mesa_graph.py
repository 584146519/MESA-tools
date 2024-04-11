import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tomso import mesa
import tkinter.messagebox as messagebox

#ctrl+k,然后ctrl+0可以全部折叠代码，会清晰很多

read_me='''
This is a simple interactive plot tool for MESA history.data file.
You can input the parameter name and value, then the tool will plot the point in the figure.
You can also change the xlabel and ylabel in the code,to plot different figure.
The code is written by Liuzy, email: <jerry@mail.bnu.edu.cn>.
'''

def find_value_line(parameter, value):
    data=h[str(parameter)]
    num=[]
    for i in range(len(data)-1):
        if data[i]<=value and data[i+1]>=value or data[i]>=value and data[i+1]<=value:
            num.append(i)
    return num
    
class InteractivePlot:
    def __init__(self, master):
        self.master = master
        self.master.title("Interactive Plot")

        # 创建一个顶层的 frame 来包含输入控件和按钮
        top_frame = tk.Frame(self.master)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # 创建 x 坐标的输入框和标签
        tk.Label(top_frame, text="parameter name:").pack(side=tk.LEFT)
        self.entry_x = tk.Entry(top_frame)
        self.entry_x.pack(side=tk.LEFT, padx=5)
        self.entry_x.insert(0, "model_number")  # 设置默认值为 model_number

        # 创建 y 坐标的输入框和标签
        tk.Label(top_frame, text="value:").pack(side=tk.LEFT)
        self.entry_y = tk.Entry(top_frame)
        self.entry_y.pack(side=tk.LEFT, padx=5)
        self.entry_y.insert(0, "1000")  # 设置默认值为 1000

        # 创建一个按钮，用户点击后更新图形
        self.button = tk.Button(top_frame, text="Plot Point", command=self.update_plot)
        self.button.pack(side=tk.LEFT, padx=5)

        # 创建一个 matplotlib 图形
        self.fig, self.ax = plt.subplots(figsize=(5, 4))  # 修改图形的大小
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)  # 将图形嵌入到 Tkinter 界面中
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 初始化图形，画图请在这里完成！！！！！！！！！！！！！！ 

        teff,Lum=h[xlabel],h[ylabel]
        self.ax.plot(teff,Lum,'-r')
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        if invert_x:
            self.ax.invert_xaxis()
        if invert_y:
            self.ax.invert_yaxis()

    def update_plot(self):
        try:
            # 获取用户输入的 x 和 y 值
            x = self.entry_x.get()
            y = float(self.entry_y.get())

            # 在图上绘制点 (x, y)
            num = find_value_line(x, y)
            if len(num) == 0:
                messagebox.showerror("Error", "No value found")
            else:
                for i in num:
                    self.ax.plot(h[xlabel][i], h[ylabel][i], 'bo')
                self.canvas.draw()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



#文件位置
h=mesa.load_history(f'./LOGS/history.data')
#画什么图,很重要，必须写对
xlabel='log_Teff'
ylabel='log_L'

#是否翻转x，y轴（例如赫罗图）
invert_x=True
invert_y=False

print(read_me)
# 创建 Tkinter 主窗口
root = tk.Tk()
app = InteractivePlot(root)
root.mainloop()
