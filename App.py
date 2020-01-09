import cv2
import tkinter as tk 
import mysql.connector
import numpy as np 
from PIL import Image,ImageTk
from tkinter import messagebox
import os

mydb=mysql.connector.connect(user="root",database="facebase")
mycursor=mydb.cursor()

detect=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')


logData=[]


class App(tk.Tk):
    def __init__ (self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container=tk.Frame(self)

        container.pack(side="top",fill="both",expand=True)
        
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        container.winfo_toplevel().title("Facial Recognition")


        self.frames={}
        for F in(loginPage,adminHome,manageAdmin,manageGuard,createAdmin,createGuard,manageEmployee,createEmployee,guardHome,manageEmployee2,manageGuard2,manageEmployee3,manageClerks,createClerk):
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(loginPage)
    def showFrame(self,page):

        frame=self.frames[page]
        frame.tkraise()
    
        


class loginPage(tk.Frame):
        def __init__(self,parent,controller):
            tk.Frame.__init__(self,parent)
            v= tk.IntVar()
            tk.Label(self,text="WELCOME").grid(row=0,column=1)

            tk.Label(self,text="Enter ID:").grid(row=1,column=0)
            entr1=tk.Entry(self)
            entr1.grid(row=1,column=1)

            tk.Label(self,text="Enter Pin:").grid(row=2,column=0)
            entr2=tk.Entry(self,show="*")
            entr2.grid(row=2,column=1)

            rb1=tk.Radiobutton(self,text="Admin",variable=v,value=1)
            rb1.grid(row=3,column=0)
            rb2=tk.Radiobutton(self,text="Guard",variable=v,value=2)
            rb2.grid(row=3,column=1)
            rb3=tk.Radiobutton(self,text="Clerk",variable=v,value=3)
            rb3.grid(row=3,column=2)

            def  login():
                id=entr1.get()
                pin=entr2.get()

                if v.get()==1:
                    query="SELECT * FROM admin WHERE id=%s AND pin=%s"
                    mycursor.execute(query,(id,pin,))
                    row=mycursor.fetchone()
                    if not row:
                        messagebox.showwarning("Error"," Wrong ID or PIN")
                    else:
                        messagebox.showinfo("Success"," Succesfully Logged In")
                        controller.showFrame(adminHome)
                        logData=row
                elif v.get()==2:
                    query="SELECT * FROM guard WHERE id=%s AND pin=%s"
                    mycursor.execute(query,(id,pin,))
                    row=mycursor.fetchone()
                    if not row:
                        messagebox.showwarning("Error"," Wrong ID or PIN")
                    else:
                        messagebox.showinfo("Success"," Succesfully Logged In")
                        controller.showFrame(guardHome)
                        logData=row
                elif v.get()==3:
                    query="SELECT * FROM clerk WHERE id=%s AND pin=%s"
                    mycursor.execute(query,(id,pin,))
                    row=mycursor.fetchone()
                    if not row:
                        messagebox.showwarning("Error"," Wrong ID or PIN")
                    else:
                        messagebox.showinfo("Success"," Succesfully Logged In")
                        controller.showFrame(manageEmployee)
                        
                    

            

            tk.Button(self,text="Login   " ,command=login).grid(row=4,column=1)
                    
        


class adminHome(tk.Frame):
    def __init__(self,parent,controller):
        def rescaleFrame(frame, percent):
            width = int(frame.shape[1] * percent/ 80)
            height = int(frame.shape[0] * percent/ 70)
            dim = (width, height)
            return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
        tk.Frame.__init__(self,parent)
        fname='Eugene'
        lname='Ikonya'
        def liveFootage():
            cap = cv2.VideoCapture(0)
            recognizer=cv2.face_LBPHFaceRecognizer.create()
            font=cv2.FONT_HERSHEY_SIMPLEX
            if os.path.exists('trainingData/faceData.yml'):
                recognizer.read('trainingData/faceData.yml')
            

            id=0

            while True:
                ret,frame=cap.read()
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces=detect.detectMultiScale(gray,1.3,5)

                for(x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    ID,confidence=recognizer.predict(gray[y:y+h,x:x+w])
                    mycursor.execute("SELECT fullName FROM faceData WHERE id={}".format(ID))
                    rows=mycursor.fetchall()
                    confidence="{0}%".format(round(100-confidence))
                    cv2.putText(frame,str(rows),(x+30,y-10),font,1,(0,0,255),0,2)
                    cv2.putText(frame,str(confidence),(x+5,y+h-5),font,1,(0,0,255),0,1)
                    

                
                cv2.imshow("face",rescaleFrame(frame,50))
                if(cv2.waitKey(1)==ord('q')):
                    break

            cap.release()
            cv2.destroyAllWindows()
        def  viewFlags():
            path='flags'
            path=os.path.realpath(path)
            os.access(path)

        tk.Label(self,text="Admin View").grid(row=0,column=1)

        tk.Button(self,text="View Footage",height=2,width=20,command=liveFootage).grid(row=1,column=0)
        tk.Label(self,text=" ").grid(row=1,column=1)
        tk.Button(self,text="     Manage Guards",height=2,width=20,command=lambda: controller.showFrame(manageGuard)).grid(row=1,column=2)

        tk.Label(self,text=" ").grid(row=2)

        


        tk.Label(self,text=" ").grid(row=4)

        tk.Button(self,text="   Manage Admins  ",height=2,width=20,command=lambda:controller.showFrame(manageAdmin)).grid(row=5,column=0)
        tk.Button(self,text="   Manage Clerks  ",height=2,width=20,command=lambda:controller.showFrame(manageClerks)).grid(row=5,column=1)
        tk.Button(self,text=" Manage Employees",height=2,width=20,command=lambda:controller.showFrame(manageEmployee)).grid(row=5,column=2)


        tk.Label(self,text=" ").grid(row=6)
        tk.Label(self,text=" ").grid(row=7)
        

        homeButton=tk.Button(self,text="Logout",command=lambda :controller.showFrame(loginPage)).grid(row=8,column=1)

        


class manageAdmin(tk.Frame):
     def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        v=tk.StringVar()
        tk.Label(self,text="Admin Profiles").grid(row=0,column=1)
        tk.Label(self,text="ID").grid(row=1,column=1)
        tk.Label(self,text="FIRST NAME").grid(row=1,column=2)
        tk.Label(self,text="LAST NAME").grid(row=1,column=3)
        tk.Label(self,text="AGE").grid(row=1,column=4)
        

        query="SELECT * FROM admin"




        mycursor.execute(query)
        rows=mycursor.fetchall()

        grow=1
        col=0
        count=1

       
        i=0
        for row in rows:
            for i in range(len(row)-1): 
                  
                tk.Radiobutton(self,variable=v,value=row[0]).grid(row=grow+1)
                tk.Label(self,text=row[i]).grid(row=grow+1,column=i+1)
                i+=1
            grow+=1

        def deleteProfile():
            id=str(v.get())
            query1= "DELETE FROM admin WHERE id=%s"
            mycursor.execute(query1,(id,))
            mydb.commit()
           
            
            
            

        btnEdit=tk.Button(self,text="Edit Profile").grid(row=grow+1,column=1)
        btnDelete=tk.Button(self,text="Delete Profile",command=deleteProfile).grid(row=grow+1,column=2)
        btnCreate=tk.Button(self,text="Create Profile",command=lambda:controller.showFrame(createAdmin)).grid(row=grow+1,column=3)
        btnBack=tk.Button(self,text="Back",command=lambda:controller.showFrame(adminHome)).grid(row=10,column=5)

class manageClerks(tk.Frame):
     def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        v=tk.StringVar()
        tk.Label(self,text="Clerk Profiles").grid(row=0,column=1)
        tk.Label(self,text="ID").grid(row=1,column=1)
        tk.Label(self,text="FULL NAME").grid(row=1,column=2)
        tk.Label(self,text="AGE").grid(row=1,column=3)
        tk.Label(self,text="PIN").grid(row=1,column=4)
     

        query="SELECT * FROM clerk"




        mycursor.execute(query)
        rows=mycursor.fetchall()

        grow=1
        col=0
        count=1

        
        i=0
        for row in rows:
            for i in range(len(row)-1): 
                  
                tk.Radiobutton(self,variable=v,value=row[0]).grid(row=grow+1)
                tk.Label(self,text=row[i]).grid(row=grow+1,column=i+1)
                i+=1
            grow+=1

        def deleteProfile():
            id=str(v.get())
            query1= "DELETE FROM clerk WHERE id=%s"
            mycursor.execute(query1,(id,))
            mydb.commit()
           
            
            
            

        btnEdit=tk.Button(self,text="Edit Profile").grid(row=grow+1,column=1)
        btnDelete=tk.Button(self,text="Delete Profile",command=deleteProfile).grid(row=grow+1,column=2)
        btnCreate=tk.Button(self,text="Create Profile",command=lambda:controller.showFrame(createClerk)).grid(row=grow+1,column=3)
        btnBack=tk.Button(self,text="Back",command=lambda:controller.showFrame(adminHome)).grid(row=10,column=5)
class createClerk(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        tk.Label(self,text="Register Clerk").grid(row=0,column=1)

        tk.Label(self,text="Clerk ID:").grid(row=1,column=0)
        entr=tk.Entry(self)
        entr.grid(row=1,column=1)

        tk.Label(self,text="First Name:").grid(row=2,column=0)
        entr1=tk.Entry(self)
        entr1.grid(row=2,column=1)

        tk.Label(self,text="Last Name:").grid(row=3,column=0)
        entr2=tk.Entry(self)
        entr2.grid(row=3,column=1)

        tk.Label(self,text="Age:").grid(row=4,column=0)
        entr3=tk.Entry(self)
        entr3.grid(row=4,column=1)

        tk.Label(self,text="Pin:").grid(row=5,column=0)
        entr4=tk.Entry(self,show="*")
        entr4.grid(row=5,column=1)

        tk.Label(self,text="Confirm Pin:").grid(row=6,column=0)
        entr5=tk.Entry(self,show="*")
        entr5.grid(row=6,column=1)

        tk.Label(self,text="Enter Position").grid(row=7,column=0)
        entr6=tk.Entry(self)
        entr6.grid(row=7,column=1)

        

        def create():
            if entr4.get()==entr5.get():
                query="INSERT INTO clerk(id,fullName,Age,pin, position) VALUES(%s,%s,%s,%s,%s)"
                values=("Clk"+entr.get(),entr1.get()+" "+entr2.get(),entr3.get(),entr4.get(),entr6.get())
                mycursor.execute(query,values)
                mydb.commit()
                
                messagebox.showinfo("Success"," Added Successfully")
                self.destroy()
            else:
                tk.Label(self,text="Pins do not Match").grid(row=9,column=1)


        tk.Button(self,text="     Register Personell      ",command=create).grid(row=10,column=1)
        btnBack=tk.Button(self,text="Back",command=lambda:controller.showFrame(manageAdmin)).grid(row=10,column=5)
        


class createAdmin(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        tk.Label(self,text="Register Personell").grid(row=0,column=1)

        tk.Label(self,text="Personell ID:").grid(row=1,column=0)
        entr=tk.Entry(self)
        entr.grid(row=1,column=1)

        tk.Label(self,text="First Name:").grid(row=2,column=0)
        entr1=tk.Entry(self)
        entr1.grid(row=2,column=1)

        tk.Label(self,text="Last Name:").grid(row=3,column=0)
        entr2=tk.Entry(self)
        entr2.grid(row=3,column=1)

        tk.Label(self,text="Age:").grid(row=4,column=0)
        entr3=tk.Entry(self)
        entr3.grid(row=4,column=1)

        tk.Label(self,text="Pin:").grid(row=5,column=0)
        entr4=tk.Entry(self,show="*")
        entr4.grid(row=5,column=1)

        tk.Label(self,text="Confirm Pin:").grid(row=6,column=0)
        entr5=tk.Entry(self,show="*")
        entr5.grid(row=6,column=1)

        

        def create():
            if entr4.get()==entr5.get():
                query="INSERT INTO admin(id,firstName,lastName,Age,pin) VALUES(%s,%s,%s,%s,%s)"
                values=("Adm"+entr.get(),entr1.get(),entr2.get(),entr3.get(),entr4.get())
                mycursor.execute(query,values)
                mydb.commit()
                messagebox.showinfo("Success"," Added Successfully")
                self.destroy()
            else:
                tk.Label(self,text="Pins do not Match").grid(row=9,column=1)


        tk.Button(self,text="     Register Personell      ",command=create).grid(row=10,column=1)
        btnBack=tk.Button(self,text="Back",command=lambda:controller.showFrame(manageAdmin)).grid(row=10,column=5)

class manageGuard(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        v=tk.IntVar()
        tk.Label(self,text="Guard Profiles").grid(row=0,column=1)
        query="SELECT * FROM guard"
        mycursor.execute(query)
        rows=mycursor.fetchall()
        tk.Label(self,text="ID").grid(row=1,column=1)
        tk.Label(self,text="FIRST NAME").grid(row=1,column=2)
        tk.Label(self,text="LAST NAME").grid(row=1,column=3)
        tk.Label(self,text="AGE").grid(row=1,column=4)
        tk.Label(self,text="PIN").grid(row=1,column=5)
        tk.Label(self,text="ROLE").grid(row=1,column=6)

        grow=2
        i=0
        for row in rows:
            for i in range(len(row)):   
                tk.Radiobutton(self,variable=v,value=str(grow)).grid(row=grow+1)
                tk.Label(self,text=row[i]).grid(row=grow+1,column=i+1)
                i+=1
            grow+=1
        def deleteProfile():
            id=str(v.get())
            query1= "DELETE FROM guard WHERE id=%s"
            mycursor.execute(query1,(id,))
            mydb.commit()
            


        btnEdit=tk.Button(self,text="Edit Profile").grid(row=grow+1,column=1)
        btnDelete=tk.Button(self,text="Delete Profile",command=deleteProfile).grid(row=grow+1,column=2)
        btnCreate=tk.Button(self,text="Create Profile",command=lambda:controller.showFrame(createGuard)).grid(row=grow+1,column=3)
        btnBack=tk.Button(self,text="Back",command=lambda:controller.showFrame(adminHome)).grid(row=grow+1,column=5)

class createGuard(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        tk.Frame.__init__(self,parent)
        tk.Label(self,text="Register Guard").grid(row=0,column=1)

        tk.Label(self,text="Personell ID:").grid(row=1,column=0)
        entr=tk.Entry(self)
        entr.grid(row=1,column=1)

        tk.Label(self,text="First Name:").grid(row=2,column=0)
        entr1=tk.Entry(self)
        entr1.grid(row=2,column=1)

        tk.Label(self,text="Last Name:").grid(row=3,column=0)
        entr2=tk.Entry(self)
        entr2.grid(row=3,column=1)

        tk.Label(self,text="Age:").grid(row=4,column=0)
        entr3=tk.Entry(self)
        entr3.grid(row=4,column=1)

        tk.Label(self,text="Pin:").grid(row=5,column=0)
        entr4=tk.Entry(self,show="*")
        entr4.grid(row=5,column=1)

        tk.Label(self,text="Confirm Pin:").grid(row=6,column=0)
        entr5=tk.Entry(self,show="*")
        entr5.grid(row=6,column=1)

        tk.Label(self,text="Role:").grid(row=7,column=0)
        entr6=tk.Entry(self)
        entr6.grid(row=7,column=1)
        

        def create():
            if entr4.get()==entr5.get():
                query="INSERT INTO guard(id,firstName,lastName,Age,pin,Role) VALUES(%s,%s,%s,%s,%s,%s)"
                values=("Grd"+entr.get(),entr1.get(),entr2.get(),entr3.get(),entr4.get(),entr6.get())
                mycursor.execute(query,values)
                mydb.commit()
                messagebox.showinfo("Success"," Added Successfully")
                self.destroy()
            else:
                tk.Label(self,text="Pins do not Match").grid(row=9,column=1)


        tk.Button(self,text="     Register Personell      ",command=create).grid(row=10,column=1)
        btnBack=tk.Button(self,text="Back",command=lambda:controller.showFrame(manageGuard)).grid(row=10,column=5)

class manageEmployee(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        v=tk.IntVar()
        tk.Label(self,text=" Manage Employees").grid(row=0,column=1)
        query="SELECT * FROM faceData"
        mycursor.execute(query)
        rows=mycursor.fetchall()
        tk.Label(self,text="ID").grid(row=1,column=1)
        tk.Label(self,text="FULL NAME").grid(row=1,column=2)
        tk.Label(self,text="AGE").grid(row=1,column=3)
        tk.Label(self,text="ROLE").grid(row=1,column=4)
        

        grow=2

        for row in rows:
            for i in range(len(row)):   
                tk.Radiobutton(self,variable=v,value=row[0]).grid(row=grow+1)
                tk.Label(self,text=row[i]).grid(row=grow+1,column=i+1)
                i+=1
            grow+=1

        def deleteProfile():
                    id=str(v.get())
                    query1= "DELETE FROM faceData WHERE id=%s"
                    mycursor.execute(query1,(id,))
                    mydb.commit()
    



        btnEdit=tk.Button(self,text="Back",command=lambda:controller.showFrame(adminHome)).grid(row=grow+1,column=3)
        btnDelete=tk.Button(self,text="Delete Profile",command=deleteProfile).grid(row=grow+1,column=1)
        btnCreate=tk.Button(self,text="Create Profile",command=lambda : controller.showFrame(createEmployee)).grid(row=grow+1,column=2)  

class createEmployee(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        tk.Label(self,text="Create Employee").grid(row=0,column=1)

        tk.Label(self,text="Enter ID").grid(row=1,column=0)
        entr1=tk.Entry(self)
        entr1.grid(row=1,column=1)

        tk.Label(self,text="Enter Full Name").grid(row=2,column=0)
        entr2=tk.Entry(self)
        entr2.grid(row=2,column=1)

        tk.Label(self,text="Enter Age:").grid(row=3,column=0)
        entr3=tk.Entry(self)
        entr3.grid(row=3,column=1)

        tk.Label(self,text="Enter Role:").grid(row=4,column=0)
        entr4=tk.Entry(self)
        entr4.grid(row=4,column=1)

        def create():
            query="INSERT INTO faceData VALUES (%s,%s,%s,%s)"
            values=(entr1.get(),entr2.get(),entr3.get(),entr4.get())
            mycursor.execute(query,values)
            mydb.commit()
            messagebox.showinfo("Success"," Added Successfully")
            self.destroy()

        def trainDataSet():
            recognizer=cv2.face_LBPHFaceRecognizer.create()
            path='dataSet'


            def getImagesWithId(path):
                imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
                faces=[]
                IDs=[]
                for imagePath in imagePaths:
                    faceImg=Image.open(imagePath).convert('L')
                    faceNP=np.array(faceImg,'uint8')
                    
                    ID=int(os.path.split(imagePath)[-1].split('.')[1])
                    faces.append(faceNP)
                    IDs.append(ID)
                    cv2.imshow("training",faceNP)
                    cv2.waitKey(20)
                return IDs,faces

            Ids,faces=getImagesWithId(path)
            recognizer.train(faces,np.array(Ids))
            recognizer.write('trainingData/faceData.yml')
            cv2.destroyAllWindows()
            tk.Button(self,text="Create Employee",command=create).grid(row=7,column=1)


        def createDataSet():
            if entr1.get():
                sampleNumber=0
                cap=cv2.VideoCapture(0)
                id=entr1.get()
                def rescale_frame(frame, percent):
                    width = int(frame.shape[1] * percent/ 80)
                    height = int(frame.shape[0] * percent/ 70)
                    dim = (width, height)
                    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

                while True:
                    ret,frame=cap.read()
                    #convert the recorded frame to grayscale
                    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                    #detect the faces from the grayscale frame
                    faces=detect.detectMultiScale(gray,1.3,5)

                    for(x,y,w,h) in faces:
                        #increment the Sample Number
                        sampleNumber=sampleNumber+1
                        print(sampleNumber)
                        #save an image everytime the face is detected inthe dataSets dir
                        cv2.imwrite("dataSet/user."+ str(id)+"."+str(sampleNumber)+".jpg",gray[y:y+h,x:x+h])
                        #add the rectangle around the face
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        #Delay maybe idk????????
                        cv2.waitKey(60)
                    #diaplay The frame

                    cv2.imshow("DataSetCreator",rescale_frame(frame,50))

                    key=cv2.waitKey(1)
                    #if the keyboard value is q stop the program
                    if(key==ord('q')):
                        break   
                    #when 35 dataset photos are taken the program breaks
                    if(sampleNumber==30):
                        break
                    cv2.destroyAllWindows()
                    tk.Button(self,text="Train The data",command=trainDataSet).grid(row=6,column=1)
            else:
                messagebox.showerror("Warning","Please Enter Data")

        tk.Button(self,text="Create Data set",command=createDataSet).grid(row=5,column=1)

class guardHome(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        def rescaleFrame(frame, percent):
            width = int(frame.shape[1] * percent/ 80)
            height = int(frame.shape[0] * percent/ 70)
            dim = (width, height)
            return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
        tk.Frame.__init__(self,parent)
        fname='Eugene'
        lname='Ikonya'
        def liveFootage():
            cap = cv2.VideoCapture(0)
            recognizer=cv2.face_LBPHFaceRecognizer.create()
            font=cv2.FONT_HERSHEY_SIMPLEX
            if os.path.exists('trainingData/faceData.yml'):
                recognizer.read('trainingData/faceData.yml')
           

            id=0

            while True:
                ret,frame=cap.read()
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces=detect.detectMultiScale(gray,1.3,5)

                for(x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    ID,confidence=recognizer.predict(gray[y:y+h,x:x+w])
                    mycursor.execute("SELECT fullName FROM faceData WHERE id={}".format(ID))
                    rows=mycursor.fetchall()
                    confidence="{0}%".format(round(100-confidence))
                    cv2.putText(frame,str(rows),(x+30,y-10),font,1,(0,0,255),0,2)
                    cv2.putText(frame,str(confidence),(x+5,y+h-5),font,1,(0,0,255),0,1)
                   

                
                cv2.imshow("face",rescaleFrame(frame,50))
                if(cv2.waitKey(1)==ord('q')):
                    break

            cap.release()
            cv2.destroyAllWindows()
        def  viewFlags():
            path='flags'
            path=os.path.realpath(path)
            os.access(path)

        tk.Label(self,text="Guard View").grid(row=0,column=1)

        tk.Button(self,text="View Footage",height=2,width=20,command=liveFootage).grid(row=1,column=1)
        tk.Button(self,text="   View Guards",height=2,width=20,command=lambda: controller.showFrame(manageGuard2)).grid(row=2,column=1)


        tk.Button(self,text=" Manage Employees",height=2,width=20,command=lambda:controller.showFrame(manageEmployee2)).grid(row=3,column=1)


        tk.Label(self,text=" ").grid(row=6)
        tk.Label(self,text=" ").grid(row=7)
        

        homeButton=tk.Button(self,text="Logout",command=lambda :controller.showFrame(loginPage)).grid(row=7,column=1)
class manageEmployee2(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        v=tk.IntVar()
        tk.Label(self,text="Manage Employees").grid(row=0,column=1)
        query="SELECT * FROM faceData"
        mycursor.execute(query)
        rows=mycursor.fetchall()
        tk.Label(self,text="ID").grid(row=1,column=1)
        tk.Label(self,text="FULL NAME").grid(row=1,column=2)
        tk.Label(self,text="AGE").grid(row=1,column=3)
        tk.Label(self,text="ROLE").grid(row=1,column=4)

        grow=2

        for row in rows:
            for i in range(len(row)):   
                tk.Radiobutton(self,variable=v,value=row[0]).grid(row=grow+1)
                tk.Label(self,text=row[i]).grid(row=grow+1,column=i+1)
    
                i+=1
            grow+=1

        def deleteProfile():
                    id=str(v.get())
                    query1= "DELETE FROM faceData WHERE id=%s"
                    mycursor.execute(query1,(id,))
                    mydb.commit()
                    



        btnEdit=tk.Button(self,text="Back",command=lambda:controller.showFrame(guardHome)).grid(row=grow+1,column=3)

class manageGuard2(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        v=tk.IntVar()
        tk.Label(self,text="Guard Profiles").grid(row=0,column=1)
        query="SELECT * FROM guard"
        mycursor.execute(query)
        rows=mycursor.fetchall()

        tk.Label(self,text="ID").grid(row=1,column=1)
        tk.Label(self,text="FIRST NAME").grid(row=1,column=2)
        tk.Label(self,text="LAST NAME").grid(row=1,column=3)
        tk.Label(self,text="AGE").grid(row=1,column=4)
        tk.Label(self,text="ROLE").grid(row=1,column=6)

        grow=2
        i=0
        for row in rows:
            for i in range(len(row)): 
                if i==4:
                    continue  
                tk.Radiobutton(self,variable=v,value=str(grow)).grid(row=grow+1)
                tk.Label(self,text=row[i]).grid(row=grow+1,column=i+1)
                i+=1
            grow+=1
        def deleteProfile():
            id=str(v.get())
            query1= "DELETE FROM guard WHERE id=%s"
            mycursor.execute(query1,(id,))
            mydb.commit()
            


     
        btnBack=tk.Button(self,text="Back",command=lambda:controller.showFrame(guardHome)).grid(row=grow+1,column=5)
class manageEmployee3(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        v=tk.IntVar()
        tk.Label(self,text=" Data Entry Clerk View").grid(row=0,column=1)
        query="SELECT * FROM faceData"
        mycursor.execute(query)
        rows=mycursor.fetchall()
        tk.Label(self,text="ID").grid(row=1,column=1)
        tk.Label(self,text="FULL NAME").grid(row=1,column=2)
        tk.Label(self,text="AGE").grid(row=1,column=3)
        tk.Label(self,text="ROLE").grid(row=1,column=4)

        grow=2

        for row in rows:
            for i in range(len(row)):   
                tk.Radiobutton(self,variable=v,value=row[0]).grid(row=grow+1)
                tk.Label(self,text=row[i]).grid(row=grow+1,column=i+1)
                i+=1
            grow+=1

        def deleteProfile():
                    id=str(v.get())
                    query1= "DELETE FROM faceData WHERE id=%s"
                    mycursor.execute(query1,(id,))
                    mydb.commit()
                   



        btnEdit=tk.Button(self,text="Back",command=lambda:controller.showFrame(adminHome)).grid(row=grow+1,column=3)
        btnDelete=tk.Button(self,text="Delete Profile",command=deleteProfile).grid(row=grow+1,column=1)
        btnCreate=tk.Button(self,text="Create Profile",command=lambda : controller.showFrame(createEmployee)).grid(row=grow+1,column=2)    
     




app=App()
app.mainloop()

