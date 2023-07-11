import pygame,math,random,sys,os,copy
import PyUI as pyui
pygame.init()
screenw = 800
screenh = 600
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
pygame.display.set_caption('Make it happen')
pygame.scrap.init()
ui = pyui.UI()
done = False
clock = pygame.time.Clock()
ui.defaultcol = (50,120,150)
ui.defaulttextcol = (220,220,240)
basecol = (63,65,75)
##basecol = (140,150,170)

class funcmn:
    def __init__(self,param,main):
        self.func = lambda: main.moredetailmenu(param)
class funcem:
    def __init__(self,param,main):
        self.func = lambda: main.editmenu(param)

class notsql:
    def load():
        if not os.path.isfile(pyui.resourcepath('userdata.csv')):
            keys = list(completedata({}))
            st = ''
            for a in keys:
                st+=a+','
            st = st.removesuffix(',')
            with open(pyui.resourcepath('userdata.csv'),'w') as f:
                f.write(st)
        with open(pyui.resourcepath('userdata.csv'),'r') as f:
            lines = f.readlines()
        for a in range(len(lines)):
            lines[a] = lines[a].removesuffix('\n')
        keys = lines[0].split(',')
        del lines[0]
        data = []
        for a in lines:
            data.append({})
            spl = a.split(',')
            for i,b in enumerate(spl):
                if keys[i] == 'ID': data[-1][keys[i]] = int(b)
                else: data[-1][keys[i]] = b
        for a in range(len(data)):
            data[a] = completedata(data[a])
        data.sort(key=lambda x: x['ID'])
        return data
    def store(data,name='userdata'):
        with open(pyui.resourcepath(f'{name}.csv'),'w') as f:
            keys = list(completedata({}))
            st = ''
            for a in keys:
                st+=a+','
            st = st.removesuffix(',')
            f.write(st+'\n')
            for a in data:
                st = ''
                for k in keys:
                    st+=str(a[k])+','
                st = st.removesuffix(',')
                f.write(st+'\n')
        
        
                



def completedata(data):
    allitems = ['Forename','Surname','Pronouns','Title','Birth Date','Address','Postcode','Home Telephone','Work Telephone','Mobile Number',
                'Email','Driving License','Owns Vehicle','Interested in volunteer driving','Days can work','Hours available per day',
                'Times unable to complete work','Disability?','Emergency Contacts','Special Needs','Date Started','Active','Staff','ID']
    processed = {}
    for a in allitems:
        if not(a in data):
            if a == 'ID':
                processed[a] = -1
            else:
                processed[a] = ''
        else:
            processed[a] = data[a]
    return processed

def searchdata(data,searchterm):
    datacopied = copy.deepcopy(data)
    ndata = []
    for a in datacopied:
        a['name'] = a['Forename']+' '+a['Surname']
        for b in searchterm[1]:
            if searchterm[0].lower() in a[b].lower():
                ndata.append(a)
                break
    return ndata

     

