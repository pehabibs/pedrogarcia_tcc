#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Carregamento de pacotes do Python
import pandas as pd
import matplotlib.animation as animation
import numpy as np
import time
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *
import asyncio
from asyncua import Client, Node
from asyncua.common.subscription import DataChangeNotif, SubHandler


# In[ ]:





# In[ ]:


#Dados de entrada

from tkinter import *

TAG = 0
In_Tempo = 0

def aoClicar():
    global TAG
    TAG = entrada.get()
    window.destroy()

window = Tk()
window.geometry("400x100")
window.title("Pedro Garcia TCC")

mensagem = StringVar()
mensagem.set("Dados de entrada:") 
mensagemLabel = Label(window,textvariable=mensagem).pack()


mensagem2 = StringVar()
mensagem2.set("TAG:") 
mensagem2Label = Label(window,textvariable=mensagem2).pack()



entrada = Entry(window)
entrada.pack()

botao = Button(window, text="Salvar", command=aoClicar)
botao.pack()
window.mainloop()
In_Tempo = time.time()


# In[ ]:





# In[ ]:


#Monitoramento

Estados = {'max_abertura':[0], 'min_abertura':[0], 'aberta':[1], 'fechada':[0], 'abrir':[0], 'fechar':[0], 'abrindo':[0], 'fechando':[0], 'falha':[0]}
banco_dados = pd.DataFrame(Estados)

#AUX2 = 0
TEMPO = 0
SINAL = 0
POTENCIOMETRO = 0
atual_Estado = ""
atual_Estado2 = ""
ant_POTENCIOMETRO = 0
ant_SINAL = 0
l_elapsedTime = [0]
l_elapsedTime2 = [0]
l_potenciometro = [0]    
l_sinal = [0]
agarramento = FALSE
calibracao = FALSE
max_abertura=0
min_abertura=1
cont=0
l_auxx=[0]
l_erro=[0]
ciclo=0

async def monitoramento(l_aux,i):
                #global AUX2
                global TEMPO
                global SINAL
                global POTENCIOMETRO
                global ant_POTENCIOMETRO
                global ant_SINAL
                global ant_TEMPO
                global val_POTENCIOMETRO
                global atual_Estado
                global atual_Estado2
                global atu_SINAL
                global atu_TEMPO
                global max_abertura
                global min_abertura
                global l_elapsedTime
                global l_sinal
                global l_potenciometro
                global In_Tempo
                global cont
                global l_auxx
                global l_erro

                


                if(i == 0):
                    if(cont==0):
                        l_potenciometro.append(l_aux[-1])
                        TEMPO = time.time()- In_Tempo
                        l_elapsedTime.append(TEMPO) 
                        aux11=l_sinal[-1]#
                        l_sinal.append(aux11)#
                        ant_POTENCIOMETRO = l_potenciometro[-2]
                        POTENCIOMETRO = l_potenciometro[-1]
                        l_auxx.append(l_aux[-1])
                        cont=0
                        aux31=l_sinal[-1]-l_auxx[-1]
                        l_erro.append(aux31)
                    
                if(i == 1):
                    if(cont==0):
                        l_sinal.append(l_aux[-1])
                        ant_SINAL = l_sinal[-2]
                        SINAL = l_sinal[-1]
                        cont=0#
                        TEMPO = time.time()- In_Tempo
                        l_elapsedTime.append(TEMPO) 
                        aux21=l_auxx[-1]#
                        l_auxx.append(aux21)#
                        aux41=l_sinal[-1]-l_auxx[-1]
                        l_erro.append(aux41)
                    
                    

                if(POTENCIOMETRO > ant_POTENCIOMETRO):
                    Estados['abrindo'] = 1
                    Estados['fechando'] = 0 
                    atual_Estado2 = "Abrindo"    
                else:
                    Estados['abrindo'] = 0
                    Estados['fechando'] = 1
                    atual_Estado2 = "Fechando"
                    

                if(SINAL >= 1410):
                    Estados['aberta'] = 0
                    Estados['fechada'] = 1
                if(SINAL <= 0):
                    Estados['aberta'] = 0
                    Estados['fechada'] = 1                   
                        
                if(SINAL > ant_SINAL):
                    Estados['abrir'] = 1
                    Estados['fechar'] = 0
                    atual_Estado = "Abrir" 
                else:
                    Estados['abrir'] = 0
                    Estados['fechar'] = 1
                    atual_Estado = "Fechar"
                    
                if(SINAL==99):
                    if(ant_SINAL!=SINAL):
                    
                        Estados['max_abertura'] = 1
                        max_abertura= max_abertura + 1
                        print("Maximo de abertura")
                else:                    
                    Estados['max_abertura'] = 0
                
                if(SINAL==0):
                    if(ant_SINAL!=SINAL):
                        Estados['min_abertura'] = 1
                        min_abertura= min_abertura + 1
                        print("Minimo de abertura")
                else:                    
                    Estados['min_abertura'] = 0
                    
                    





# In[ ]:





# In[ ]:


#Analise dos dados
auxvisu =0

