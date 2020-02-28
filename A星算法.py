

'''
看到项目中有一个A*算法,跟图有关,挺有意思.在游戏中很常用.


所以看到网上一个python实现,现在来研究一下.

这个算法主要是跟dijikstra算法比较.他是启发型的但是保证找到最优解.速度比地理特斯拉算法要快很多!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

'''



#需要进行抽象化的有：节点（属性有：x y坐标  父节点  g及h ）  地图（属性有高度 宽度  数据(数据中有可通行路径与障碍两种)）
#A_star :
# open_list (存放待测试的点，刚开始有start加入list，后面每一个current的相邻点（不能位于colse_list中且不是终点）要放到open_list中) 表示已经走过的点
# close_list(存放已测试的点，已经当过current的点，就放到close_list中) 存放已经探测过的点，不必再进行探测
# current 现在正在测试的点，要计算current周围的点的代价f  经过current后要放到close_list中 将openlist代价f最小的node当作下一个current
# start_point end_point

#初始化地图  openlist closelist node
#将start点放入openlist中
#while（未达到终点）：
#取出 openlist 中的点 将这个点设置为current 并放入closelist中
#for node_near in（current的临近点）
#if（current的临近点 node_near 不在closelist中且不为障碍）：
#计算 node_near 的f（f=g+h）大小
# if( node_near 不在 openlist 中)   #表示这个节点可以进行探索.
# 将 node_near 放入 openlist，并将其父节点设置为current 然后将f值设置为计算出的f值
# else if( node_near 在 openlist 中)
#  if（计算出的f大于在openlist中的f）
#    不动作
#  else if（计算出的f小于等于在openlist中的f）
#     将 openlist 中的 node_near 的f值更新为计算出的新的更小的f值 并将父节点设置为current
#返回并继续循环



# 之前的算法没有,在对角线和直线上加不同的权重,就导致最优解可能会走斜线来到达直线就能到达的目标.
# 所以加上对角权重即可.









import sys
#将地图中的点抽象化成类
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y




# __eq__ 定义了类的等号(==)行为
    def __eq__(self, other): #函数重载
        if((self.x == other.x )and (self.y == other.y)):
            return  1
        else:
            return 0

#通过列表实现的地图的建立  类c语言数组？
class map_2d:
    def __init__(self,height,width):
        self.height = height
        self.width = width

        self.data = [[0 for i in range(width)] for j in range(height)]
    def map_show(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.data[i][j], end=' ')
            print("")

            # 设置障碍,也就是填入1.


    #          注意游戏地图一定要有边缘,所以最后的2b地图周围一圈必须都是1才行.
    # 这样obstacle 中也包含了是否超出边界的处理过程.
    def obstacle(self,obstacle_x,obstacle_y):
        self.data[obstacle_x][obstacle_y]=1


        # 字符6表示开始和结束点.
    def end_draw(self,point):
        self.data[point.x][point.y] = 6

#A*算法的实现
class A_star:
    # 设置node, 这些node作为地图中点的抽象,往list中放.
    class Node:
        def __init__(self, point, endpoint, g):
            self.point = point  # 自己当前的坐标
            self.endpoint = endpoint  # 目标结束点的坐标.
            self.father = None  # 父节点
            self.g = g  # g值，g值在用到的时候会重新算


            # 结束点到当前带点的海明距离*10
            self.h = (abs(endpoint.x - point.x) + abs(endpoint.y - point.y)) * 10  # 计算h值
            self.f = self.g + self.h  # f值就是q值.

        #寻找临近点, 然后返回这个点抽象之后的node
        def search_near(self,ud,rl):  # up  down  right left


            # ud,rl 都是-1 or 1表示周围的点.
            nearpoint = Point(self.point.x + rl, self.point.y + ud)

            # 下面为什么要加1 我们把权重写在这个地方. 就是后面+1,下面我修改这个为对角衰减类型
            # nearnode = A_star.Node(nearpoint, self.endpoint, self.g+1 )

            #我修改的对角衰减类型.
            if 0 in [ud,rl]:

                 nearnode = A_star.Node(nearpoint, self.endpoint, self.g+1 )
            else:
                nearnode = A_star.Node(nearpoint, self.endpoint, self.g + 1.4)






            return nearnode




    def __init__(self,start_point,end_point,map):#需要传输到类中的，在此括号中写出
        self.path=[]
        self.close_list=[] #存放已经走过的点
        self.open_list=[] #存放需要尽心探索的点
        self.current = 0 #现在的node
        self.start_point=start_point
        self.end_point=end_point
        self.map = map #所在地图






