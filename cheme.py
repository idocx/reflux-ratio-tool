import os.path

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import matplotlib
matplotlib.rcParams["font.family"] = "STSong"  # 设置中文字体
matplotlib.rcParams["font.size"] = 14  # 设置字号

current_dir = os.path.dirname(os.path.abspath(__file__))  #  文件路径


def two_p(p1, p2):
    """
    由两点确定一条直线
    : para : p1, p2: 形如[x, y]的两点
    : return : 直线方程（函数）f(x)
    """
    x1, y1 = p1
    x2, y2 = p2
    slope = (y2 - y1) / (x2 - x1)
    intercept = (y1 * x2 - x1 * y2) / (x2 - x1)
    return lambda x: slope * x + intercept


# parse args
flag = input("（1）全回流 /（2）部分回流 [选择1或者2]：")

if flag == "2":     # 部分回流
    flag = False

    # 数据
    delta = float(input("delta："))
    r = 4
    xw = float(input("xw："))
    xd = float(input("xd："))
    xf = float(input("xf："))
elif flag == "1":   # 全回流
    flag = True

    # 数据
    xw = float(input("xw："))
    xd = float(input("xd："))
else:
    raise ValueError("Expect 1/2, but get {}".format(flag))

if flag:  # 全回流的情况
    title = "全回流"
else:  # 部分回流的情况
    #title = "部分回流, R={}, 板{}进料".format(r, level)
    title = "部分回流，R={}".format(r)
    a = [xd, xd]
    b = [xw, xw]
    c = [0, xd/(r+1)]
    l_jl = two_p(a, c)
    d = [(xf/(delta-1)+xd/(r+1))/(delta/(delta-1)-r/(r+1)), 0]
    d[1] = l_jl(d[0])
    l_tl = two_p(b, d)

x_y = np.loadtxt(os.path.join(current_dir, "x_y.csv"), delimiter=',')
f_y_x = interpolate.interp1d(x_y[1], x_y[0], kind="slinear")  # 线性插值做出平衡线

# 作图相关参数设置
plt.title(title)
plt.xlabel("$x$")
plt.ylabel('$y$')

# 做出平衡线与对角线
plt.plot(x_y[0], x_y[1], color="black")  
plt.plot([0, 1], [0, 1], color="black")

# 标记出各点
plt.annotate("$a$ ($x_d$, $x_d$)", [xd, xd], xytext=(5, -10), textcoords="offset points")
plt.annotate("$b$ ($x_w$, $x_w$)", [xw, xw], xytext=(5, -10), textcoords="offset points")
plt.scatter([xd, xw], [xd, xw], color="black", s=10)

# 部分回流的情况
if not flag:
    plt.annotate("$d$ ({0:.2}, {1:.2})".format(*d), d, xytext=(5, -10), textcoords="offset points", color="red")
    plt.plot([b[0], d[0], a[0]],[b[1], d[1], a[1]], color="red") 
    plt.scatter(*d, color="red", marker="o", s=15)  


def l(x):
    """
    操作线方程
    """
    if flag or x < xw:
        return x
    elif x < d[0]:
        return l_tl(x)
    else:
        return l_jl(x)
    

# 绘制折线
x_tmp = xd
y_tmp = l(x_tmp)
x_line = []
y_line = []
cnt = 0
while x_tmp > xw+0.005:  # 加上一个小数，否则在xw=0时会出问题
    cnt += 1
    x_line.append(x_tmp)
    y_line.append(y_tmp)
    x_tmp = f_y_x(y_tmp)
    x_line.append(x_tmp)
    y_line.append(y_tmp)
    plt.annotate(cnt, [x_tmp, y_tmp], xytext=(-10, 5), textcoords="offset points")
    y_tmp = l(x_tmp)
x_line.append(x_tmp)
y_line.append(y_tmp)

plt.plot(x_line, y_line)  # 把折线在图上画出来

plt.show()
plt.savefig(os.path.join(current_dir, "{}.svg".format(title)))