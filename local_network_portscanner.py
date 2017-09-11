from PyQt5 import QtWidgets
import sys
import socket
import threading
import re
import queue
from time import localtime, strftime #za vremeto

#to store all entities connected to the network,their ip,open ports and store them
network_entities=[]
entity_ip=[]

current_time=str(strftime("%d-%m-%Y %H_%M_%S", localtime()))
the_report=open(str(current_time)+"_scan.txt","a")

q=queue.Queue()

threads=80
lock=threading.Lock()

#to get the host's local ip
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
host_ip=s.getsockname()[0]

#removing the last digits so we can scan the whole network 
whole_network=re.sub(r"\d{1,3}$",'',host_ip)


class window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initialize_gui()

    def initialize_gui(self):
        self.label1=QtWidgets.QLabel("Number of threads:"+str(threads)+" scan port range is from 0 to 200")
        self.start_full_scan_button=QtWidgets.QPushButton("Start full scan with report")

        
        v_box=QtWidgets.QVBoxLayout()#virtical box
        v_box.addWidget(self.label1)
        v_box.addWidget(self.start_full_scan_button)
 
        
        self.setLayout(v_box)
        
        self.setWindowTitle("local_network_portscanner")

        #all the button functions

        self.start_full_scan_button.clicked.connect(start)


        self.show()
        
            
#the_report.write(socket.gethostbyaddr(entity))            
    
        
#the portscan for  each individual network entity
def portscan(entity,port):
    
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        with lock:
            con=s.connect((entity,port))
            the_report.write("on "+str(entity)+" port "+ str(port)+" is open\n")
            
            
    except:
        pass

    

#the  network scan 
def networkscan():
    with lock:
        for x in range(0,255):
            u=str(whole_network+str(x))
            try:
                m=socket.gethostbyaddr(u)
                network_entities.append(m)
                entity_ip.append(u)
        
            except:
                print(" " )
                pass
        print(u)



def threader():
    while True:
        threads=q.get()
        networkscan()
        q.task_done()


#starts all the functions 
def start():
    for x in range(threads):
        t=threading.Thread(target=threader)
        t.daemon=True
        t.start()

    for x in range(0,1):
        q.put(x)

    q.join()
   

    #the portscanning:
    for x in entity_ip:
        for y in range(0,200):
            portscan(x,y)
    

    the_report.close()
    for x in network_entities:
        del x
    for y in entity_ip:
        del y

app=QtWidgets.QApplication(sys.argv)
a_window=window()
sys.exit(app.exec_())

            