# 这个select 体现了贪婪,因为先计算最小的min,然后走 f值最小的那个节点.
    def select_current(self):
        min=10000000
        node_temp = 0

        # 找到open表中 f值最小的节点.吧他当作下一步应该走到的位置!并且就这么走
        # 在记录表中记录下这个一个步奏.
        for ele in self.open_list:
            if ele.f < min:
                min = ele.f
                node_temp = ele




        self.path.append(node_temp)
        self.open_list.remove(node_temp)
        self.close_list.append(node_temp)
        return node_temp








    def isin_openlist(self,node):
        for opennode_temp in self.open_list:
            if opennode_temp.point == node.point:
                return opennode_temp
        return 0

    def isin_closelist(self,node):
        for closenode_temp in self.close_list:
            if closenode_temp.point == node.point:
                return 1
        return 0

    def is_obstacle(self,node):
        if self.map.data[node.point.x][node.point.y]==1 :
            return  1
        return  0













    # 整个算法的核心函数就这个一个!!!!!!!!!
    def near_explore(self,node):



        # 对周围8个方块进行逐个判断,所以是8个类似的部分!!!!!!!
        ud = 1
        rl = 0
        node_temp = node.search_near(ud,rl) #在调用另一个类的方法时（不论是子类还是在类外定义的类），都要进行实例化才能调用函数
        if node_temp.point == end_point:
            return 1 # 返回1表示已经不用再搜索了,返回0表示还没到终点.
        elif self.isin_closelist(node_temp):  # closelist表示搜索过的点.
            pass
        elif self.is_obstacle(node_temp): # 表示不能走的点,也pass掉.
            pass
        elif self.isin_openlist(node_temp) == 0: # 之前openlist 作更新.
            node_temp.father = node
            self.open_list.append(node_temp)
        else:# 下行是动态规划的公式核心.  # 也就是node的f值更新而已.
            if node_temp.f < (self.isin_openlist(node_temp)).f:
                self.open_list.remove(self.isin_openlist(node_temp))
                node_temp.father = node
                self.open_list.append(node_temp)










        ud = -1
        rl = 0
        node_temp = node.search_near(ud,rl) #在调用另一个类的方法时（不论是子类还是在类外定义的类），都要进行实例化才能调用函数
        if node_temp.point == end_point:
            return 1
        elif self.isin_closelist(node_temp):
            pass
        elif self.is_obstacle(node_temp):
            pass
        elif self.isin_openlist(node_temp) == 0:
            node_temp.father = node
            self.open_list.append(node_temp)
        else:
            if node_temp.f < (self.isin_openlist(node_temp)).f:
                self.open_list.remove(self.isin_openlist(node_temp))
                node_temp.father = node
                self.open_list.append(node_temp)

        ud = 0
        rl = 1
        node_temp = node.search_near(ud,rl) #在调用另一个类的方法时（不论是子类还是在类外定义的类），都要进行实例化才能调用函数
        if node_temp.point == end_point:
            return 1
        elif self.isin_closelist(node_temp):
            pass
        elif self.is_obstacle(node_temp):
            pass
        elif self.isin_openlist(node_temp) == 0:
            node_temp.father = node
            self.open_list.append(node_temp)
        else:
            if node_temp.f < (self.isin_openlist(node_temp)).f:
                self.open_list.remove(self.isin_openlist(node_temp))
                node_temp.father = node
                self.open_list.append(node_temp)

        ud = 0
        rl = -1
        node_temp = node.search_near(ud,rl) #在调用另一个类的方法时（不论是子类还是在类外定义的类），都要进行实例化才能调用函数
        if node_temp.point == end_point:
            return 1
        elif self.isin_closelist(node_temp):
            pass
        elif self.is_obstacle(node_temp):
            pass
        elif self.isin_openlist(node_temp) == 0:
            node_temp.father = node
            self.open_list.append(node_temp)
        else:
            if node_temp.f < (self.isin_openlist(node_temp)).f:
                self.open_list.remove(self.isin_openlist(node_temp))
                node_temp.father = node
                self.open_list.append(node_temp)

        ud = 1
        rl = 1
        node_temp = node.search_near(ud,rl) #在调用另一个类的方法时（不论是子类还是在类外定义的类），都要进行实例化才能调用函数
        if node_temp.point == end_point:
            return 1
        elif self.isin_closelist(node_temp):
            pass
        elif self.is_obstacle(node_temp):
            pass
        elif self.isin_openlist(node_temp) == 0:
            node_temp.father = node
            self.open_list.append(node_temp)
        else:
            if node_temp.f < (self.isin_openlist(node_temp)).f:
                self.open_list.remove(self.isin_openlist(node_temp))
                node_temp.father = node
                self.open_list.append(node_temp)

        ud = 1
        rl = -1
        node_temp = node.search_near(ud,rl) #在调用另一个类的方法时（不论是子类还是在类外定义的类），都要进行实例化才能调用函数
        if node_temp.point == end_point:
            return 1
        elif self.isin_closelist(node_temp):
            pass
        elif self.is_obstacle(node_temp):
            pass
        elif self.isin_openlist(node_temp) == 0:
            node_temp.father = node
            self.open_list.append(node_temp)
        else:
            if node_temp.f < (self.isin_openlist(node_temp)).f:
                self.open_list.remove(self.isin_openlist(node_temp))
                node_temp.father = node
                self.open_list.append(node_temp)

        ud = -1
        rl = 1
        node_temp = node.search_near(ud,rl) #在调用另一个类的方法时（不论是子类还是在类外定义的类），都要进行实例化才能调用函数
        if node_temp.point == end_point:
            return 1
        elif self.isin_closelist(node_temp):
            pass
        elif self.is_obstacle(node_temp):
            pass
        elif self.isin_openlist(node_temp) == 0:
            node_temp.father = node
            self.open_list.append(node_temp)
        else:
            if node_temp.f < (self.isin_openlist(node_temp)).f:
                self.open_list.remove(self.isin_openlist(node_temp))
                node_temp.father = node
                self.open_list.append(node_temp)

        ud = -1
        rl = -1
        node_temp = node.search_near(ud,rl) #在调用另一个类的方法时（不论是子类还是在类外定义的类），都要进行实例化才能调用函数
        if node_temp.point == end_point:
            return 1
        elif self.isin_closelist(node_temp):
            pass
        elif self.is_obstacle(node_temp):
            pass
        elif self.isin_openlist(node_temp) == 0:
            node_temp.father = node
            self.open_list.append(node_temp)
        else:
            if node_temp.f < (self.isin_openlist(node_temp)).f:
                self.open_list.remove(self.isin_openlist(node_temp))
                node_temp.father = node
                self.open_list.append(node_temp)

        return 0

