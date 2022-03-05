from tkinter import Button
from tkinter import Tk
from tkinter import Canvas
from time import sleep
 
import numpy as np
 
Font = ('微软雅黑',5,'bold')

class Maze(object):
    #初始化函数
    def __init__(self):
 
        self.blockcolorIndex = 0
        self.blockcolor = ['black', 'yellow', 'red', 'green','aqua','dodgerblue']  # 障碍颜色为黑色、起点黄色 终点红色、路径绿色
        self.mapStatus = np.ones((15, 15), dtype=int)  # 地图状态数组（全0数组） 1无障碍 0障碍
        self.startPoint = 'start'  # 起点
        self.endPoint = 'end'  # 终点
 
        self.selectedStart = False  # 是否选了起点 默认否
        self.selectedEnd = False  # 是否选了终点 默认否
 
        self.openList = []  # open表
        self.closeList = []  # close表
        self.isOK = False  # 是否已经结束
 
        self.route = []  # 路径列表
        # UI
        self.root = Tk()
        self.root.title('A*迷宫寻路系统')
        self.root.geometry("800x800+300+0")
        self.btn_obstacle = Button(self.root, text="选择障碍", command=self.selectobstacle)
        self.btn_obstacle.pack()
        self.btn_start = Button(self.root, text="选择起点", command=self.selectstart)
        self.btn_start.pack()
        self.btn_end = Button(self.root, text="选择终点", command=self.selectend)
        self.btn_end.pack()
        self.btn_action = Button(self.root, text="开始寻路", command=self.selectaction)
        self.btn_action.pack()
        self.btn_restart = Button(self.root, text="重新开始", command=self.selectrestart)
        self.btn_restart.pack()
        self.canvas = Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack()
        for i in range(1, 17):
            self.canvas.create_line(30, 30 * i, 480, 30 * i)  # 横线
            self.canvas.create_line(30 * i, 30, 30 * i, 480)  # 竖线
        self.canvas.bind("<Button-1>", self.drawMapBlock) # 绑定事件和鼠标左键一起
        self.root.mainloop() # 给予点按反馈
    #重新开始函数
    def selectrestart(self):
        self.mapStatus = np.ones((15, 15), dtype=int)  # 地图状态数组（全0数组） 1无障碍 0障碍
        self.startPoint = 'start'
        self.endPoint = 'end'
        self.selectedStart = False  # 是否选了起点 默认否
        self.selectedEnd = False  # 是否选了终点 默认否
        self.openList = []  # open表
        self.closeList = []  # close表
        self.isOK = False  # 是否已经结束
        self.route = []
        self.canvas.destroy()
        self.canvas = Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack()
 
        for i in range(1, 17):
            self.canvas.create_line(30, 30 * i, 480, 30 * i)  # 横线
            self.canvas.create_line(30 * i, 30, 30 * i, 480)  # 竖线
        self.canvas.bind("<Button-1>", self.drawMapBlock)
 
    def selectobstacle(self):
        self.blockcolorIndex = 0  # 'black'黑色
 
    def selectstart(self):
        if not self.selectedStart:
            self.blockcolorIndex = 1  # yellow黄色
        else:
            self.blockcolorIndex = 0  # black黑色
 
    def selectend(self):
        if not self.selectedEnd:
            self.blockcolorIndex = 2  # red红色
        else:
            self.blockcolorIndex = 0  # black黑色
 
    def selectaction(self):
        self.blockcolorIndex = 3  # 'green'绿色
        self.Astart() # 调用A*函数
        self.route.pop(-1)
        self.route.pop(0)
        #self.route.pop(0)
        for i in self.route:
            self.canvas.create_rectangle((i.x + 1) * 30, (i.y + 1) * 30, (i.x + 2) * 30, (i.y + 2) * 30, fill='green')
            tempstr=i.g
            int(tempstr)
            self.canvas.create_text( ((i.x+1)*30+9,(i.y+1)*30+5),text=i.evaluate(),
                                    font = Font,fill = 'black'
                                    )
            self.canvas.create_text( ((i.x+1)*30+9,(i.y+2)*30-5),text=tempstr,
                                    font = Font,fill = 'blue'
                                    )
            self.canvas.create_text( ((i.x+2)*30-7,(i.y+2)*30-15),text=i.h,
                                    font = Font,fill = 'red'
                                    )
            
    
    #A*算法
    def Astart(self):
        # 将起点放到open表中
        self.openList.append(self.startPoint)
        while (not self.isOK):
            # 先检查终点是否在open表中 ，没有继续，有则结束
            if self.inOpenList(self.endPoint) != -1:  # 在open表中
                self.isOK = True  
                self.end = self.openList[self.inOpenList(self.endPoint)]
                self.route.append(self.end)
                self.te = self.end
                #self.canvas.create_rectangle((self.endPoint.x + 1) * 30, (self.endPoint.y + 1) * 30, (self.endPoint.x + 2) * 30, (self.endPoint.y + 2) * 30,
                                            # fill=self.blockcolor[self.blockcolorIndex])
                while (self.te.parentPoint != 0):
                    self.te = self.te.parentPoint
                    self.route.append(self.te)
            else:
                self.sortOpenList()  # 将估值最小的节点放在index = 0
                current_min = self.openList[0]  # 估值最小节点
                #self.canvas.create_rectangle(current_min.x,current_min.y,current_min.x+1,current_min.y+1,fill=self.blockcolor[4])
                self.openList.pop(0)
                self.closeList.append(current_min)
                #self.canvas.create_rectangle((current_min.x+1)*30,(current_min.y+1)*30,(current_min.x+2)*30,(current_min.y+2)*30,fill=self.blockcolor[5])

                # 开拓current_min节点，并放到open 表
                if current_min.x - 1 >= 0:  # 没有越界
                    if (self.mapStatus[current_min.y][current_min.x - 1]) != 0:  # 西侧非障碍，可开拓
                        self.temp1 = mapPoint(current_min.x - 1, current_min.y, current_min.distanceStart + 1,
                                              self.endPoint.x, self.endPoint.y, current_min)
                        if self.inOpenList(self.temp1) != -1:  # open表存在相同的节点
                            if self.temp1.evaluate() < self.openList[self.inOpenList(self.temp1)].evaluate():
                                self.openList[self.inOpenList(self.temp1)] = self.temp1
                        elif self.inCloseList(self.temp1) != -1:  # 否则查看close表是否存在相同的节点（存在）
                            if self.temp1.evaluate() < self.closeList[self.inCloseList(self.temp1)].evaluate():
                                self.closeList[self.inCloseList(self.temp1)] = self.temp1
                        else:  # open 、 close表都不存在 temp1
                            self.openList.append(self.temp1)
                            self.canvas.create_rectangle((self.temp1.x+1)*30,(self.temp1.y+1)*30,(self.temp1.x+2)*30,(self.temp1.y+2)*30,fill=self.blockcolor[4])
                            tempstr=self.temp1.g
                            #int(tempstr)
                            self.canvas.create_text( ((self.temp1.x+1)*30+9,(self.temp1.y+1)*30+5),text=self.temp1.evaluate(),
                                    font = Font,fill = 'black'
                                    )
                            self.canvas.create_text( ((self.temp1.x+1)*30+9,(self.temp1.y+2)*30-5),text=tempstr,
                                    font = Font,fill = 'blue'
                                    )
                            self.canvas.create_text( ((self.temp1.x+2)*30-7,(self.temp1.y+2)*30-15),text=self.temp1.h,
                                    font = Font,fill = 'red'
                                    )

                if current_min.y + 1 < 15 and current_min.x - 1 > 0:
                    if (self.mapStatus[current_min.y+1][current_min.x-1]) != 0 :  # 西北侧非障碍,可开拓
                        if (self.mapStatus[current_min.y+1][current_min.x]) != 0 or  (self.mapStatus[current_min.y][current_min.x-1]) != 0: # 西北侧不被堵住
                            self.temp5 = mapPoint(current_min.x - 1, current_min.y+1, current_min.distanceStart + 1.4,
                                                  self.endPoint.x, self.endPoint.y, current_min)
                            if self.inOpenList(self.temp5) != -1:  # open表存在相同的节点
                                if self.temp5.evaluate() < self.openList[self.inOpenList(self.temp5)].evaluate():
                                    self.openList[self.inOpenList(self.temp5)] = self.temp5
                            elif self.inCloseList(self.temp5) != -1:  # 否则查看close表是否存在相同的节点（存在）
                                if self.temp5.evaluate() < self.closeList[self.inCloseList(self.temp5)].evaluate():
                                    self.closeList[self.inCloseList(self.temp5)] = self.temp5
                            else:
                                self.openList.append(self.temp5)
                                self.canvas.create_rectangle((self.temp5.x+1)*30,(self.temp5.y+1)*30,(self.temp5.x+2)*30,(self.temp5.y+2)*30,fill=self.blockcolor[4])
                            tempstr=self.temp5.g
                            #int(tempstr)
                            self.canvas.create_text( ((self.temp5.x+1)*30+9,(self.temp5.y+1)*30+5),text=self.temp5.evaluate(),
                                    font = Font,fill = 'black'
                                    )
                            self.canvas.create_text( ((self.temp5.x+1)*30+9,(self.temp5.y+2)*30-5),text=tempstr,
                                    font = Font,fill = 'blue'
                                    )
                            self.canvas.create_text( ((self.temp5.x+2)*30-7,(self.temp5.y+2)*30-15),text=self.temp5.h,
                                    font = Font,fill = 'red'
                                    )

 
                if current_min.x + 1 < 15:
                    if (self.mapStatus[current_min.y][current_min.x + 1]) != 0:  # 东侧非障碍,可开拓
                        self.temp2 = mapPoint(current_min.x + 1, current_min.y, current_min.distanceStart + 1,
                                              self.endPoint.x, self.endPoint.y, current_min)
                        if self.inOpenList(self.temp2) != -1:  # open表存在相同的节点
                            if self.temp2.evaluate() < self.openList[self.inOpenList(self.temp2)].evaluate():
                                self.openList[self.inOpenList(self.temp2)] = self.temp2
                        elif self.inCloseList(self.temp2) != -1:  # 否则查看close表是否存在相同的节点（存在）
                            if self.temp2.evaluate() < self.closeList[self.inCloseList(self.temp2)].evaluate():
                                self.closeList[self.inCloseList(self.temp2)] = self.temp2
                        else:
                            self.openList.append(self.temp2)
                            self.canvas.create_rectangle((self.temp2.x+1)*30,(self.temp2.y+1)*30,(self.temp2.x+2)*30,(self.temp2.y+2)*30,fill=self.blockcolor[4])
                            tempstr=self.temp2.g
                            #int(tempstr)
                            self.canvas.create_text( ((self.temp2.x+1)*30+9,(self.temp2.y+1)*30+5),text=self.temp2.evaluate(),
                                    font = Font,fill = 'black'
                                    )
                            self.canvas.create_text( ((self.temp2.x+1)*30+9,(self.temp2.y+2)*30-5),text=tempstr,
                                    font = Font,fill = 'blue'
                                    )
                            self.canvas.create_text( ((self.temp2.x+2)*30-7,(self.temp2.y+2)*30-15),text=self.temp2.h,
                                    font = Font,fill = 'red'
                                    )

 
                if current_min.x + 1 < 15 and current_min.y + 1 < 15:
                    if (self.mapStatus[current_min.y+1][current_min.x+1]) != 0 :  # 东北侧非障碍,可开拓
                        if (self.mapStatus[current_min.y+1][current_min.x]) != 0 or  (self.mapStatus[current_min.y][current_min.x+1]) != 0: # 东北侧不被堵住
                            self.temp6 = mapPoint(current_min.x + 1, current_min.y+1, current_min.distanceStart + 1.4,
                                                  self.endPoint.x, self.endPoint.y, current_min)
                            if self.inOpenList(self.temp6) != -1:  # open表存在相同的节点
                                if self.temp6.evaluate() < self.openList[self.inOpenList(self.temp6)].evaluate():
                                    self.openList[self.inOpenList(self.temp6)] = self.temp6
                            elif self.inCloseList(self.temp6) != -1:  # 否则查看close表是否存在相同的节点（存在）
                                if self.temp6.evaluate() < self.closeList[self.inCloseList(self.temp6)].evaluate():
                                    self.closeList[self.inCloseList(self.temp6)] = self.temp6
                            else:
                                self.openList.append(self.temp6)
                                self.canvas.create_rectangle((self.temp6.x+1)*30,(self.temp6.y+1)*30,(self.temp6.x+2)*30,(self.temp6.y+2)*30,fill=self.blockcolor[4])
                            tempstr=self.temp6.g
                           # int(tempstr)
                            self.canvas.create_text( ((self.temp6.x+1)*30+9,(self.temp6.y+1)*30+5),text=self.temp6.evaluate(),
                                    font = Font,fill = 'black'
                                    )
                            self.canvas.create_text( ((self.temp6.x+1)*30+9,(self.temp6.y+2)*30-5),text=tempstr,
                                    font = Font,fill = 'blue'
                                    )
                            self.canvas.create_text( ((self.temp6.x+2)*30-7,(self.temp6.y+2)*30-15),text=self.temp6.h,
                                    font = Font,fill = 'red'
                                    )



                if current_min.y - 1 >= 0:
                    if (self.mapStatus[current_min.y - 1][current_min.x]) != 0:  # 南侧非障碍,可开拓
                        self.temp3 = mapPoint(current_min.x, current_min.y - 1, current_min.distanceStart + 1,
                                              self.endPoint.x, self.endPoint.y, current_min)
                        if self.inOpenList(self.temp3) != -1:  # open表存在相同的节点
                            if self.temp3.evaluate() < self.openList[self.inOpenList(self.temp3)].evaluate():
                                self.openList[self.inOpenList(self.temp3)] = self.temp3
                        elif self.inCloseList(self.temp3) != -1:  # 否则查看close表是否存在相同的节点（存在）
                            if self.temp3.evaluate() < self.closeList[self.inCloseList(self.temp3)].evaluate():
                                self.closeList[self.inCloseList(self.temp3)] = self.temp3
                        else:
                            self.openList.append(self.temp3)
                            self.canvas.create_rectangle((self.temp3.x+1)*30,(self.temp3.y+1)*30,(self.temp3.x+2)*30,(self.temp3.y+2)*30,fill=self.blockcolor[4])
                            tempstr=self.temp3.g
                            #int(tempstr)
                            self.canvas.create_text( ((self.temp3.x+1)*30+9,(self.temp3.y+1)*30+5),text=self.temp3.evaluate(),
                                    font = Font,fill = 'black'
                                    )
                            self.canvas.create_text( ((self.temp3.x+1)*30+9,(self.temp3.y+2)*30-5),text=tempstr,
                                    font = Font,fill = 'blue'
                                    )
                            self.canvas.create_text( ((self.temp3.x+2)*30-7,(self.temp3.y+2)*30-15),text=self.temp3.h,
                                    font = Font,fill = 'red'
                                    )


                if current_min.y - 1 > 0 and current_min.x - 1 > 0:
                    if (self.mapStatus[current_min.y-1][current_min.x-1]) != 0 :  # 西南侧非障碍,可开拓
                        if (self.mapStatus[current_min.y-1][current_min.x]) != 0 or  (self.mapStatus[current_min.y][current_min.x-1]) != 0: # 西南侧不被堵住
                            self.temp7 = mapPoint(current_min.x - 1, current_min.y-1, current_min.distanceStart + 1.4,
                                                  self.endPoint.x, self.endPoint.y, current_min)
                            if self.inOpenList(self.temp7) != -1:  # open表存在相同的节点
                                if self.temp7.evaluate() < self.openList[self.inOpenList(self.temp7)].evaluate():
                                    self.openList[self.inOpenList(self.temp7)] = self.temp7
                            elif self.inCloseList(self.temp7) != -1:  # 否则查看close表是否存在相同的节点（存在）
                                if self.temp7.evaluate() < self.closeList[self.inCloseList(self.temp7)].evaluate():
                                    self.closeList[self.inCloseList(self.temp7)] = self.temp7
                            else:
                                self.openList.append(self.temp7)
                                self.canvas.create_rectangle((self.temp7.x+1)*30,(self.temp7.y+1)*30,(self.temp7.x+2)*30,(self.temp7.y+2)*30,fill=self.blockcolor[4])
                            tempstr=self.temp7.g
                            #int(tempstr)
                            self.canvas.create_text( ((self.temp7.x+1)*30+9,(self.temp7.y+1)*30+5),text=self.temp7.evaluate(),
                                    font = Font,fill = 'black'
                                    )
                            self.canvas.create_text( ((self.temp7.x+1)*30+9,(self.temp7.y+2)*30-5),text=tempstr,
                                    font = Font,fill = 'blue'
                                    )
                            self.canvas.create_text( ((self.temp7.x+2)*30-7,(self.temp7.y+2)*30-15),text=self.temp7.h,
                                    font = Font,fill = 'red'
                                    )


 
                if current_min.y + 1 < 15:
                    if (self.mapStatus[current_min.y + 1][current_min.x]) != 0:  # 北侧非障碍,可开拓
                        self.temp4 = mapPoint(current_min.x, current_min.y + 1, current_min.distanceStart + 1,
                                              self.endPoint.x, self.endPoint.y, current_min)
 
                        if self.inOpenList(self.temp4) != -1:  # open表存在相同的节点
                            if self.temp4.evaluate() < self.openList[self.inOpenList(self.temp4)].evaluate():
                                self.openList[self.inOpenList(self.temp4)] = self.temp4
                        elif self.inCloseList(self.temp4) != -1:  # 否则查看close表是否存在相同的节点（存在）
                            if self.temp4.evaluate() < self.closeList[self.inCloseList(self.temp4)].evaluate():
                                self.closeList[self.inCloseList(self.temp4)] = self.temp4
                        else:
                            self.openList.append(self.temp4)
                            self.canvas.create_rectangle((self.temp4.x+1)*30,(self.temp4.y+1)*30,(self.temp4.x+2)*30,(self.temp4.y+2)*30,fill=self.blockcolor[4])
                            tempstr=self.temp4.g
                            #int(tempstr)
                            self.canvas.create_text( ((self.temp4.x+1)*30+9,(self.temp4.y+1)*30+5),text=self.temp4.evaluate(),
                                    font = Font,fill = 'black'
                                    )
                            self.canvas.create_text( ((self.temp4.x+1)*30+9,(self.temp4.y+2)*30-5),text=tempstr,
                                    font = Font,fill = 'blue'
                                    )
                            self.canvas.create_text( ((self.temp4.x+2)*30-7,(self.temp4.y+2)*30-15),text=self.temp4.h,
                                    font = Font,fill = 'red'
                                    )



                if current_min.y - 1 > 0 and current_min.x + 1 < 15:
                    if (self.mapStatus[current_min.y-1][current_min.x+1]) != 0 :  # 东南侧非障碍,可开拓
                        if (self.mapStatus[current_min.y-1][current_min.x]) != 0 or  (self.mapStatus[current_min.y][current_min.x+1]) != 0: # 东南侧不被堵住
                            self.temp8 = mapPoint(current_min.x + 1, current_min.y-1, current_min.distanceStart + 1.4,
                                                  self.endPoint.x, self.endPoint.y, current_min)
                            if self.inOpenList(self.temp8) != -1:  # open表存在相同的节点
                                if self.temp8.evaluate() < self.openList[self.inOpenList(self.temp8)].evaluate():
                                    self.openList[self.inOpenList(self.temp8)] = self.temp8
                            elif self.inCloseList(self.temp8) != -1:  # 否则查看close表是否存在相同的节点（存在）
                                if self.temp8.evaluate() < self.closeList[self.inCloseList(self.temp8)].evaluate():
                                    self.closeList[self.inCloseList(self.temp8)] = self.temp8
                            else:
                                self.openList.append(self.temp8)
                                self.canvas.create_rectangle((self.temp8.x+1)*30,(self.temp8.y+1)*30,(self.temp8.x+2)*30,(self.temp8.y+2)*30,fill=self.blockcolor[4])
                            tempstr=self.temp8.g
                            #int(tempstr)
                            self.canvas.create_text( ((self.temp8.x+1)*30+9,(self.temp8.y+1)*30+5),text=self.temp8.evaluate(),
                                    font = Font,fill = 'black'
                                    )
                            self.canvas.create_text( ((self.temp8.x+1)*30+9,(self.temp8.y+2)*30-5),text=tempstr,
                                    font = Font,fill = 'blue'
                                    )
                            self.canvas.create_text( ((self.temp8.x+2)*30-7,(self.temp8.y+2)*30-15),text=self.temp8.h,
                                    font = Font,fill = 'red'
                                    )

    

    def drawMapBlock(self, event):
        x, y = event.x, event.y
        if (30 <= x <= 480) and (30 <= y <= 480):
            i = int((x // 30) - 1)
            j = int((y // 30) - 1)
            # 记录下起止点，并不能选择多个起点或者多个终点
            if self.blockcolorIndex == 1 and not self.selectedStart: # 黄色起点
                self.startPoint = mapPoint(i, j, 0, 0, 0, 0)
                self.selectedStart = True
                self.canvas.create_rectangle((i + 1) * 30, (j + 1) * 30, (i + 2) * 30, (j + 2) * 30,
                                             fill=self.blockcolor[self.blockcolorIndex])
                self.blockcolorIndex = 0
            elif self.blockcolorIndex == 2 and not self.selectedEnd: # 红色终点
                self.endPoint = mapPoint(i, j, 0, 0, 0, 0)
                self.selectedEnd = True
                self.canvas.create_rectangle((i + 1) * 30, (j + 1) * 30, (i + 2) * 30, (j + 2) * 30,
                                             fill=self.blockcolor[self.blockcolorIndex])
                self.blockcolorIndex = 0
            elif self.blockcolorIndex == 0: #黑色障碍
                self.canvas.create_rectangle((i + 1) * 30, (j + 1) * 30, (i + 2) * 30, (j + 2) * 30,
                                             fill=self.blockcolor[self.blockcolorIndex])
                self.mapStatus[j][i] = self.blockcolorIndex

            elif self.blockcolorIndex == 3: # 绿色路径
                self.canvas.create_rectangle((i + 1) * 30, (j + 1) * 30, (i + 2) * 30, (j + 2) * 30,
                                             fill=self.blockcolor[self.blockcolorIndex])
                self.mapStatus[j][i] = self.blockcolorIndex
 
    # 检查终点是否在open表中
    def endInOpenList(self):
        for i in self.openList:
            if self.endPoint[0] == i.x and self.endPoint[1] == i.y:
                return True
        return False
 
    # 将节点加进open表前，检查该节点是否在open表中
    def inOpenList(self, p1):
        for i in range(0, len(self.openList)):
            if p1.isEq(self.openList[i]):
                return i
        return -1
 
    # 将节点加进open表前，检查该节点是否在close表中
    # 若在返回索引，不在返回-1
    def inCloseList(self, p1):
        for i in range(0, len(self.closeList)):
            if p1.isEq(self.closeList[i]):
                return i
        return -1
 
    # 将 估值最小的 排在 index = 0
    def sortOpenList(self):
        if len(self.openList) > 0:
            if len(self.openList) > 1:
                for i in range(1, len(self.openList)):
                    if self.openList[i].evaluate() < self.openList[0].evaluate():
                        self.t = self.openList[0]
                        self.openList[0] = self.openList[i]
                        self.openList[i] = self.t
 
 
class mapPoint(object):
    def __init__(self, x, y, distanceStart, endX, endY, parentPoint):
        self.x = x
        self.y = y
        self.distanceStart = distanceStart
        self.endX = endX
        self.endY = endY
        self.g = distanceStart
        self.h = abs(x - endX) + abs(y - endY)
        self.f = distanceStart + abs(x - endX) + abs(y - endY)
        self.parentPoint = parentPoint  # 前一个节点
 
    def evaluate(self): # 曼哈顿距离
        g=self.distanceStart
        h= round(abs(self.x - self.endX) + abs(self.y - self.endY),2)
        f=g+h
        return f
 
    def isEq(self, point):
        if point.x == self.x and point.y == self.y:
            return True
        else:
            return False
 
 
def main():
    Maze()
 
 
if __name__ == '__main__':
    main()
