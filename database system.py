import pygame,math,random,sys,os,copy,time
import PyUI as pyui
pygame.init()
screenw = 800
screenh = 600

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

logo = pygame.image.load(resource_path('images\\make it happen white small.png'))
logo.set_colorkey((255,255,255))
pygame.display.set_icon(logo)
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
pygame.display.set_caption('Make it happen')
pygame.scrap.init()
ui = pyui.UI()
done = False
clock = pygame.time.Clock()
ui.defaultcol = (50,120,150)
ui.defaulttextcol = (220,220,240)
basecol = (63,65,75)
##ui.defaultanimationspeed = 2
##basecol = (140,150,170)


class funcmn:
    def __init__(self,param,main):
        self.func = lambda: main.moredetailmenu(param)
class funcem:
    def __init__(self,param,main):
        self.func = lambda: main.editmenu(param)
class funcec:
    def __init__(self,param):
        self.func = lambda: main.editcontact(param)
class funcdc:
    def __init__(self,param):
        self.func = lambda: main.deletecontact(param)
class funcef:
    def __init__(self,param,form):
        self.func = lambda: form.edititem(param)
class funcdf:
    def __init__(self,param,form):
        self.func = lambda: form.deleteitem(param)

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
                b = b.replace('`',',')
                if keys[i] == 'ID': data[-1][keys[i]] = int(b)
                elif keys[i] in ['Emergency Contacts','Expenses','Mileage']:
                    exec('emergencycontactexecvalue='+b,globals())
                    if b == 'Emergency Contacts':
                        data[-1][keys[i]] = [completecontactdata(e) for e in emergencycontactexecvalue]
                    else: data[-1][keys[i]] = emergencycontactexecvalue
                else: data[-1][keys[i]] = b
        for a in range(len(data)):
            data[a] = completedata(data[a])
        data.sort(key=lambda x: x['ID'])
        return data
    def store(data,name='userdata'):
        data = copy.deepcopy(data)
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
                    if type(a[k]) == str or type(a[k]) == list:
                        a[k] = str(a[k]).replace(',','`')
                    st+=str(a[k])+','
                st = st.removesuffix(',')
                f.write(st+'\n')
        
      
def datetoday(date):
    t = 0
    date = date.lower()
    try:
        splitters = '\/.,-~":;'
        rem = 'qwertyuiopasdfghjklzxcvbnm'
        for a in rem:
            date = date.replace(a,'')
        for a in splitters:
            date = date.replace(a,'/')
        spl = date.split('/')
        if len(spl[2]) == 1:
            spl[2] = '0'+spl[2]
        if len(spl[2]) == 2:
            if int(spl[2])<35: spl[2] = '20'+spl[2]
            else: spl[2] = '19'+spl[2]
        t+=int(spl[0])
        t+=int(spl[1])*31
        t+=int(spl[2])*365.25
        return t
    except Exception as e:
        return t

def gettoday(adjust=0):
    now = time.time()
    adjusted = now-adjust*24*60*60
    day = int(time.ctime(adjusted).split()[2])
    t = time.localtime()
    year = t.tm_year
    month = t.tm_mon
    if day<int(time.ctime(now).split()[2]) and adjust<0:
        month+=1
    elif day>int(time.ctime(now).split()[2]) and adjust>0:
        month-=1
    return f'{day}/{month}/{year}'

def autodate(text):
    text = text.lower()
    num = ''
    if text in ['0','today','now','']: num = 0
    elif text in ['yesterday']: num = 1
    elif text in ['tomorrow']: num = -1
    else:
        try: num = int(text)
        except: pass
    if num != '':
        text = gettoday(num)
    return text

def filternums(text):
    nums = '0123456789'
    ntext = ''
    for a in text:
        if a in nums:
            ntext+=a
    if ntext == '': out = 0
    else: out = int(ntext)
    return out

def completedata(data):
    allitems = ['Forename','Surname','Pronouns','Title','Birth Date','Ethnicity','Address','Postcode','Home Telephone','Work Telephone','Mobile Number',
                'Email','Qualifications','Driving License','Owns Vehicle and has Relevant Documents','Interested in volunteer driving','Days can work','Hours available per day',
                'Times unable to complete work','Disability?','Emergency Contacts','Reasonable Adjustments','Date Started','Active','Staff','ID','Expenses','Mileage']
    processed = {}
    for a in allitems:
        if not(a in data):
            if a == 'ID':
                processed[a] = -1
            elif a in ['Emergency Contacts','Expenses','Mileage']:
                processed[a] = []
            else:
                processed[a] = ''
        else:
            processed[a] = data[a]
    return processed

def completecontactdata(data={}):
    allitems = ['Name','Address','Home Number','Mobile Number','Relationship']
    processed = {}
    for a in allitems:
        if not (a in data):
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

