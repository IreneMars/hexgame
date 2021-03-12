from tkinter import * 

#Starting the "popup":
root=Tk()
root.title("Size of the Board")
root.geometry("400x200+700+400")
frame=Frame(root,width=500,height=50)
frame.pack()#Here we put the frame inside the root. 

label1=Label(frame, text="Size:")#The first row of the grid
label1.grid(row=0,column=0,padx=5,pady=5)

size=StringVar()
field=Entry(frame,textvariable=size)#and its input
field.grid(row=0,column=1,padx=10,pady=5)	

var1=StringVar()
var2=StringVar()
def uncheck_other(button_var):
	button_var.set("")

Checkbutton(frame,text="Human",variable=var1,onvalue = "Human", offvalue = "",command=lambda *args: uncheck_other(var2)).grid(row=1,column=0,padx=5,pady=10)
Checkbutton(frame,text="Computer",variable=var2,onvalue = "Computer", offvalue = "",command=lambda *args: uncheck_other(var1)).grid(row=1,column=1,padx=5,pady=10)


message1=StringVar()
message2=StringVar()
label2=Label(frame, text="", textvariable=message1)#Optional row that only appears if a mistake is made completing the form
label3=Label(frame, text="", textvariable=message2)#Optional row that only appears if a mistake is made completing the form
#That's why grid() method is not called here.
#We'll make it appear later once we check if there is an error.

#VARIABLE PASSED TO THE MAIN CLASS: BOARD_SIZE
board_size=0
first_player=""

#Method called by the button 'OK'
def sendValues(size_value,player_value,computer_value):	
	res=size_value
	print("player:",player_value)
	print("computer:",computer_value)
	if res.isdigit()==False:
		message1.set("That value is not correct.")#ERROR2: not an int value
		label2.grid(row=3,column=0,padx=5,pady=0,columnspan=2)
		if player_value=="" and computer_value=="":
			message1.set("That value is not correct and \nyou must select the first player.")#ERROR2: not an int value
			label2.grid(row=3,column=0,padx=5,pady=0,columnspan=2)	
	
	elif res.isdigit() and (player_value!="" or computer_value!=""):
		if 2<int(res)<17:			
			global board_size
			global first_player
			board_size=int(res)#board_size takes the VALID value of the input
			if player_value!="":
				first_player=player_value
			else:
				first_player=computer_value			
			print(board_size)
			print(first_player)
			root.destroy()#FINE		
		else:		
			message1.set("That size is not available.")#ERROR1
			label2.grid(row=3,column=0,padx=5,pady=0,columnspan=2)
		
	elif res.isdigit() and player_value=="" and computer_value=="":	
		if int(res)<3 or int(res)>=17:
			message1.set("That size is not available and \nyou must select the first player.")#ERROR2: not an int value
			label2.grid(row=3,column=0,padx=5,pady=0,columnspan=2)
		else:
			message1.set("You must select the first player.")#ERROR2: not an int value
			label2.grid(row=3,column=0,padx=5,pady=0,columnspan=2)	
	
	
	
button=Button(frame,text="OK", command=lambda *args: sendValues(size.get(),var1.get(),var2.get()))#The 'OK' button
button.grid(row=2,column=0,pady=10,columnspan=2)

root.mainloop()#Here finishes the context of the loop. 
#The loop ends if you close it manually ('x') or if you enter a valid number




			