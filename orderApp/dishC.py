#coding:utf-8
from socket import AF_INET, SOCK_STREAM, socket
from optparse import OptionParser
from optparse import OptionGroup


class Item(object):

    def __init__(self, name):
        self.name = name

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

class FoodItem(Item):
    def __init__(self, name, dprice):
        super(FoodItem, self).__init__(name)
        self.dprice = dprice

    def getName(self):
        return self.name


    def getPrice(self):
        return self.dprice


class ToolItem(Item):
    def __init__(self, name, tprice):
        super(ToolItem, self).__init__(name)
        self.tprice = tprice

    def getPrice(self):
        return self.tprice


class Menu(object):
    def __init__(self):
        self.dishData = {}
        self.toolData = {}
        try:
            f = open('menu.txt')
            for line in f:
                l = line.split()
                self.dishData[l[0]] = FoodItem(l[0],l[1])
        except Exception as e:
            print e

    def hasItem(self, name):
        return name in self.dishData


    def getItem(self, name):
         return self.dishData.get(name)


    def getFoodItemItemPrice(self, name):
        return self.dishData[name].getPrice()

    def getToolItemPrice(self, name):
        return self.toolsData[name].getPrice()

class OrderedList(object):
    def __init__(self):
        self.orderList = {}

    def addOrderItem(self, orderItem):
        self.orderList[orderItem.getName()] = orderItem
        orderItem.setStatus(orderItem.ORDERING)


    def getOrderItem(self,name):
        return self.orderList.get(name)

    def placeOrderList(self):
        for name in self.orderList:
            orderItem = self.getOrderItem(name) 
            orderItem.setStatus(orderItem.PLACEORDER)

    
    def printOrderList(self):
        orderDict = {}
        for name in self.orderList:
             orderDict[name] = self.getOrderItem(name)
        return orderDict

    def printBill(self):
        self.printOrderList()
        total = 0
        for name in self.orderList:
            orderItem = self.getOrderItem(name)
            if orderItem.status == orderItem.PLACEORDER:
                total += orderItem.getfPrice()
        return total


        

class OrderItem(Item):
    ORDERING = '点菜中'
    PLACEORDER = '已下单'
    OUTOFFOOD = '出菜中'
    HASSERVED = '已上菜'
    CANCEL = '菜品被取消'
    NOORDER = '未点菜'
    def __init__(self, dishItem, fnum):
        self.dishItem = dishItem
        self.setStatus(self.NOORDER)   
        self.fnum = fnum

    
    def cancelOrder(self, fnum):
        if not fnum:
            self.setStatus(self.CANCEL)
        self.fnum -= fnum

    def setStatus(self, status_str):
        self.status = status_str

    def getName(self):
        return self.dishItem.getName()

    def getfPrice(self):
        return float(self.dishItem.getPrice())*self.getFnum()


    def getPrice(self):
        return float(self.dishItem.getPrice())

    def getFnum(self):
        return self.fnum

    def getStatus(self):
        return self.status

    def __str__(self):
        return '菜名: %s\t数量: %d\t单价: %.2f元\t状态: %s' % (self.getName(), self.getFnum(),  self.getPrice(), self.getStatus()) 

class Table(object):
    OPEN_TABLE = 'Open Table'
    CLOSE_TABLE = 'Close Table'
    def __init__(self, menu, pnum):
        self.menu = menu
        self.orderedList = OrderedList()
        self.pnum = pnum
        self.setStatus(self.CLOSE_TABLE)


    def getPnum(self):
        return self.pnum

    def setRnum(self, num):
        self.rnum = num

    def getRnum(self):
        return self.rnum
   

    def orderFoodItem(self, name, fnum):
        if self.getStatus() == self.OPEN_TABLE:
            temp = self.menu.getItem(name)
            if temp:
                orderItem = OrderItem(temp, fnum)
                self.orderedList.addOrderItem(orderItem)
                return '*'*20+'点菜完毕'+'*'*20
        else:
            return  '此桌还未开台.....'

    def openTable(self):
        self.setStatus(self.OPEN_TABLE)
        return 'Open Table number %s Success' %self.pnum

    def setStatus(self, status_str):
        self.status = status_str


    def getStatus(self):
        return self.status


    def placeOrder(self):
        self.orderedList.placeOrderList()
        self.orderedList.printOrderList()
        return  '%s号桌下单成功 !!!' % self.pnum


    def cancelOrder(self, name, fnum=0):
        orderItem = self.orderedList.getOrderItem(name)
        if orderItem:
            orderItem.cancelOrder(fnum)

    def checkOut(self):
        s = self.printBill()
        for name in self.orderedList.orderList:
            orderItem = self.orderedList.getOrderItem(name) 
            orderItem.setStatus(orderItem.NOORDER)
        self.setStatus(self.CLOSE_TABLE)
        return s
        

    def printBill(self):
        total = self.orderedList.printBill() + self.getRnum()*2
        print '餐具数: %d\t单价:%d' %(self.getRnum(), 2)
        return '%s号桌的消费为: %.2f元' %(self.getPnum(), total)

