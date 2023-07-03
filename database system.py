import pygame,math,random,sys,os
import PyUI as pyui
pygame.init()
screenw = 800
screenh = 600
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
pygame.scrap.init()
ui = pyui.UI()
done = False
clock = pygame.time.Clock()
ui.defaultcol = (50,120,150)
ui.defaulttextcol = (220,220,240)

class funcmn:
    def __init__(self,param,main):
        self.func = lambda: main.moredetailmenu(param)
class funcem:
    def __init__(self,param,main):
        self.func = lambda: main.editmenu(param)

class ITEM:
    def __init__(self,data):
        self.data = data
        self.menu = 'info'+str(self.data['ID'])
        self.makegui()
    def makegui(self):
        ## main
        ui.maketext(10,10,'Data for '+self.data['name'],80,self.menu,self.menu+'title',backingcol=(63,64,75),scalesize=False)
        ui.makebutton(0,0,'back',40,ui.menuback,self.menu,ID=self.menu+'back',anchor=('w-10',10),objanchor=('w',0),roundedcorners=4,scalesize=False)
        ui.maketable(0,0,[],[ui.maketext(0,0,'Item',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True),
                             ui.maketext(0,0,'Menu',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True),
                             ui.maketext(0,0,'Edit',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True)],self.menu,self.menu+'table',roundedcorners=4,textcenter=False,verticalspacing=4,textsize=30,boxwidth=[200,200,100],anchor=(10,80),col=(63,64,75))
        self.refreshtable()

        ## edit menu
        ui.makewindowedmenu(10,10,300,120,self.menu+'edit',self.menu,(63,64,75),roundedcorners=8,scalesize=False,scalex=False,scaley=False)
        ui.maketable(5,5,[['Item',ui.maketextbox(0,0,'',200,2,self.menu+'edit',roundedcorners=4,height=60,textsize=30)]],menu=self.menu+'edit',roundedcorners=4,boxwidth=[84,200],boxheight=60,textsize=35,scalesize=False,scalex=False,scaley=False,col=(63,64,75))
        ui.makebutton(150,95,'Save',40,self.saveedited,self.menu+'edit',scalesize=False,scalex=False,scaley=False,roundedcorners=10,verticalspacing=3,center=True)
    def refreshtable(self):
        ui.IDs[self.menu+'table'].wipe(ui,False)
        data = []
        for a in self.data:
            func = funcem(a,self)
            obj = ui.makebutton(0,0,'{dots}',30,func.func,roundedcorners=4,clickdownsize=2)
            data.append([a,self.data[a],obj])
        ui.IDs[self.menu+'table'].data = data
        ui.IDs[self.menu+'table'].refresh(ui)
        ui.IDs[self.menu+'table'].refreshcords(ui)
    def editmenu(self,item):
        ui.movemenu(self.menu+'edit','down')
    def saveedited(self):
        pass
    def wipe(self):
        items = ['title','back','table']
        for a in items:
            ui.delete(self.menu+a,False)

class MAIN:
    def __init__(self):
        self.data = [{'name':'chris','age':'17','ID':2},{'name':'ryan','age':'16','ID':1}]
        self.data.sort(key=lambda x: x['ID'])

        self.menus = []
        self.generatemenus()
        self.makegui()
    def makegui(self):
        ui.maketable(0,0,[],['ID','Name','Age','More'],anchor=(10,10),boxwidth=[70,180,100,100],verticalspacing=5,textsize=30,roundedcorners=4,col=(63,65,75),scalesize=False,ID='main table')
        self.refreshtable()
    def generatemenus(self):
        for a in self.menus:
            a.wipe()
        self.menus = []
        for a in self.data:
            self.menus.append(ITEM(a))
            
    def refreshtable(self):
        ui.IDs['main table'].wipe(ui,False)
        data = []
        for a in range(len(self.data)):
            func = funcmn(self.data[a]['ID'],self)
            obj = ui.makebutton(0,0,'{dots}',30,func.func,roundedcorners=4,clickdownsize=2)
            data.append([self.data[a]['ID'],self.data[a]['name'],self.data[a]['age'],obj])
        ui.IDs['main table'].data = data
        ui.IDs['main table'].refresh(ui)
        ui.IDs['main table'].refreshcords(ui)
    def moredetailmenu(self,ID):
        ui.movemenu('info'+str(ID),'left')
        
        
main = MAIN()


while not done:
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
##        if event.type == pygame.KEYDOWN:
##            if event.key == pygame.K_SPACE:
##                ui.sliders[0].slider+=1
##                ui.sliders[0].limitpos(ui)
    screen.fill((63,65,75))
    
    ui.rendergui(screen)
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit() 