def dataoutput(data,item):
    output = {}
    for i,a in enumerate(data):
        info = a[item]
        if item in ['Postcode']:
            for a in main.menus[i].menus['Postcode'].checkboxes:
                if main.menus[i].menus['Postcode'].checkboxes[a].toggle:
                    info = a
        if item == 'Birth Date':
            if datetoday(a[item])!=0:
                info = int(datetoday(gettoday())/365.25-datetoday(a[item])/365.25)
            else:
                info = 'No Data'
        if not(info in output):
           output[info] = 0
        output[info]+=1
    with open('data.txt','w') as f:
        for a in output:
            if a == '': b = 'No Data'
            else: b = a
            f.write(f'{b} - {output[a]}\n')
            

class dummytextbox:
    def __init__(self,text):
        self.text = text
        self.enabled = False
    def refresh(self,ui):
        pass

class FORM:
    def __init__(self,typ,data,menu,master):
        self.typ = typ
        self.menu = menu
        self.unqmenu = menu+typ
        self.data = data
        self.master = master
        self.scroller = 0
        if self.typ == 'Expenses': self.fields = ['Date','Hours','Pay','Alternative']
        else: self.fields = ['Date','Start Mileage','Collecting From','Number of Trays','Taken to','Close Mileage','Total Trip Mileage']
        self.makegui()
    def makegui(self):
        ## list menu
        ui.makewindowedmenu(0,0,589,340,self.unqmenu+'list',self.menu,basecol,roundedcorners=10,scaley=True,ID=self.unqmenu+'list window',center=True,anchor=('w/2','h/2'))
        if self.typ == 'Expenses': xpos = -214
        else: xpos = -333
        ui.makebutton(xpos,25,self.typ,30,lambda: ui.movemenu(self.unqmenu+'list','down'),self.menu,anchor=('w',0),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalesize=False,layer=3,col=basecol,ID=self.unqmenu+'button')

        if self.typ == 'Expenses': self.table = ui.maketable(10,10,[],['Date','Hours','Pay','',''],self.unqmenu+'list',boxwidth=[150,150,150,80,27],boxheight=27,verticalspacing=5,textsize=30,roundedcorners=4,col=basecol,ID=self.unqmenu+'list')
        else: self.table = ui.maketable(10,10,[],['Date','Mileage','',''],self.unqmenu+'list',boxwidth=[226,226,80,27],boxheight=27,verticalspacing=4,textsize=30,roundedcorners=4,col=basecol,ID=self.unqmenu+'list')
        self.refreshtable()
        
        ui.makebutton(12,12,'+',40,self.additem,self.unqmenu+'list',col=basecol,roundedcorners=4,clickdownsize=1,border=2,layer=2,width=27,height=27,textoffsety=-2,textoffsetx=1,ID=self.unqmenu+'add button')
        self.scroller = ui.makescroller(584,10,320,self.shifttable,maxp=self.table.height,pageheight=320,menu=self.unqmenu+'list',runcommandat=1,col=pyui.shiftcolor(basecol,30),roundedcorners=3)
        
        ## edit menu
        spread = 50
        if self.typ == 'Mileage': spread = 40
        ui.makewindowedmenu(0,0,590,86+spread*(len(self.fields)-1)+50,self.unqmenu+'edit',self.menu,basecol,roundedcorners=10,scaley=True,ID=self.menu+'edit window',center=True,anchor=('w/2','h/2'))
        ui.maketext(295,5,'Enter '+self.typ,40,self.unqmenu+'edit',self.unqmenu+'edit title',backingcol=basecol,objanchor=('w/2',0))
        yinc = 45
        xinc = 210
        if self.typ == 'Expenses': xinc = 160
        self.textboxes = {}
        for a in self.fields:
            ui.maketext(10,yinc,a,34,self.unqmenu+'edit',backingcol=basecol)
            self.textboxes[a] = ui.maketextbox(xinc,yinc,'',580-xinc,menu=self.unqmenu+'edit',textsize=32,ID=self.unqmenu+a)
            yinc+=spread
        if self.typ == 'Mileage': yinc += 10
        ui.makebutton(375,yinc-8,'Save',34,self.save,self.unqmenu+'edit',objanchor=('w/2',0),verticalspacing=4,roundedcorners=5,clickdownsize=2)
        ui.makebutton(215,yinc-8,'Clear',34,self.clear,self.unqmenu+'edit',objanchor=('w/2',0),verticalspacing=4,roundedcorners=5,clickdownsize=2)

    def refreshtable(self):
        self.data.sort(key=lambda x:datetoday(x['Date']),reverse=True)
        data = []
        self.table.wipe(ui,False)
        self.table.boxheight = 27
        for i,a in enumerate(self.data):
            func = funcef(i,self)
            editbutton = ui.makebutton(0,0,'{dots}',30,func.func,self.unqmenu+'edit',roundedcorners=4,col=basecol,clickdownsize=1)
            func = funcdf(i,self)
            crossbutton = ui.makebutton(0,0,'{cross}',17,func.func,self.unqmenu+'edit',roundedcorners=4,col=basecol,clickdownsize=1,textoffsetx=1,textoffsety=1)
            if self.typ == 'Expenses': data.append([a['Date'],a['Hours'],a['Pay'],editbutton,crossbutton])
            else: data.append([a['Date'],a['Total Trip Mileage'],editbutton,crossbutton])
        self.table.data = data
        self.table.refresh(ui)
        if self.scroller != 0:
            self.scroller.maxp = self.table.height
            self.scroller.refresh(ui)
            self.scroller.limitpos(ui)
        if self.table.height<320:
            ui.IDs[self.unqmenu+'list window'].width = 589
        else:
            ui.IDs[self.unqmenu+'list window'].width = 604

    def shifttable(self):
        ui.IDs[self.unqmenu+'add button'].y = 12-self.scroller.scroll
        self.table.y = 10-self.scroller.scroll
        self.table.refreshcords(ui)
    
    def additem(self):
        self.clear()
        ui.movemenu(self.unqmenu+'edit','down')
        self.editing = -1
    def edititem(self,index):
        ui.movemenu(self.unqmenu+'edit','down')
        for a in self.textboxes:
            self.textboxes[a].text = self.data[index][a]
            self.textboxes[a].refresh(ui)
        self.editing = index
    def deleteitem(self,index):
        del self.data[index]
        self.refreshtable()
        self.master.data[self.typ] = self.data
        notsql.store(main.data)
        
    def clear(self):
        for a in self.textboxes:
            self.textboxes[a].text = ''
            self.textboxes[a].refresh(ui)
    def save(self):
        info = {}
        for a in self.textboxes:
            info[a] = self.textboxes[a].text
        if self.editing == -1:
            self.data.append(info)
        else:
            self.data[self.editing] = info
        self.refreshtable()
        self.master.data[self.typ] = self.data