def plot(): 
    global l_sinal
    global l_elapsedTime
    global l_potenciometro
    global l_erro
    global TAG
    global max_abertura
    global min_abertura
    global agarramento
    global calibracao
    global ws2
    global fig
    global plt
    global auxvisu
    global canvas
    global toolbar
    global ax
    global fig
    global text10
    global text20
    global text30
    global text40
    global text50
    global ciclo
    global l_auxx
    global l_erro
    
            

            
    if(max_abertura>=min_abertura):
        ciclo = max_abertura - (max_abertura - min_abertura) 
    else:
        ciclo = min_abertura - (min_abertura - max_abertura)
    
        
    if(auxvisu==0):

        ws2 = Tk()
        ws2.title('Pedro Garcia TCC')
        ws2.geometry('800x600')  
        auxvisu=1
    

    
        fig,ax=plt.subplots(2,1, figsize=(9, 5))
        fig.subplots_adjust(left=0.1, right=0.6,top=1, bottom=0.1,hspace=0.4)
    
        text10=fig.text(0.7, 0.35, "TAG:   " + TAG)
        text20=fig.text(0.7, 0.3, "Total de steps:   " + str(len(l_sinal)))
        text30=fig.text(0.7, 0.25, "Ciclo:   " + str(ciclo))
        text40=fig.text(0.7, 0.2, "Agarramento:   " + str(agarramento))
        text50=fig.text(0.7, 0.15, "Calibração:   " + str(calibracao))
    
    
        plt.rc('font', size=12)          # controls default text sizes
        plt.rc('axes', titlesize=12)     # fontsize of the axes title
        plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
        plt.rc('legend', fontsize=12)    # legend fontsize
        plt.rc('figure', titlesize=20)
    
    


        ax[0].plot(l_elapsedTime, l_sinal, color="blue")
        ax[0].plot(l_elapsedTime, l_auxx, color="red")
        ax[0].set(xlabel='tempo (s)', ylabel='amplitude do sinal (un)', title='Experimento 1: Gráfico dos sinais da válvula')
        ax[0].legend(["Sinal de entrada da válvula","Sinal de saída da válvula"], bbox_to_anchor = (1.8, 1))
        ax[0].grid()   
    
        ax[1].plot(l_elapsedTime, l_erro, color="green")
        ax[1].set(xlabel='tempo (s)', ylabel='amplitude do sinal (un)')#, title='Experimento 1: Gráfico dos sinais da válvula')
        ax[1].legend(["Erro de referência"], bbox_to_anchor = (1.59, 2))
        ax[1].grid() 
    
    
        fig.savefig("exp1.png");     
        plt.show()            

        canvas = FigureCanvasTkAgg(fig,master = ws2)   
        canvas.draw() 
        canvas.get_tk_widget().pack() 
        toolbar = NavigationToolbar2Tk(canvas,ws2) 
        toolbar.update() 
        canvas.get_tk_widget().pack()
        
    else:
        fig.savefig("exp1.png");  
    
    
    
auxs=0
auxs2=0
    
def plot2():
    global l_sinal
    global l_elapsedTime
    global l_potenciometro
    global l_erro
    global TAG
    global max_abertura
    global min_abertura
    global agarramento
    global calibracao
    global ws2
    global fig
    global plt
    global auxvisu
    global canvas
    global toolbar
    global ax
    global fig
    global text10
    global text20
    global text30
    global text40
    global text50
    global ciclo
    global l_auxx
    global auxs
    global auxs2
    
        
        

    for i in range(len(l_erro)): 
        #print(l_erro)
        if(l_erro[i]>=10):
            
            for y in range(len(l_erro)):
                if(l_erro[-y]<=5):
                    if(auxs==0 and auxs2==0):
                        if(y<=100):
                            agarramento=TRUE
                            auxs=len(l_erro)-y -1
                        
                        else:
                            calibracao=TRUE
                            auxs2=len(l_erro)-y -1
                        
        

            
    if(max_abertura>=min_abertura):
        ciclo = (max_abertura - (max_abertura - min_abertura))/2

    else:
        ciclo = (min_abertura - (min_abertura - max_abertura))/2
        

    ax[0].plot(l_elapsedTime, l_sinal, color="blue")
    ax[0].plot(l_elapsedTime, l_auxx, color="red")
    ax[1].plot(l_elapsedTime, l_erro, color="green")
    text10.set_visible(False)
    text10=fig.text(0.7, 0.35, "TAG:   " + TAG)
    text10.set_visible(True)    
    
    
    text20.set_visible(False)
    text20=fig.text(0.7, 0.3, "Total de steps:   " + str(int(len(l_sinal)/2)))
    text20.set_visible(True)
        
    text30.set_visible(False)
    text30=fig.text(0.7, 0.25, "Ciclo:   " + str(ciclo))
    text30.set_visible(True)
        
    if(auxs>=1):
        text40.set_visible(False)
        text40=fig.text(0.7, 0.2, "Agarramento:   " + str(agarramento) + "  em  " + str(int(l_elapsedTime[auxs]))+"s")
        text40.set_visible(True)
    else:
    
        text40.set_visible(False)
        text40=fig.text(0.7, 0.2, "Agarramento:   " + str(agarramento) + "  em  0s")
        text40.set_visible(True)
        
    if(auxs2>=1):  
        text50.set_visible(False)
        text50=fig.text(0.7, 0.15, "Calibração:   " + str(calibracao) + "  em  " + str(int(l_elapsedTime[auxs2]))+"s")
        text50.set_visible(True)
    else:
        
        text50.set_visible(False)
        text50=fig.text(0.7, 0.15, "Calibração:   " + str(calibracao) + "  em  0s")
        text50.set_visible(True)
    
    
    
    
    canvas.draw() 
    toolbar.update() 
    ws2.update()