class ITEM:
    def __init__(self,data,main):
        self.data = data
        self.menu = 'info'+str(self.data['ID'])
        
        self.makegui(main)
    def makegui(self,main):
        ## main
        ui.maketext(10,25,'Data for '+self.data['Forename'],40,self.menu,self.menu+'title',backingcol=basecol,objanchor=(0,'h/2'),scalesize=False,layer=3)
        ui.makebutton(-8,25,'Back',30,ui.menuback,self.menu,ID=self.menu+'back',anchor=('w',0),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalesize=False,layer=3,col=basecol)
        ui.makebutton(-78,25,'Delete User',30,main.deluser,self.menu,ID=self.menu+'del',anchor=('w',0),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalesize=False,layer=3,col=basecol)
        ui.makerect(0,0,screenw,50,menu=self.menu,layer=2,scalesize=False,col=(83,86,100),ID=self.menu+'rect')
        ui.makerect(0,50,screenw,4,menu=self.menu,layer=2,scalesize=False,col=(80,150,160),ID=self.menu+'rect2')
        ui.maketable(0,0,[],[ui.maketext(0,0,'Item',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True),
                             ui.maketext(0,0,'Info',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True),
                             ui.maketext(0,0,'Edit',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True)],self.menu,self.menu+'table',roundedcorners=4,textcenter=False,verticalspacing=4,textsize=30,boxwidth=[200,200,100],anchor=(10,60),col=basecol,scalesize=False,scalex=False,scaley=False)
        ui.makescroller(0,0,screenh-60,self.slidetable,pageheight=screenh-60,anchor=('w',60),objanchor=('w',0),scalesize=False,menu=self.menu,ID=self.menu+'scroller',runcommandat=1,layer=0)
        self.refreshtable()

        ## edit menu
        ui.makewindowedmenu(10,10,400,140,self.menu+'edit',self.menu,basecol,roundedcorners=8,scalesize=False,scalex=False,scaley=False,ID=self.menu+'window')
        ui.maketable(5,5,[['Item',ui.maketextbox(0,0,'',200,2,self.menu+'edit',roundedcorners=4,height=80,textsize=30,verticalspacing=4)]],menu=self.menu+'edit',roundedcorners=4,boxwidth=[184,200],boxheight=80,textsize=35,scalesize=False,scalex=False,scaley=False,col=basecol,ID=self.menu+'editbox')
        ui.makebutton(200,115,'Save',40,self.saveedited,self.menu+'edit',scalesize=False,scalex=False,scaley=False,roundedcorners=10,verticalspacing=3,center=True,ID=self.menu+'save')
    def refreshtable(self):
        ui.IDs[self.menu+'table'].wipe(ui,False)
        data = []
        for a in self.data:
            if a == 'ID':
                obj = ''
            else:
                func = funcem(a,self)
                obj = ui.makebutton(0,0,'{dots}',30,func.func,roundedcorners=4,clickdownsize=2)
            data.append([str(a),str(self.data[a]),obj])
        ui.IDs[self.menu+'table'].data = data
        sc = ui.IDs[self.menu+'scroller']
        if (sc.maxp-sc.minp)>sc.pageheight: ui.IDs[self.menu+'table'].boxwidth = [(screenw-126-15)/2,(screenw-126-15)/2,100]
        else: ui.IDs[self.menu+'table'].boxwidth = [(screenw-126)/2,(screenw-126)/2,100]
        ui.IDs[self.menu+'table'].refresh(ui)
        ui.IDs[self.menu+'title'].text = f'Data for {self.data["Forename"]} {self.data["Surname"]}'
        ui.IDs[self.menu+'title'].refresh(ui)
        self.slidetable()
        self.reshiftgui()
    def slidetable(self):
        ui.IDs[self.menu+'table'].y = 60-ui.IDs[self.menu+'scroller'].scroll
        ui.IDs[self.menu+'table'].refreshcords(ui)
    def reshiftgui(self):
        ui.IDs[self.menu+'rect'].width = screenw
        ui.IDs[self.menu+'rect2'].width = screenw
        ui.IDs[self.menu+'scroller'].scroll = 0
        ui.IDs[self.menu+'scroller'].height = screenh-60
        ui.IDs[self.menu+'scroller'].pageheight = screenh-60
        ui.IDs[self.menu+'scroller'].maxp = ui.IDs[self.menu+'table'].height
        ui.IDs[self.menu+'scroller'].refresh(ui)
        if self.menu+'window' in ui.IDs:
            ui.IDs[self.menu+'editbox'].boxwidth = [184,screenw-36-184]
            ui.IDs[self.menu+'window'].width = screenw-10
    def editmenu(self,item):
        self.selected = item
        ui.IDs[self.menu+'editbox'].wipe(ui,True)
        ui.IDs[self.menu+'editbox'].data = [[item,ui.maketextbox(0,0,str(self.data[item]),200,2,self.menu+'edit',roundedcorners=4,height=80,textsize=30,verticalspacing=4,command=self.saveedited,commandifenter=True)]]
        ui.IDs[self.menu+'editbox'].refresh(ui)
        ui.IDs[self.menu+'editbox'].refreshcords(ui)
        ui.IDs[self.menu+'table'].refreshcords(ui)
        ui.IDs[self.menu+'editbox'].tableimages[0][1][1].selected = True
        ui.selectedtextbox = ui.textboxes.index(ui.IDs[self.menu+'editbox'].tableimages[0][1][1])
        ui.movemenu(self.menu+'edit','down')
    def saveedited(self):
        self.data[self.selected] = ui.IDs[self.menu+'editbox'].data[0][1].text
        main.refreshdata()
        self.refreshtable()
        ui.menuback()
    def wipe(self):
        items = ['title','back','del','table','scroller','editbox','save','rect','rect2','window']
        for a in items:
             ui.delete(self.menu+a,False)