##建图并设立障碍
ss=map_2d(10,20)
for i in range(10):
    ss.obstacle(4,i)
for i in range(19):
    ss.obstacle(0,i+1)
for i in range(9):
    ss.obstacle(i+1,0)
for i in range(9):
    ss.obstacle(i+1,19)
for i in range(19):
    ss.obstacle(9,i)
ss.obstacle(8,6)
ss.obstacle(6,8)
ss.obstacle(6,15)
ss.obstacle(9,10)
start_point = Point(1,3)
end_point = Point(9,2)
ss.end_draw(end_point)
ss.end_draw(start_point)
import copy
# ss2用于画最优解.
ss2=copy.deepcopy(ss)  # 注意这个地方因为是对象所以要重新开内存来赋值才避免冲突.
#初始化设置A*
a_star = A_star(start_point,end_point,ss)
start_node = a_star.Node(start_point,end_point,0)
a_star.open_list.append(start_node)

flag=0 #到达终点的标志位
m=0 #步数统计

#进入循环
while  flag != 1 :
    a_star.current = a_star.select_current()#从openlist中选取一个node
    flag=a_star.near_explore(a_star.current)#对选中的node进行周边探索
    m=m+1
    print(m)

#画出地图路径
for node_path in a_star.path:
    ss.end_draw(node_path.point)
ss.map_show()

print("上面打印的地图里面的6只是表示所有探索过的位置,而不是真正最优解走的路径.")



print("下面打印最优解:")



endNode=a_star.open_list[-1]
save=[]
tmp=endNode
while tmp.father!=None:
    ss2.end_draw(tmp.point)
    tmp=tmp.father
ss2.map_show()