##        self.master.refreshtable()
        notsql.store(main.data)
        ui.menuback()
    def enterdown(self,dirr):
        ui.activemenu == self.unqmenu+'edit'
        lis = list(self.textboxes)
        for a in self.textboxes:
            if self.textboxes[a].selected:
                if a == 'Date':
                    self.textboxes[a].text = autodate(self.textboxes[a].text)
                    self.textboxes[a].refresh(ui)
                elif a == 'Total Trip Mileage' and self.textboxes[a].text == '':
                    self.textboxes[a].text = str(filternums(self.textboxes['Close Mileage'].text)-filternums(self.textboxes['Start Mileage'].text))
                    self.textboxes[a].refresh(ui)
                sel = lis.index(a)
                if sel+dirr == len(lis):
                    sel = -1
                self.textboxes[lis[sel+dirr]].selected = True
                self.textboxes[lis[sel]].selected = False
                ui.selectedtextbox = ui.textboxes.index(self.textboxes[lis[sel+dirr]])
                break

        
class EDITINFO:
    def __init__(self,item,data,menu,master):
        self.item = item
        self.data = data
        self.outputdata = data
        self.menu = menu+item
        self.master = master
        self.editbox = dummytextbox(str(self.data))
        self.makegui()
    def makegui(self):
        ui.makewindowedmenu(10,10,400,140,self.menu,self.menu.removesuffix(self.item),basecol,roundedcorners=8,scalesize=False,scalex=False,scaley=False,ID=self.menu+'window')
        ui.makebutton(6,115,'Save',40,self.master.saveedited,self.menu,scalesize=False,scalex=False,scaley=False,roundedcorners=10,verticalspacing=3,objanchor=(0,'h/2'),ID=self.menu+'save')
        ui.makebutton(99,115,'Data',40,lambda: dataoutput(main.data,self.item),self.menu,scalesize=False,scalex=False,scaley=False,roundedcorners=10,verticalspacing=3,objanchor=(0,'h/2'),ID=self.menu+'save')
        self.titlewidth = 184
        self.textboxstart = 193
        self.checkboxes = {}
        if not self.item in list(main.checkboxes):
            ui.maketable(5,5,[[self.lineitem(self.item),ui.maketextbox(0,0,str(self.data),200,2,self.menu,roundedcorners=4,height=80,textsize=30,verticalspacing=4,scalesize=False)]],menu=self.menu,roundedcorners=4,boxwidth=[-1,200],boxheight=80,textsize=35,scalesize=False,scalex=False,scaley=False,col=basecol,ID=self.menu+'editbox')
            self.editbox = ui.IDs[self.menu+'editbox'].tableimages[0][1][1]
            self.textboxstart = ui.IDs[self.menu+'editbox'].boxwidths[0]+14
        else:
            ui.maketable(5,5,[[self.lineitem(self.item),'']],menu=self.menu,roundedcorners=4,boxwidth=[-1,200],boxheight=80,textsize=35,scalesize=False,scalex=False,scaley=False,col=basecol,ID=self.menu+'editbox',layer=0)
            xinc = ui.IDs[self.menu+'editbox'].boxwidths[0]+20
            exclusive = [self.menu+'checkbox'+b for b in main.checkboxes[self.item] if b!='textbox']
            for b in main.checkboxes[self.item]:
                if not(b in ['textbox','button','view']):
                    ui.maketext(xinc,45,b,30,self.menu,ID=self.menu+b,objanchor=(0,'h/2'),backingcol=basecol,scalesize=False)
                    xinc+=ui.IDs[self.menu+b].width+10
                    self.checkboxes[b] = ui.makecheckbox(xinc,45,40,self.seteditbox,menu=self.menu,ID=self.menu+'checkbox'+b,objanchor=(0,'h/2'),spacing=-8,clickdownsize=2,toggle=False,bindtoggle=exclusive,scalesize=False)
                    if self.item in ['Pronouns','Postcode','Ethnicity']: xinc+=ui.IDs[self.menu+'checkbox'+b].width+10
                    else: xinc+=ui.IDs[self.menu+'checkbox'+b].width+40
                    ui.IDs[self.menu+'checkbox'+b].storeddata = b 
                elif b == 'textbox':
                    self.editbox = ui.maketextbox(xinc,7,str(self.data),100,height=80,command=self.updatecheckboxes,menu=self.menu,ID=self.menu+'editbox',textsize=32,scalesize=False,commandifkey=True)
            self.textboxstart = xinc
        self.titlewidth = ui.IDs[self.menu+'editbox'].boxwidths[0]
        self.reshiftgui()
        self.updatecheckboxes()
    def seteditbox(self):
        enabled = -1
        for a in self.checkboxes:
            if self.checkboxes[a].toggle:
                enabled = a
        if enabled != -1:
            self.editbox.text = enabled
            self.editbox.refresh(ui)
    def updatecheckboxes(self):
        text = self.editbox.text.lower()
        boxes = [a.lower() for a in list(self.checkboxes)]
        for i,a in enumerate(self.checkboxes):
            if text == boxes[i]:
                self.checkboxes[a].toggle = True
            else:
                self.checkboxes[a].toggle = False
        if self.item == 'Postcode':
            text = self.editbox.text.lower()[2:4]
            if text!='':
                text = text.split()[0]
                try: text = int(text)
                except: return
                boxes = []
                for a in list(self.checkboxes):
                    b = a.replace('/','-')
                    b = b.removeprefix('CH')
                    rang = b.split('-')
                    boxes.append([a for a in range(int(rang[0]),int(rang[1])+1)])
                for i,a in enumerate(self.checkboxes):
                    if text in boxes[i]:
                        self.checkboxes[a].toggle = True
                    else:
                        self.checkboxes[a].toggle = False
            
        
        
    def lineitem(self,item):
        split = self.item.split()
        st = ''
        for i,a in enumerate(split):
            st+=a
            if i!=len(split)-1:
                if i in [1,4] or (self.item == 'Reasonable Adjustments' and i == 0):
                    st+='\n'
                else:
                    st+=' '
        return st
    def refreshmenu(self):
        if self.editbox.enabled:
            self.editbox.selected = True
            ui.selectedtextbox = ui.textboxes.index(self.editbox)
    def reshiftgui(self):
        if self.editbox.enabled:
            ui.IDs[self.menu+'window'].width = screenw-20
            self.editbox.width = screenw-32-self.textboxstart
            self.editbox.refresh(ui)
            ui.IDs[self.menu+'editbox'].boxwidth = [self.titlewidth,screenw-42-self.titlewidth]
            ui.IDs[self.menu+'editbox'].refresh(ui)
        else:
            ui.IDs[self.menu+'window'].width = self.textboxstart+12
            ui.IDs[self.menu+'editbox'].boxwidth = [self.titlewidth,self.textboxstart-self.titlewidth-14]
            ui.IDs[self.menu+'editbox'].refresh(ui)
    

class ITEM:
    def __init__(self,data):
        self.data = data
        self.menu = 'info'+str(self.data['ID'])
        premake = ['Postcode']
        self.menus = {a:EDITINFO(a,self.data[a],self.menu,self) for a in premake}
        self.active = False

    def makegui(self,main):
        self.active = True
        self.expenses = FORM('Expenses',self.data['Expenses'],self.menu,self)
        self.mileage = FORM('Mileage',self.data['Mileage'],self.menu,self)
        
        ## main
        ui.maketext(10,25,'Data for '+self.data['Forename'],40,self.menu,self.menu+'title',backingcol=(83,86,100),objanchor=(0,'h/2'),scalesize=False,layer=3)
        ui.makebutton(-8,25,'Back',30,ui.menuback,self.menu,ID=self.menu+'back',anchor=('w',0),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalesize=False,layer=3,col=basecol)
        ui.makebutton(-78,25,'Delete User',30,lambda: main.confirm(main.deluser),self.menu,ID=self.menu+'del',anchor=('w',0),objanchor=('w','h/2'),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalesize=False,layer=3,col=basecol)
        ui.makerect(0,0,screenw,50,menu=self.menu,layer=2,scalesize=False,col=(83,86,100),ID=self.menu+'rect')
        ui.makerect(0,50,screenw,4,menu=self.menu,layer=2,scalesize=False,col=(80,150,160),ID=self.menu+'rect2')
        ui.maketable(0,0,[],[ui.maketext(0,0,'Item',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True),
                             ui.maketext(0,0,'Info',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True),
                             ui.maketext(0,0,'Edit',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True)],self.menu,self.menu+'table',roundedcorners=4,textcenter=False,verticalspacing=4,textsize=30,boxwidth=[200,200,100],anchor=(10,60),col=basecol,scalesize=False,scalex=False,scaley=False,clickablerect=pygame.Rect(0,54,4000,4000))
        ui.makescroller(0,0,screenh-60,self.slidetable,pageheight=screenh-60,anchor=('w',60),objanchor=('w',0),scalesize=False,menu=self.menu,ID=self.menu+'scroller',runcommandat=1,layer=0)
        self.refreshtable()

        ## edit menu
        self.menus.update({a:EDITINFO(a,self.data[a],self.menu,self) for a in list(self.data) if (not(a in main.fieldignore) and not(a == 'Postcode'))})
        self.mileageupdate()
    def refreshtable(self):
        ui.IDs[self.menu+'table'].wipe(ui,False)
        data = []
        for a in self.data:
            if not(a in main.fieldignore):
                if a == 'ID':
                    obj = ''
                else:
                    if a == 'Emergency Contacts':
                        func = lambda: main.viewcontact(['Add',-1,self.data['ID']-1,self.menu])
                    else:
                        func = funcem(a,self)
                        func = func.func
                    obj = ui.makebutton(0,0,'{dots}',30,func,roundedcorners=4,clickdownsize=2,clickablerect=pygame.Rect(0,54,4000,4000))
                if type(self.data[a]) == list:
                    st = ''
                    for b in self.data[a]:
                        st+=(b['Name']+',')
                    data.append([str(a),st.removesuffix(','),obj])
                else:                
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
        if self.menus != []:
            for a in self.menus:
                self.menus[a].reshiftgui()
    def editmenu(self,item):
        self.selected = item
        self.menus[self.selected].refreshmenu()
        ui.movemenu(self.menu+self.selected,'down')
    def saveedited(self):
        self.data[self.selected] = self.menus[self.selected].editbox.text
        main.refreshdata()
        self.refreshtable()
        self.mileageupdate()
        ui.menuback()
    def mileageupdate(self):
        if self.data['Owns Vehicle and has Relevant Documents'] == 'Yes':
            ui.IDs[self.menu+'Mileagebutton'].enabled = True
        else:
            ui.IDs[self.menu+'Mileagebutton'].enabled = False
    def wipe(self):
        items = ['title','back','del','table','scroller','editbox','save','rect','rect2','window']
        for a in items:
             ui.delete(self.menu+a,False)