class MAIN:
    def __init__(self): 
        self.data = notsql.load()
        self.searchterm = ['',['name']]
        self.data = notsql.load()

        self.menus = []
        self.generatemenus()
        self.makegui()
    def makegui(self):
        ## title screen
        ui.maketext(0,0,'',250,anchor=('w/2','0'),objanchor=('w/2','0'),img=pygame.image.load(pyui.resourcepath('make it happen.png')),colorkey=(251,251,251))
        ui.makebutton(0,270,'Users',50,lambda: ui.movemenu('table','up'),roundedcorners=10,clickdownsize=2,verticalspacing=4,anchor=('w/2','0'),objanchor=('w/2',0))
        ui.makebutton(0,330,'Add User',50,self.adduser,anchor=('w/2','0'),objanchor=('w/2',0),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalex=False,scaley=False)
        
        
        ## main table
        ui.maketable(0,0,[],['ID','Name','More'],anchor=(10,60),boxwidth=[100,300,100],verticalspacing=5,textsize=30,roundedcorners=4,col=basecol,ID='main table',menu='table',scalesize=False)
        ui.makescroller(0,0,screenh-60,self.slidetable,pageheight=screenh-60,anchor=('w',60),objanchor=('w',0),scalesize=False,menu='table',ID='main scroller',runcommandat=1,layer=0)
        self.refreshtable()

        ## search bar
        ui.makerect(0,50,screenw,4,menu='table',layer=2,col=(80,150,160),scalesize=False,ID='tabletoprect1')
        ui.makerect(0,0,screenw,50,menu='table',layer=2,col=(83,86,100),scalesize=False,ID='tabletoprect2')
        ui.maketext(13,26,'Search',30,'table',scalesize=False,layer=4,objanchor=(0,'h/2'),backingcol=pyui.shiftcolor(basecol,-20))
        ui.makebutton(-46,25,'{search}',18,menu='table',scalesize=False,objanchor=(0,'h/2'),anchor=('(w-100)/2',0),layer=4,spacing=2,clickdownsize=1,roundedcorners=9,col=basecol,borderdraw=False,hovercol=pyui.shiftcolor(basecol,-4),command=self.searchitem)
        ui.makebutton(-20,25,'{cross}',16,menu='table',scalesize=False,objanchor=(0,'h/2'),anchor=('(w-100)/2',0),layer=4,spacing=2,clickdownsize=1,roundedcorners=9,col=basecol,borderdraw=False,hovercol=pyui.shiftcolor(basecol,-4),command=self.clearsearchitem,width=30,height=30,textoffsetx=1,textoffsety=1)
        ui.maketextbox(10,10,'',(screenw-100)/2,menu='table',commandifenter=True,height=30,scalesize=False,textsize=28,verticalspacing=2,roundedcorners=5,col=basecol,layer=3,borderdraw=True,leftborder=80,rightborder=56,ID='search bar',command=self.searchitem)
        ui.makebutton(-80,25,'Add User',30,self.adduser,anchor=('w','0'),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalesize=False,col=basecol,menu='table',layer=3)
        ui.makebutton(-10,25,'Back',30,ui.menuback,anchor=('w','0'),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalesize=False,col=basecol,menu='table',layer=3)


        ## add user menu
        self.empty = completedata({})
        self.shiftingitems = []
        yinc = 70
        self.checkboxes = {'Pronouns':['She/Her','He/Him','They/Them','textbox'],'Driving license':['Yes','No'],'Owns Vehicle':['Yes','No'],'Interested in volunteer driving':['Yes','No'],'Disability?':['Yes','No'],'Staff':['Yes','No'],'Emergency Contacts':['button']}
        for i,a in enumerate(self.empty):
            if a != 'ID':
                ui.maketext(30,yinc,a,35,'add user',ID='add user'+a,maxwidth=200,backingcol=basecol)
                h = ui.IDs['add user'+a].height
                if a in self.checkboxes:
                    xinc = 240
                    disper = 540/len(self.checkboxes[a])
                    exclusive = ['add user checkbox'+a+'*'+b for b in self.checkboxes[a] if b!='textbox']
                    for b in self.checkboxes[a]:
                        if not(b in ['textbox','button']):
                            ui.maketext(xinc,yinc+h/2,b,30,'add user',ID='add user'+a+'*'+b,objanchor=(0,'h/2'))
                            xinc+=ui.IDs['add user'+a+'*'+b].width+10
                            ui.makecheckbox(xinc,yinc+h/2,40,menu='add user',ID='add user checkbox'+a+'*'+b,objanchor=(0,'h/2'),spacing=-8,clickdownsize=2,toggle=False,bindtoggle=exclusive)
                            if a == 'Pronouns': xinc+=ui.IDs['add user checkbox'+a+'*'+b].width+10
                            else: xinc+=ui.IDs['add user checkbox'+a+'*'+b].width+40
                            ui.IDs['add user checkbox'+a+'*'+b].storeddata = b
                            self.shiftingitems.append('add user'+a+'*'+b)
                            self.shiftingitems.append('add user checkbox'+a+'*'+b)
                        elif b == 'textbox':
                            ui.maketextbox(xinc,yinc,'',133,height=h,menu='add user',ID='add user inp'+a+'*'+b,textsize=32)
                            self.shiftingitems.append('add user inp'+a+'*'+b)
                        elif b == 'button':
                            ui.makebutton(xinc,yinc,'Add Emergency Contact',32,command=lambda: ui.movemenu('add contact','down'),width=200,height=h,menu='add user',ID='add user button'+a+'*'+b,roundedcorners=6,clickdownsize=2)
                            self.shiftingitems.append('add user button'+a+'*'+b)
                else:
                    ui.maketextbox(240,yinc,'',540,height=h,menu='add user',ID='add user inp'+a,textsize=32,spacing=1)
                    self.shiftingitems.append('add user inp'+a)
                self.shiftingitems.append('add user'+a)
                yinc+=h+15
        ui.makescroller(0,0,screenh-54,self.shiftaddmenu,maxp=yinc,pageheight=screenh,anchor=('w','h'),objanchor=('w','h'),ID='add menu scroller',menu='add user',runcommandat=1,scalesize=False)
        ui.maketext(10,25,'New User',40,'add user',textcol=(240,240,240),layer=3,backingcol=pyui.shiftcolor(basecol,20),centery=True)
        ui.makerect(0,50,screenw,4,menu='add user',layer=2,col=(80,150,160))
        ui.makerect(0,0,screenw,50,menu='add user',layer=2,col=(83,86,100))
        ui.makerect(0,-1000,screenw,1000,menu='add user',layer=2,col=basecol)
        ui.makebutton(-148,25,'Clear',30,self.clearuser,anchor=('w','0'),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,col=basecol,menu='add user',layer=3)
        ui.makebutton(-78,25,'Save',30,self.saveuser,anchor=('w','0'),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,col=basecol,menu='add user',layer=3)
        ui.makebutton(-8,25,'Back',30,ui.menuback,anchor=('w','0'),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,col=basecol,menu='add user',layer=3)

        for a in self.shiftingitems:
            ui.IDs[a].truestarty = ui.IDs[a].starty

        ## emergency contacts
        ui.makewindowedmenu(60,60,680,300,'add contact','add user',basecol,roundedcorners=10,scaley=True)
        ui.maketext(340,10,'Add Emergency Contact',40,'add contact',backingcol=basecol,objanchor=('w/2',0))

        ui.maketext(10,55,'Name',34,'add contact',backingcol=basecol)
        ui.maketextbox(90,55,'',570,1,'add contact',textsize=32)
        
    def generatemenus(self):
        for a in self.menus:
            a.wipe()
        self.menus = []
        for a in self.data:
            self.menus.append(ITEM(a,self))
            
    def refreshtable(self):
        displaydata = searchdata(self.data,self.searchterm)
        
        ui.IDs['main table'].wipe(ui,False)
        data = []
        for a in range(len(displaydata)):
            func = funcmn(displaydata[a]['ID'],self)
            obj = ui.makebutton(0,0,'{dots}',30,func.func,roundedcorners=4,clickdownsize=2)
            data.append([displaydata[a]['ID'],displaydata[a]['Forename']+' '+displaydata[a]['Surname'],obj])

        sc = ui.IDs['main scroller']
        if (sc.maxp-sc.minp)>sc.pageheight:
            ui.IDs['main table'].boxwidth = [100,(screenw-8-20-200-15),100]
            print('shorter')
        else: ui.IDs['main table'].boxwidth = [100,(screenw-8-20-200),100]
        
        ui.IDs['main table'].data = data
        ui.IDs['main table'].refresh(ui)
    def slidetable(self):
        ui.IDs['main table'].y = 60-ui.IDs['main scroller'].scroll
        ui.IDs['main table'].refreshcords(ui)
    def moredetailmenu(self,ID):
        self.menuin = ID-1
        self.menus[self.menuin].reshiftgui()
        self.menus[self.menuin].refreshtable()
        ui.movemenu('info'+str(ID),'left')
    def refreshdata(self):
        self.data = []
        for a in self.menus:
            self.data.append(a.data)
        notsql.store(self.data)
        self.refreshtable()
    def adduser(self):
        ui.movemenu('add user','up')
    def clearuser(self):
        for a in self.shiftingitems:
            if type(ui.IDs[a]) == pyui.TEXTBOX:
                ui.IDs[a].text = ''
                ui.IDs[a].refresh(ui)
            elif type(ui.IDs[a]) == pyui.BUTTON:
                ui.IDs[a].toggle = False
    def saveuser(self):
        data = {'ID':len(self.data)+1}
        empty = completedata({})
        for a in self.shiftingitems:
            if type(ui.IDs[a]) == pyui.TEXTBOX:
                temp = a.removeprefix('add user inp')
                if '*' in temp:
                    data[temp.split('*')[0]] = ui.IDs[a].text
                elif temp in list(empty):
                    data[temp] = ui.IDs[a].text
        for a in self.shiftingitems:
            if type(ui.IDs[a]) == pyui.BUTTON:
                temp = a.removeprefix('add user checkbox')
                items = temp.split('*')
                if ui.IDs[a].toggle:
                    data[items[0]] = ui.IDs[a].storeddata
                
                
        self.data.append(completedata(data))
        notsql.store(self.data)
        self.refreshtable()
        self.menus.append(ITEM(completedata(data),self))
        ui.menuback()
    def deluser(self):
        notsql.store(self.data,'backup')
        for a in ui.animations:
            a.finish(ui,True)
        ui.animations = []
        self.data.remove(self.menus[self.menuin].data)
        self.menus[self.menuin].wipe()
        del self.menus[self.menuin]
        self.data.sort(key=lambda x: x['ID'])
        for a in range(len(self.data)):
            self.data[a]['ID'] = a+1
        notsql.store(self.data)
        self.generatemenus()
        
        self.refreshtable()
        ui.activemenu = 'table'
        self.menuin = -1
        
    def searchitem(self):
        self.searchterm = [ui.IDs['search bar'].text,['name']]
        self.refreshtable()
    def clearsearchitem(self):
        ui.IDs['search bar'].text = ''
        ui.IDs['search bar'].refresh(ui)
        self.searchitem()
        
    def shiftaddmenu(self):
        for a in self.shiftingitems:
            ui.IDs[a].y = ui.IDs[a].truestarty-ui.IDs[a].objanchor[1]-ui.IDs['add menu scroller'].scroll
            ui.IDs[a].refreshcords(ui)
    def reshiftgui(self):
        ui.IDs['search bar'].width = (screenw-100)/2
        ui.IDs['search bar'].refresh(ui)
        ui.IDs['tabletoprect1'].width = screenw
        ui.IDs['tabletoprect2'].width = screenw
        ui.IDs['add menu scroller'].height = screenh-54*ui.scale
        ui.IDs['add menu scroller'].pageheight = screenh/ui.scale
        ui.IDs['add menu scroller'].refresh(ui)
        ui.IDs['add menu scroller'].resetcords(ui)
        ui.IDs['main scroller'].scroll = 0
        ui.IDs['main scroller'].height = screenh-60
        ui.IDs['main scroller'].pageheight = screenh-60
        ui.IDs['main scroller'].maxp = ui.IDs['main table'].height
        ui.IDs['main scroller'].refresh(ui)
        ui.IDs['main table'].boxwidth = [100,(screenw-8-20-200),100]
        self.refreshtable()
        
main = MAIN()


while not done:
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            screenw = event.w
            screenh = event.h
            main.reshiftgui()
            if 'info' in ui.activemenu:
                main.menus[main.menuin].reshiftgui()
                main.menus[main.menuin].refreshtable()
    screen.fill(basecol)
    ui.rendergui(screen)
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit() 
