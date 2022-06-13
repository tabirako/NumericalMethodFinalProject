#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
import tkinter.messagebox


# In[2]:


## all unit in millimeter
speedOfSound = 345000 # mm/sec
## The speed of sound in dry air at 22 °C is 344.632 m/s


# In[ ]:





# In[3]:


noteName = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
interval = [2,2,1,2,2,2,1] # Major
blist = list()


# In[4]:


def button_event(v):
    tk.messagebox.showinfo('{0}'.format(v))

win = tk.Tk()
win.title("FluteDimension")
win.geometry('700x450')

### 12TET is used
needNote = 7
selectedKey = 0 # the fundamental note on the flute -12~+12, default=0 (middle C)

def change_notenum():
    global needNote
    needNote = int(nVar.get())
    #print(needNote)
    
def change_basenote():
    global selectedKey
    selectedKey = int(baseVar.get())
    #print(needNote)
    
### main calculating part 
### very important
    
def calc(needNote,selectedKey,t,a,b,d,e,standardFreq,blist):
    #print(needNote,selectedKey,t,a,b,d,e,standardFreq,blist)
    global result_text
    global noteName
    global interval
    
    ### all the varibles here should be able to modified

    # t =wall thickness of the tube

    # a =inside radius of tube
    # b = radius of blow hole

    # d = distance from center of blow hole to stopper
    # e = 0.3 fraction of blow hole covered by the player's lip normally from 0.25 to 0.33

    
    def Heff(): 
        return t+1.7*b

    def Lb(): # should be fixed for all holes, virtual length for blowhole
        return Heff()*(1 - e)*(a/b)**2

    def Lo(): # ideal length
        """
        v = λf
        λ = v/f
        the length of the tube from the center of the blow hole to the open end is half λ
        """
        return 0.5*speedOfSound/fundamental

    def Le(f): # effective length
        """
        print(f'Lb()={Lb()}')
        print(f'Lo(f)={Lo(f)}')
        print(f'0.6*a={0.6*a}')
        """
        # 0.6*a is the extra length for the end of the tube

        return Lb()+Lo()+0.6*a
    
    fundamental = standardFreq*2**((selectedKey-9)/12) # fundamental freq
    k = selectedKey
    
    ### no key hole for the fundamental
    length = [[noteName[k%12],0,fundamental,Le(fundamental),Lo()]]
    
    ## create first arrpox. postition as a list
    for i in range(1,needNote):
        k += interval[(i-1)%7]
        #print(k)
        length.append([noteName[k%12],
                    blist[i-1],
                    fundamental*2**((k-selectedKey)/12), # freq 
                    Le(fundamental)*2**(-(k-selectedKey)/12), # desired effetive length <<< Lei >>>
                    Le(fundamental)*2**(-(k-selectedKey)/12)-Lb()-0.6*a # <<<approx. hole positions>>>
                    ])
    
    ## calcuting part
    for n in range(1,needNote):
        for j in range(10):
            for i in range(n,needNote):
                _b = length[i][1]
                if i == n:

                    D = length[i-1][4]-length[i][4]
                    Lc= (t+1.5*_b)/( (_b/a)**2 + (t+1.5*_b)/D )
                    # print(f'first{Lc}')

                else:
                    s = 0.5 * (length[i-1][4]-length[i][4])
                    Lc =  s*( (1 + 2*(1.5*_b + t)*(a/_b)**2 /s )**0.5 - 1 )
                    # print(f'S={s}')
                    # print(f'second{i},{j},{n},{Lc}')

                length[i][4] = length[i][3]-Lc-Lb()
    """
    # checkes result
    for i in length:
        print(i)
    """
    
    # delete previous result
    result_text.delete("1.0","end")
     
    #print new results
    result_text.insert("1.0",f"Notes\tøHole\tFrequency\t\tLength from embouchure\n ")
    result_text.insert("end",f"{length[0][0]}\t - \t{length[0][2]:.2f}\t\t{length[0][4]:.2f}\n ")
        
    for i in range(1,needNote):
        ast = '*' if  length[i][4].imag != 0 else ''
        result_text.insert("end",f"{length[i][0]}\t{length[i][1]*2:.2f}\t{length[i][2]:.2f}\t\t{length[i][4].real:.2f}{ast}\n ")
    
    # if the difference between hole i and hole i-1 is negative, it creates complex numers,
    # which means the dimension entered by the user
    # can't be estimated with this method
    
    if ast == '*':
         result_text.insert("end","* = Not Accurate")

### pop up screen for entering the hole sizes
### use pop up screen for the option of different note numbers