class MAIN:
    def init(self):
        self.newusercontacts = []
        self.menuin = 0
        #display contactID userID menu
        self.contactmenuuse = ['Add',0,-1,'add user']
        self.checkboxes = {'Pronouns':['She/Her','He/Him','They/Them','textbox'],'Postcode':['CH41-43','CH44/45','CH46-49','CH60-64','textbox'],'Driving license':['Yes','No'],'Owns Vehicle and has Relevant Documents':['Yes','No'],'Interested in volunteer driving':['Yes','No'],'Disability?':['Yes','No'],'Staff':['Yes','No'],'Emergency Contacts':['button','view'],'Active':['Yes','No'],'Ethnicity':['White British','White Irish','BAME','textbox']}
        self.fieldignore = ['Expenses','Mileage']
        
        
        self.data = notsql.load()
        self.searchterm = ['',['name']]

        self.menus = []
        self.generatemenus()
        self.makegui()
    def makegui(self):
        ## title screen
        ui.maketext(0,0,'',250,anchor=('w/2','0'),objanchor=('w/2','0'),img=pygame.image.load(resource_path('images\\make it happen.png')),colorkey=(251,251,251))
        ui.makebutton(0,270,'Users',50,lambda: ui.movemenu('table','up'),roundedcorners=10,clickdownsize=2,verticalspacing=4,anchor=('w/2','0'),objanchor=('w/2',0))
        ui.makebutton(0,330,'Add User',50,self.adduser,anchor=('w/2','0'),objanchor=('w/2',0),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalex=False,scaley=False)
        
        
        ## main table
        ui.maketable(0,0,[],['ID','Name','More'],anchor=(10,60),boxwidth=[100,300,100],verticalspacing=5,textsize=30,roundedcorners=4,col=basecol,ID='main table',menu='table',scalesize=False,clickablerect=pygame.Rect(0,54,4000,4000))
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
        for i,a in enumerate(self.empty):
            if not(a in self.fieldignore):
                if a != 'ID':
                    ui.maketext(30,yinc,a,35,'add user',ID='add user'+a,maxwidth=200,backingcol=basecol)
                    h = ui.IDs['add user'+a].height
                    if a in self.checkboxes:
                        xinc = 240
                        disper = 540/len(self.checkboxes[a])
                        exclusive = ['add user checkbox'+a+'*'+b for b in self.checkboxes[a] if b!='textbox']
                        for b in self.checkboxes[a]:
                            if not(b in ['textbox','button','view']):
                                ui.maketext(xinc,yinc+h/2,b,30,'add user',ID='add user'+a+'*'+b,objanchor=(0,'h/2'),backingcol=basecol)
                                xinc+=ui.IDs['add user'+a+'*'+b].width+10
                                ui.makecheckbox(xinc,yinc+h/2,40,menu='add user',ID='add user checkbox'+a+'*'+b,objanchor=(0,'h/2'),spacing=-8,clickdownsize=2,toggle=False,bindtoggle=exclusive,clickableborder=15)
                                if a in ['Pronouns','Postcode','Ethnicity']: xinc+=ui.IDs['add user checkbox'+a+'*'+b].width+10
                                else: xinc+=ui.IDs['add user checkbox'+a+'*'+b].width+40
                                ui.IDs['add user checkbox'+a+'*'+b].storeddata = b
                                self.shiftingitems.append('add user'+a+'*'+b)
                                self.shiftingitems.append('add user checkbox'+a+'*'+b)
                            elif b == 'textbox' and a!='Postcode':
                                if a == 'Pronouns': wid = 133
                                else: wid = 93
                                ui.maketextbox(xinc,yinc,'',wid,height=h,menu='add user',ID='add user inp'+a+'*'+b,textsize=32)
                                self.shiftingitems.append('add user inp'+a+'*'+b)
                            elif b == 'button':
                                ui.makebutton(xinc,yinc,'Add Emergency Contact',32,command=lambda: self.newcontact(['New',-1,-1,'add user']),width=200,height=h,menu='add user',ID='add user button'+a+'*'+b,roundedcorners=6,clickdownsize=2)
                                self.shiftingitems.append('add user button'+a+'*'+b)
                            elif b == 'view':
                                ui.makebutton(xinc+210,yinc,'View Emergency Contacts',32,command=lambda: self.viewcontact(['Add',-1,-1,'add user']),width=200,height=h,menu='add user',ID='add user button'+a+'*'+b,roundedcorners=6,clickdownsize=2)
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
        ui.makewindowedmenu(60,60,680,341,'add contact','add user',basecol,roundedcorners=10,scaley=True,ID='add contacts menu')
        ui.maketext(340,10,'Add Emergency Contact',40,'add contact',backingcol=basecol,objanchor=('w/2',0),ID='add contacts title')
        self.contactinfo = list(completecontactdata())
        yinc = 55
        for item in self.contactinfo:
            ui.maketext(10,yinc,item,34,'add contact',backingcol=basecol)
            ui.maketextbox(200,yinc,'',460,1,'add contact',textsize=32,ID='add contact'+item)
            yinc+=49
        ui.makebutton(420,yinc-12,'Save',34,self.saveemergencycontact,'add contact',objanchor=('w/2',0),verticalspacing=4,roundedcorners=5,clickdownsize=2)
        ui.makebutton(260,yinc-12,'Clear',34,self.clearcontactmenu,'add contact',objanchor=('w/2',0),verticalspacing=4,roundedcorners=5,clickdownsize=2)

        # view emergency contacts
        ui.makewindowedmenu(60,60,680,335,'view contact','add user',basecol,roundedcorners=10,scaley=True,ID='view contacts')
        ui.maketable(10,10,[],['Name','',''],'view contact',ID='view contacts menu',col=basecol,roundedcorners=4,verticalspacing=3,textsize=30,boxwidth=[545,80,27],boxheight=27)
        ui.makebutton(12,12,'+',40,lambda: self.newcontact(-1),'view contact',col=basecol,roundedcorners=4,clickdownsize=1,border=2,layer=2,width=27,height=27,textoffsety=-2,textoffsetx=1)
        self.refreshcontactstable()

        ## confirm menu
        ui.makewindowedmenu(0,0,200,122,'confirm',col=basecol,roundedcorners=10,ID='confirm menu',center=True,anchor=('w/2','h/2'))
        ui.maketext(100,5,'Confirm',40,'confirm',backingcol=basecol,objanchor=('w/2',0))
        ui.makebutton(100,50,'DELETE',50,menu='confirm',verticalspacing=6,roundedcorners=7,col=(180,60,60),objanchor=('w/2',0),ID='confirm button',clickdownsize=2)
        self.reshiftgui()
        
        
    def generatemenus(self):
        for a in self.menus:
            a.wipe()
        self.menus = []
        for a in self.data:
            self.menus.append(ITEM(a))
            
    def refreshtable(self):
        displaydata = searchdata(self.data,self.searchterm)
        encode = {'Yes':0,'':1,'No':2}
        cols = {0:'(220,220,240)',1:'(150,150,160)',2:'(250,100,100)'}
        for a in range(len(displaydata)):
            displaydata[a]['encoded'] = encode[displaydata[a]['Active']]
        displaydata.sort(key=lambda x: x['encoded'])
        
        ui.IDs['main table'].wipe(ui,False)
        data = []
        for a in range(len(displaydata)):
            func = funcmn(displaydata[a]['ID'],self)
            obj = ui.makebutton(0,0,'{dots}',30,func.func,roundedcorners=4,clickdownsize=2,clickablerect=pygame.Rect(0,54,4000,4000))
            data.append([displaydata[a]['ID'],'{"'+displaydata[a]['Forename']+' '+displaydata[a]['Surname']+'"'+cols[displaydata[a]['encoded']]+'}',obj])

        sc = ui.IDs['main scroller']
        if (sc.maxp-sc.minp)>sc.pageheight:
            ui.IDs['main table'].boxwidth = [100,(screenw-8-20-200-15),100]
        else: ui.IDs['main table'].boxwidth = [100,(screenw-8-20-200),100]
        
        ui.IDs['main table'].data = data
        ui.IDs['main table'].refresh(ui)
        
    def newcontact(self,contactmenuuse):
        if contactmenuuse == -1:
            if self.contactmenuuse[3] == 'add user': contactmenuuse = ['New',-1,-1,self.contactmenuuse[3]]
            else: contactmenuuse = ['Add',-1,-1,self.contactmenuuse[3]]
        ui.IDs['add contacts menu'].behindmenu = contactmenuuse[3]
        ui.IDs['view contacts'].behindmenu = contactmenuuse[3]
        self.contactmenuuse = contactmenuuse
        ui.movemenu('add contact','down')
        self.refreshcontactstable()
    def viewcontact(self,contactmenuuse):
        ui.IDs['add contacts menu'].behindmenu = contactmenuuse[3]
        ui.IDs['view contacts'].behindmenu = contactmenuuse[3]
        self.contactmenuuse = contactmenuuse
        self.refreshcontactstable()
        ui.movemenu('view contact','down')
    def editcontact(self,contactmenuuse):
        ui.IDs['add contacts menu'].behindmenu = contactmenuuse[3]
        ui.IDs['view contacts'].behindmenu = contactmenuuse[3]
        self.contactmenuuse = contactmenuuse
        items = list(completecontactdata())
        ids = ['add contact'+a for a in items]
        for a in range(len(ids)):
            if contactmenuuse[3] == 'add user':
                ui.IDs[ids[a]].text = self.newusercontacts[contactmenuuse[1]][items[a]]
            else:
                ui.IDs[ids[a]].text = self.data[contactmenuuse[2]]['Emergency Contacts'][contactmenuuse[1]][items[a]]
            ui.IDs[ids[a]].refresh(ui)
            
        ui.movemenu('add contact','down')
        self.refreshcontactstable()
    def deletecontact(self,contactmenuuse):
        self.contactmenuuse = contactmenuuse
        if self.contactmenuuse[3] == 'add user':
            del self.newusercontacts[self.contactmenuuse[1]]
        else:
            del self.data[self.contactmenuuse[2]]['Emergency Contacts'][self.contactmenuuse[1]]
        self.menus[self.contactmenuuse[2]].refreshtable()
        self.refreshcontactstable()
        notsql.store(self.data)
    def clearcontactmenu(self):
        ids = ['add contact'+a for a in list(completecontactdata())]
        for a in range(len(ids)):
            ui.IDs[ids[a]].text = ''
            ui.IDs[ids[a]].refresh(ui)
        
    def refreshcontactstable(self):
        ui.IDs['view contacts menu'].wipe(ui,False)
        data = []
        contactinfo = copy.deepcopy(self.newusercontacts)
        if self.contactmenuuse[3] != 'add user':
            contactinfo = copy.deepcopy(self.menus[self.contactmenuuse[2]].data['Emergency Contacts'])
        for i,a in enumerate(contactinfo):
            if self.contactmenuuse[3]!='add user': func = funcec(['Edit',i,self.contactmenuuse[2],ui.IDs['view contacts'].behindmenu])
            else: func = funcec(['Edit',i,-1,'add user'])
            editbutton = ui.makebutton(0,0,'{dots}',30,func.func,'view contact',roundedcorners=4,col=basecol,clickdownsize=1)
            if self.contactmenuuse[3]!='add user': func = funcdc(['Edit',i,self.contactmenuuse[2],ui.IDs['view contacts'].behindmenu])
            else: func = funcdc(['Edit',i,-1,'add user'])
            crossbutton = ui.makebutton(0,0,'{cross}',17,func.func,'view contact',roundedcorners=4,col=basecol,clickdownsize=1,textoffsetx=1,textoffsety=1)
            data.append([a['Name'],editbutton,crossbutton])
        ui.IDs['view contacts menu'].data = data
        ui.IDs['view contacts menu'].boxheight = 27
        ui.IDs['view contacts menu'].refresh(ui)
        ui.IDs['add contacts title'].text = self.contactmenuuse[0]+' Emergency Contact'
        ui.IDs['add contacts title'].refresh(ui)
    def saveemergencycontact(self):
        items = list(completecontactdata())
        ids = ['add contact'+a for a in items]
        data = {}
        for i,a in enumerate(ids):
            data[items[i]] = ui.IDs[a].text
        if self.contactmenuuse[0] == 'Add':
            self.data[self.contactmenuuse[2]]['Emergency Contacts'].append(data)
            self.menus[self.contactmenuuse[2]].refreshtable()
            notsql.store(self.data)
        elif self.contactmenuuse[0] == 'New':
            self.newusercontacts.append(data)
        elif self.contactmenuuse[0] == 'Edit':
            if self.contactmenuuse[3]!='add user':
                self.data[self.contactmenuuse[2]]['Emergency Contacts'][self.contactmenuuse[1]] = data
                self.menus[self.contactmenuuse[2]].refreshtable()
                notsql.store(self.data)
            else:
                self.newusercontacts[self.contactmenuuse[1]] = data
        self.refreshcontactstable()
        self.clearcontactmenu()
        ui.menuback()

    def confirm(self,func):
        ui.IDs['confirm menu'].behindmenu = ui.activemenu
        ui.IDs['confirm button'].command = func
        ui.movemenu('confirm','down')
    
    def slidetable(self):
        ui.IDs['main table'].y = 60-ui.IDs['main scroller'].scroll
        ui.IDs['main table'].refreshcords(ui)
    def moredetailmenu(self,ID):
        self.menuin = ID-1
        if not self.menus[self.menuin].active:
            self.menus[self.menuin].makegui(self)
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
            elif type(ui.IDs[a]) == pyui.BUTTON and ui.IDs[a].toggleable: 
                ui.IDs[a].toggle = False
        self.newusercontacts = []
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
                if ui.IDs[a].toggle and ui.IDs[a].toggleable:
                    data[items[0]] = ui.IDs[a].storeddata
                
        data['Emergency Contacts'] = copy.deepcopy(self.newusercontacts)
        self.data.append(completedata(data))
        notsql.store(self.data)
        self.refreshtable()
        self.menus.append(ITEM(completedata(data)))
        self.clearuser()
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
            ui.IDs[a].y = (ui.IDs[a].anchor[1]+ui.IDs[a].starty*ui.IDs[a].scale-ui.IDs[a].objanchor[1]*ui.IDs[a].scale)/ui.IDs[a].dirscale[1]-ui.IDs['add menu scroller'].scroll
            ui.IDs[a].refreshcords(ui)
    def reshiftgui(self):
        ui.IDs['search bar'].width = (screenw-100)/2
        ui.IDs['search bar'].refresh(ui)
        ui.IDs['tabletoprect1'].width = screenw
        ui.IDs['tabletoprect2'].width = screenw
        ui.IDs['add menu scroller'].height = screenh-54*ui.scale
        ui.IDs['add menu scroller'].pageheight = screenh/ui.scale
        ui.IDs['add menu scroller'].maxp = (ui.IDs['add userStaff'].anchor[1]+(ui.IDs['add userStaff'].starty-ui.IDs['add userStaff'].objanchor[1])*ui.IDs['add userStaff'].scale)/ui.IDs['add userStaff'].dirscale[1]
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
main.init()


