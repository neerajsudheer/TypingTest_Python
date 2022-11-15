from tkinter import *
import ctypes
import time
import threading
import random
import tkinter
from tkinter import Label
from PIL import ImageTk, Image
import numpy as np 
import matplotlib.pyplot as plt
import mysql.connector as a
con = a.connect(host="localhost",user="root",passwd="",database="typingtest")
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Function : Customer Login   
def funcCustomerLogin():
      root = Tk()

      root.title("Typing Test LOGIN")
      # Setting the Font for all Labels and Buttons
      root.option_add("*Label.Font", "consolas 30")
      root.option_add("*Button.Font", "consolas 30")
      root.geometry("425x325")
      mylabel1 = Label(root,text="       ",bd="45")

      mylabel2 = Label(root,text="LOGIN PAGE",anchor=CENTER,bg="light yellow",bd="20")

      mylabel3 = Label(root,text="Login with your username and password")

      mylabel4 = Label(root,text="UserName:")

      mylabel5 = Label(root,text="Password:")

      myentry1= Entry(root,width=50)
      l1=Label(root,text="Typing Test",bd=20,anchor=CENTER,relief="ridge",bg="light yellow",width=12,font=('arial', 40, 'bold'))
      l1.place(x=600,y=0)


      myentry2= Entry(root,show="*",width=50)
      ac= myentry1.get()
      
      def login(a=myentry1,b=myentry2):
          ac= a.get()
          a="select password from user where user_name=%s"
          data=(ac,)
          c=con.cursor()
          c.execute(a,data)
          myresult=c.fetchone()
          if b.get()== myresult[0] :
                      nonlocal myentry1
                      d = myentry1
                      message = "Login Sucessful"
                      message2 ="Proceeding to the Main Page"
                      lb4 = Label(root, text = message,fg="green")
                      lb5 = Label(root, text = message2,fg="green")
                      lb4.grid(row=6, column =2)
                      lb5.grid(row=7, column =2)

                      root1 = Tk()
                      root1.title('Type Speed Test')

                      # Setting the starting window dimensions
                      root1.geometry('700x700')

                      # Setting the Font for all Labels and Buttons
                      root1.option_add("*Label.Font", "consolas 30")
                      root1.option_add("*Button.Font", "consolas 30")

                      def resetWritingLabels():
                          # Text List
                          possibleTexts = [
                              'For writers, a random sentence can help them get their creative juices flowing. Since the topic of the sentence is completely unknown, it forces the writer to be creative when the sentence appears. There are a number of different ways a writer can use the random sentence for creativity. The most common way to use the sentence is to begin a story. Another option is to include it somewhere in the story. A much more difficult challenge is to use it to end a story. In any of these cases, it forces the writer to think creatively since they have no idea what sentence will appear from the tool.',
                              'The goal of Python Code is to provide Python tutorials, recipes, problem fixes and articles to beginner and intermediate Python programmers, as well as sharing knowledge to the world. Python Code aims for making everyone in the world be able to learn how to code for free. Python is a high-level, interpreted, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.',
                              'As always, we start with the imports. Because we make the UI with tkinter, we need to import it. We also import the font module from tkinter to change the fonts on our elements later. We continue by getting the partial function from functools, it is a genius function that excepts another function as a first argument and some args and kwargs and it will return a reference to this function with those arguments. This is especially useful when we want to insert one of our functions to a command argument of a button or a key binding.'
                          ]
                          # Chosing one of the texts randomly with the choice function
                          text = random.choice(possibleTexts).lower()

                          # defining where the text is split
                          splitPoint = 0
                          global label1
                          label1 = Label(root1, text="Hello "+ac.upper()+" !\n Welcome to Typing Speed Test", fg='grey')
                          label1.place(relx=0.7, rely=0.1, anchor=E)
                          # This is where the text is that is already written
                          global labelLeft
                          labelLeft = Label(root1, text=text[0:splitPoint], fg='grey')
                          labelLeft.place(relx=0.5, rely=0.5, anchor=E)

                          # Here is the text which will be written
                          global labelRight
                          labelRight = Label(root1, text=text[splitPoint:])
                          labelRight.place(relx=0.5, rely=0.5, anchor=W)

                              # This label shows the user which letter he now has to press
                          global currentLetterLabel
                          currentLetterLabel = Label(root1, text=text[splitPoint], fg='grey')
                          currentLetterLabel.place(relx=0.5, rely=0.6, anchor=N)

                          # this label shows the user how much time has gone by
                          global timeleftLabel
                          timeleftLabel = Label(root1, text=f'0 Seconds', fg='grey')
                          timeleftLabel.place(relx=0.5, rely=0.4, anchor=S)

                          global writeAble
                          writeAble = True
                          root1.bind('<Key>', keyPress)

                          global passedSeconds
                          passedSeconds = 0

                          # Binding callbacks to functions after a certain amount of time.
                          root1.after(60000, stopTest)
                          root1.after(1000, addSecond)

                      def stopTest():
                          global writeAble
                          writeAble = False

                          # Calculating the amount of words
                          global amountWords
                          amountWords = len(labelLeft.cget('text').split(' '))

                          # Destroy all unwanted widgets.
                          timeleftLabel.destroy()
                          currentLetterLabel.destroy()
                          labelRight.destroy()
                          labelLeft.destroy()

                              # Display the test results with a formatted string
                          global ResultLabel
                          ResultLabel = Label(root1, text=f'Words per Minute: {amountWords}', fg='black')
                          ResultLabel.place(relx=0.5, rely=0.4, anchor=CENTER)
                          data1= [ac,amountWords]
                          sql1="insert into user_speed values(%s,%s)"
                          c=con.cursor()
                          c.execute(sql1,data1)
                          con.commit()

                          # Display a button to restart the game
                          global ResultButton
                          ResultButton = Button(root1, text=f'Retry', command=restart)
                          ResultButton.place(relx=0.5, rely=0.6, anchor=CENTER)

                          def graphspeed():
                              plt.style.use('Solarize_Light2')
                              a="select type_speed from user_speed where user_name=%s"
                              data=(ac,)
                              c1=con.cursor()
                              c1.execute(a,data)
                              values=c1.fetchall()
                              newvalues=list()
                              for i in values :
                                  i = str(i)
                                  i=i.strip("(")
                                  i=i.strip(")")
                                  i=i.strip(",")
                                  newvalues.append(int(i))
                              num=len(newvalues)+1
                              number=list(range(num))
                              number= number[1:]
                              plt.plot(number, newvalues)
                              plt.axis([0, num, 0, 150])
                              plt.xlabel('Attempt No')
                              plt.ylabel('Typing Speed')
                              plt.title('Typing Speed Graph for '+ac.upper())
                              plt.show()

                          global Button1
                          Button1 = Button(root1, text=f'Past Perfomance Graph', command=graphspeed)
                          Button1.place(relx=0.5, rely=0.9, anchor=CENTER)

                      def restart():
                          # Destry result widgets
                          ResultLabel.destroy()
                          ResultButton.destroy()

                          # re-setup writing labels.
                          resetWritingLabels()

                      def addSecond():
                          # Add a second to the counter.

                          global passedSeconds
                          passedSeconds += 1
                          timeleftLabel.configure(text=f'{passedSeconds} Seconds')

                          # call this function again after one second if the time is not over.
                          if writeAble:
                              root1.after(1000, addSecond)

                      def keyPress(event=None):
                          try:
                              if event.char.lower() == labelRight.cget('text')[0].lower():
                                  # Deleting one from the right side.
                                  labelRight.configure(text=labelRight.cget('text')[1:])
                                  # Deleting one from the right side.
                                  labelLeft.configure(text=labelLeft.cget('text') + event.char.lower())
                                  #set the next Letter Lavbel
                                  currentLetterLabel.configure(text=labelRight.cget('text')[0])
                          except tkinter.TclError:
                              pass

                      # This will start the Test
                      resetWritingLabels()
                      root1.attributes('-fullscreen',True)
                      # Start the mainloop
                      root1.mainloop()


          else:
                      message = "Invalid Account Number or Password "
                      lb4 = Label(root, text = message,fg="red")
                      lb4.grid(row=6, column =2)

       
      mybutton1 = Button(root,text="Login",command=login)

      mybutton2 = Button(root,text="New user?, Create new account",command=funcNewUser)            
          
         
      mylabel1.grid(row=1, column =2)
      mylabel2.grid(row=2, column=2)
      mylabel3.grid(row=3, column =2)
      mylabel4.grid(row=4)
      mylabel5.grid(row=5)
      myentry1.grid(row=4 , column =2)
      myentry2.grid(row=5,column=2)
      mybutton1.grid(row=8, column =2)
      mybutton2.grid(row=9, column =2)
      root.attributes('-fullscreen',True)
      root.mainloop()