def enterKey():
    
    global blist
    global needNote
    global selectedKey
    global noteName
    
    top = tk.Toplevel(win)
    top.title("key sizes")
    
    keylabels = list()
    keyentries = list()
    
    b = float(bVar.get())
    
    #notice for the arrangement of input boxes
    noticelabel = tk.Label(top, text=f'Enter the key radius from\nthe lowest note to the highest')
    noticelabel.pack()
    
    ## create boxes, await for user input
    k = selectedKey
    for i in range(1,needNote):
        k += interval[(i-1)%7]
        keylabels.append(tk.Label(top, text=f"Key hole radius for: {noteName[k%12]}"))
        keyentries.append(tk.Entry(top))
    
    ### default dimension
    for entry in keyentries:
        entry.insert(0, b)
    
    ## pack boxes
    for label, entry in zip(keylabels, keyentries):
        label.pack()
        entry.pack()
    
    ###close the pop-up screen after entering the dimensions
    def command():
        global blist
        global needNote
        global selectedKey
        
        
        bmap = map(float, [entry.get() for entry in keyentries])
        blist = list(bmap)
        
        #print(blist)
        top.destroy()
        
        calc(needNote,
             selectedKey,
             float(tVar.get()),
             float(aVar.get()),
             float(bVar.get()),
             float(dVar.get()),
             float(eVar.get()),
             float(fundamentalVar.get()),
             blist)
    
    ### even if it's closed, the default will kick in
    def on_closing():
        global blist
        bmap = map(float, [entry.get() for entry in keyentries])
        blist = list(bmap)
        print(blist)
        top.destroy()
        calc(needNote,
             selectedKey,
             float(tVar.get()),
             float(aVar.get()),
             float(bVar.get()),
             float(dVar.get()),
             float(eVar.get()),
             float(fundamentalVar.get()),
             blist)

    buttonFinish = tk.Button(top, text="Finish", command=command)
    buttonFinish.pack()
    
    top.protocol("WM_DELETE_WINDOW", on_closing)

#needed Hole
sblabel = tk.Label(win, text='How many notes do you want:')
sblabel.grid(column = 0, row = 0, columnspan = 2)

##spinbox for neednote
nVar = tk.StringVar()
nVar.set('7')
sb = tk.Spinbox(win, textvariable = nVar, from_ = 1, to = 9, command = change_notenum, takefocus = False, width = 5,font=('Arial',12))
sb.grid(column = 2, row = 0)

#spin box seleted key
sblabel = tk.Label(win, text=f'Transpose, default=C foot=0')
sblabel.grid(column = 0, row = 1, columnspan = 2)

baseVar = tk.StringVar()
baseVar.set('0')
sb = tk.Spinbox(win, textvariable = baseVar, from_ = -12, to = 12, command = change_basenote, takefocus = False, width = 5,font=('Arial',12))
sb.grid(column = 2, row = 1)

#slide inside radius
tVar = tk.DoubleVar()
tVar.set(1.25)
button_a = tk.Scale(win, label = 'Inner radius', orient = 'h', length=250, from_ = 0.05, to = 3, resolution = 0.05, variable = tVar)
button_a.grid(row = 2, column = 0, columnspan = 3)

#slide inside radius
aVar = tk.DoubleVar()
aVar.set(9.5)
button_a = tk.Scale(win, label = 'Inner radius', orient = 'h', length=250, from_ = 0.1, to = 25, resolution = 0.1, variable = aVar)
button_a.grid(row = 3, column = 0, columnspan = 3)

#slide blow hole radius
bVar = tk.DoubleVar()
bVar.set(5)
button_b = tk.Scale(win, label = 'Blow hole radius', orient = 'h', length=250, from_ = 0.1, to = 15, resolution = 0.1, variable = bVar)
button_b.grid(row = 4, column = 0, columnspan = 3)

#slide stopper distance
dVar = tk.DoubleVar()
dVar.set(17)
button_d = tk.Scale(win, label= 'Stopper distance', orient = 'h', length=250, from_ = 1, to = 30, resolution = 1, variable = dVar)
button_d.grid(row = 5, column = 0, columnspan = 3)

#slide embouchure
eVar = tk.DoubleVar()
eVar.set(0.3)
             
button_e = tk.Scale(win, label = 'Covered% embouchure', orient = 'h', length=250, from_ = 0.25, to = 0.33, resolution = 0.01, variable = eVar)
button_e.grid(row = 6, column = 0, columnspan = 3)

#slide fundamental
fundamentalVar = tk.DoubleVar()
fundamentalVar.set(440)
             
button_e = tk.Scale(win, label = 'fundamental frequency', orient = 'h', length=250, from_ = 415.3, to = 466.2, resolution = 0.01, variable = fundamentalVar)
button_e.grid(row = 7, column = 0, columnspan = 3)

#ask for user input of key hole sizes
button_compute = tk.Button(win, text='Enter the key sizes', font=('Arial',12), command=enterKey)
button_compute.grid(row = 8, column = 0, columnspan = 3)

#result label with notion on units
notice_text = tk.Label(win, text=f'result: 　†all lengths are in milimeter')
notice_text.grid(row = 0, column = 3, sticky="w")

#print result text in here
result_text=tk.Text(win)
result_text.grid(row = 1, column = 3,rowspan = 8, sticky="w")


# In[5]:


win.mainloop()


# In[ ]:




