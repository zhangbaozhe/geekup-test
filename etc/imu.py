import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import re
# Fixing random state for reproducibility
np.random.seed(196)
#初始数据绘图
dis = np.zeros(40)
dis2 = dis
fig, ax = plt.subplots()
line, = ax.plot(dis)
ax.set_ylim(-180, 180)
plt.grid(True)
ax.set_ylabel("angle")
ax.set_xlabel("time")

ser = serial.Serial('COM4',57600)


def update(frames):
    global dis
    global dis2
    global line 
    global ser 

    #读入模拟
    #a = np.random.rand()*2-1
    a = get_message(ser) 
    send_x(ser,30)
    send_y(ser,40)
    #a = get_message(ser)
    ser.flushInput()
    time.sleep(0.1)

    #time.sleep(np.random.rand()/10)
    #绘图数据生成  
    dis[0:-1] = dis2[1:] 
    dis[-1] = a
    dis2 = dis
    #绘图 
    line.set_ydata(dis)    
    #颜色设置
    plt.setp(line, 'color', 'r', 'linewidth', 2.0)
    # if abs(a) < 0.5:
    #     plt.setp(line, 'color', 'r', 'linewidth', 2.0)
    # else:
    #     plt.setp(line, 'color', 'b', 'linewidth', 2.0)
    return line


def get_message(ser):
    mess=0
    mess=ser.readline()
    mess=bytes.decode(mess)
    #print(mess)
    #mess=mess.split('.')[0]
    #print(mess)
    #mess=re.sub('\D','',mess)
    
    mess=float(mess)
    print(mess)
    return mess
    
    # print(mess)

def send_x(ser,x):
    command = x
    command=('+'+str(command)+'x').encode(encoding='utf-8')
    ser.write(command)

def send_y(ser,y):
    command = y
    command=('*'+str(command)+'y').encode(encoding='utf-8')
    ser.write(command)



ani = animation.FuncAnimation(fig, update, frames= None, interval=100)
plt.show()

# def run(ser):
#     while True:
#         mess = get_message(ser)
#         send_x(ser,2)
#         #mess = get_message(ser)
#         send_y(ser,4)
#         #mess = get_message(ser)
#         ser.flushInput()
#         time.sleep(0.1)
        
#run(ser)