def funcNewUser():
      
      root = Tk()
      l1=Label(root,text="")
      l1.grid(row=0,column=0)
      root.title("Typing Test New User[New Account]")
      root.geometry("425x390")
      l1=Label(root,text="Typing Test",bd=20,relief="ridge",bg="light yellow",width=12,font=('arial', 40, 'bold'))
      l1.place(x=650,y=0)
      # Setting the Font for all Labels and Buttons
      root.option_add("*Label.Font", "consolas 30")
      root.option_add("*Button.Font", "consolas 30")
      mylabel2 = Label(root,text="NEW USER",anchor=CENTER,bg="light yellow",bd="20")
      mylabel2.place(x=800,y=150)

      customer_data = []

      l2=Label(root,text="Enter UserName :")
      l2.place(x=350,y=400)
      e = Entry(root,width=50)
      e.place(x=1200,y=420)


      l3=Label(root,text="Enter Password :")
      l3.place(x=350,y=550)
      e2 = Entry(root,show="*",width=50)
      e2.place(x=1200,y=570)

      def funcAddUser():
        if len(e.get()) < 6 or len(e.get()) > 13 or len(e2.get()) == 0 or len(e2.get())<8:
            message = "Minimum Number of characters not met"
            message1 = "                                          "
            lb4 = Label(root, text = message,fg="red")
            lb4.place(x=200,y=850)
            lb5 = Label(root, text = message1,fg="red")
            lb5.place(x=200,y=1000)
        else:
            data1= [e.get(),e2.get()]
            sql1="insert into user values(%s,%s)"
            c=con.cursor()
            c.execute(sql1,data1)
            con.commit()
            message = "   Your account has been sucessfully created "
            message1 = "                                                    "
            lb4 = Label(root, text = message,fg="green")
            lb4.place(x=200,y=850) 
            lb5 = Label(root, text = message1,fg="green")
            lb5.place(x=200,y=1000)
            
      b1 = Button(root,text="Create account",command=funcAddUser)
      b1.place(x=545,y=650) 
      b2 = Button(root,text="Login",command=funcCustomerLogin)
      b2.place(x=1200,y=650)      
      root.attributes('-fullscreen',True)
      root.mainloop()
root=Tk()
root.config(bg="white")
root.title("Typing Test")
root.geometry("780x550")
root.option_add("*Label.Font", "consolas 30")
root.option_add("*Button.Font", "consolas 30")

'''l1=Label(root,text="Typing Test",bd=20,relief="ridge",bg="light yellow",width=12,font=('arial', 40, 'bold'))
l1.place(x=650,y=0)


image = PhotoImage(file="pic.PNG")
img=image.resize((341,256))
Label(root, image=img).place(x=0,y=0)'''
img_old=Image.open('newpic.PNG')
img_resized=img_old.resize((1930,1060)) # new width & height
my_img=ImageTk.PhotoImage(img_resized)
l1=Label(root,image=my_img)
l1.place(x=0,y=0)

bt6 = Button(root,bg="white",text="USER LOGIN",command=funcCustomerLogin,relief="groove")
bt6.place(x=350,y=250)

bt7 = Button(root,bg="white",text="NEW USER",command=funcNewUser,relief="groove")
bt7.place(x=1200,y=250)
root.attributes('-fullscreen',True)
root.mainloop()