class InstructParser(object):
    OPENTAB = 'login'
    ORDER = 'order'
    PLACEORDER = 'placeorder'
    CANCELORDER = 'cancelorder'
    CHECKOUT = 'checkout'
    QUIT = 'quit'
    def __init__(self, severobj):
        self.createOptParse()
        self.sever = severobj

    def createOptParse(self):
        self.parse = OptionParser()
        self.parse.add_option("-t", type="string", dest="pnum",help="number of table.")
        group = OptionGroup(self.parse,'LoginOptions', 'Number of table after -t')
        group.add_option("-r", type="int", dest="rnum",help="number of people.")
        self.parse.add_option_group(group)
        group = OptionGroup(self.parse, 'OrderOptions', 'Number of table after -t') 
        group.add_option("-d", type="string",dest="dishname",help="dish name.")
        group.add_option("-f", type="int", dest="fnum",help="number of dish.")
        self.parse.add_option_group(group)
        group = OptionGroup(self.parse, 'PlaceOrderOptions', 'Number of table after -t')
        self.parse.add_option_group(group)
        group = OptionGroup(self.parse, 'CancelOrderOptions', 'Number of table after -t')
        group.add_option("--cd", type="string",dest="dishname",help="dish name.")
        group.add_option("--cf", type="int", dest="fnum",help="number of dish.")
        self.parse.add_option_group(group)
        group = OptionGroup(self.parse, 'CheckoutOptions', 'Number of table after -t')
        self.parse.add_option_group(group)
        group = OptionGroup(self.parse, 'QiutOptions', 'Quit this ordersystem!!!')
        self.parse.add_option_group(group)
    


    def parseInstruct(self, instruct):
            if instruct[0] == self.OPENTAB:
                (options, args) = self.parse.parse_args(instruct[1:])
                self.printCommand(instruct[0])
                table = self.sever.getTable(options.pnum)
                table.setRnum(options.rnum)
                return table.openTable()
            elif instruct[0] == self.ORDER:
                (options, args) = self.parse.parse_args(instruct[1:])
                self.printCommand(instruct[0])
                table = self.sever.getTable(options.pnum)
                return table.orderFoodItem(options.dishname, options.fnum)
            elif instruct[0] == self.PLACEORDER:
                (options, args) = self.parse.parse_args(instruct[1:])
                self.printCommand(instruct[0])
                table = self.sever.getTable(options.pnum)
                return table.placeOrder()
            elif instruct[0] == self.CANCELORDER:
                (options, args) = self.parse.parse_args(instruct[1:])
                self.printCommand(instruct[0])
                table = self.sever.getTable(options.pnum)
                table.cancelOrder(options.dishname, options.fnum)
                return  "你的菜品已经取消成功!!!"
            elif instruct[0] == self.CHECKOUT:
                (options, args) = self.parse.parse_args(instruct[1:])
                self.printCommand(instruct[0])
                table = self.sever.getTable(options.pnum)
                return table.checkOut()
            elif instruct[0] == self.QUIT:
                return '退出系统!!!'


    def printCommand(self, command):
        print '*'*20+command+'*'*20


class Server(object):
    def __init__(self):
        self.initTable()
        self.printSys()


    def initTable(self):
        menu = Menu()
        self.tableDict = {}
        f = open('table.conf')
        for line in f:
            l = line.split()
            if l[0] == '散桌':
                num = int(l[1])
                for i in xrange(num):
                    self.tableDict[str(i+1)] = Table(menu, str(i+1))  
            else:
                self.tableDict[l[0]] = Table(menu, l[0])


    def printSys(self):
        print '\n\n\n\n\n'+'*'*40+'欢迎进入点菜系统'+'*'*40+'\n\n\n\n\n\n'


    def getTable(self, pnum):
        try:
            if pnum in self.tableDict:
                return self.tableDict[pnum] 
        except Exception as e:
            print 'Exception:', e