while not done:
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE or (event.type == pygame.KEYDOWN and event.key == pygame.K_F5):
            screenw = ui.screenw
            screenh = ui.screenh
            main.reshiftgui()
            if 'info' in ui.activemenu:
                main.menus[main.menuin].reshiftgui()
                main.menus[main.menuin].refreshtable()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RETURN or event.key == pygame.K_DOWN or event.key == pygame.K_UP) and not(ui.kprs[pygame.K_LSHIFT]):
                dirr = 1
                if event.key == pygame.K_UP:
                    dirr = -1
                if len(main.menus)>0 and main.menus[main.menuin].active:
                    main.menus[main.menuin].mileage.enterdown(dirr)
                    main.menus[main.menuin].expenses.enterdown(dirr)
                data = list(completedata({}))
                if ui.selectedtextbox != -1:
                    ID = ui.textboxes[ui.selectedtextbox].ID
                    if ('add user inp' in ID) or ('add contact' in ID):
                        if 'add contact' in ID:
                            data = main.contactinfo
                            prefix = 'add contact'
                        else:
                            prefix = 'add user inp'
                        item = ID.removeprefix(prefix)
                        if item in data and (data.index(item)!=len(data)-1 or dirr == -1):
                            if item == 'Date Started':
                                ui.IDs[ID].text = autodate(ui.IDs[ID].text)
                                ui.IDs[ID].refresh(ui)
                            ui.IDs[ID].selected = False
                            newID = prefix+data[data.index(item)+dirr]
                            inc = dirr*2
                            while not(newID in ui.IDs):
                                newID = prefix+data[data.index(item)+inc]
                                inc+=dirr
                                if data.index(item)+inc == len(data):
                                    newID = ID
                                    break
                        ui.IDs[ID].selected = False
                        ui.IDs[newID].selected = True
                        ui.selectedtextbox = [a.ID for a in ui.textboxes].index(newID)
                            
    screen.fill(basecol)
    ui.rendergui(screen)
##    screen.blit(icon,(0,0))
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit() 