# In[ ]:


#Visualização
from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) 


running = False
status = 0 


def b1():
    global running
    global OPEN
    global status
    global In_Tempo
    running = True

    button1['state'] = NORMAL
    button2['state'] = DISABLED  
    
    atualiza()
    
    

def b2(): 
    global running
    
    running = False
    button1['state'] = DISABLED 
    button2['state'] = NORMAL
    

def atualiza():
    global POTENCIOMETRO
    global atual_Estado
    global atual_Estado2
    global TEMPO
    global SINAL
    global atn_SINAL
    global In_Tempo
    global auxvisu

    if running == True:
        bar['value']=(float(POTENCIOMETRO))
        status = float(bar['value']) 
         
        percent.set("Entrada:"+str(int(SINAL))+"%") 

        text2.set("Estado entrada:"+ atual_Estado)
        percent2.set("Saida:"+str(int(POTENCIOMETRO))+"%") 
        
        text.set("Estado saida:"+ atual_Estado2) 
        
        tem.set("Tempo:"+ str(int(TEMPO)))
        
        if(auxvisu==1):
            
            plot2()
        ws.update()
            
    else:
            if(auxvisu==1):
                plot2()
                
            ws.update()
    
    
    
ws = Tk()
ws.title('Pedro Garcia TCC')
ws.geometry('500x500')


percent = StringVar()
percent.set("Entrada:") 
percentLabel = Label(ws,textvariable=percent).pack()

text2 = StringVar()
text2.set("Estado entrada:") 
task2Label = Label(ws,textvariable=text2).pack()


percent2 = StringVar()
percent2.set("Saida:") 
percent2Label = Label(ws,textvariable=percent2).pack()

text = StringVar()
text.set("Estado saida:") 
taskLabel = Label(ws,textvariable=text).pack()

tem = StringVar()
tem.set("Tempo:") 
taskLabel2 = Label(ws,textvariable=tem).pack()


img = PhotoImage(file="control.png", width=300,height=250)
label_imagem = Label(ws, image=img).pack()
bar = Progressbar(ws,orient=HORIZONTAL,length=300)
bar.pack(pady=10)

button1 = Button(ws, text="Stop",command=b2,state=DISABLED)
button2 = Button(ws, text="Start",command = b1)
button1.pack(side=LEFT)
button2.pack(side=RIGHT)


plot_button = Button(master = ws,command = plot,height = 2,width = 10,text = "Plotar") 
plot_button.pack()


ws.update()


# In[ ]:





# In[ ]:


#CLiente protocolo UPC UA
ENDPOINT = "opc.tcp://192.168.0.123:4840"
NAMESPACE = "OPCUA"

l_aux = []
l_node = []
class MyHandler(SubHandler):
    def __init__(self):
        self._queue = asyncio.Queue()

    def datachange_notification(self, node: Node, value, data: DataChangeNotif) -> None:
        self._queue.put_nowait([node, value, data])

    async def process(self) -> None:

        try:
            while True:
                # Get data in a queue.
                [node, value, data] = self._queue.get_nowait()
                path = await node.get_path(as_string=True)
                l_aux.append(value)
                l_node.append(node)
                if(node == l_node[0]):
                    await monitoramento(l_aux, 0)
                
                else: 
                    await monitoramento(l_aux, 1)

                atualiza()
                ws.update()


        except asyncio.QueueEmpty:
            ws.update()
            
            
            pass

        
        
        
async def main() -> None:
    async with Client(url=ENDPOINT) as client:
        # Get a variable node.
        idx = await client.get_namespace_index(NAMESPACE)
        node = await client.get_objects_node().get_child([f'{idx}:MyObject', f'{idx}:Potenciometro'])
        node1 = await client.get_objects_node().get_child([f'{idx}:MyObject', f'{idx}:Sinal'])
       
        
        # Subscribe data change.
        handler = MyHandler()
        subscription = await client.create_subscription(period=0, handler=handler)
        await subscription.subscribe_data_change(node)
        await subscription.subscribe_data_change(node1)


        # Process data change every
        while True:
            await handler.process()
            await asyncio.sleep(0.001)
            
#Funcao main
if __name__ == '__main__':
    await main()


# In[ ]:





# In[ ]:





# In[ ]:




