import tkinter as tk
import tkinter.messagebox

root = tk.Tk()
root.title('Calci')

frame = tk.Frame(root, bg="darkgray", padx=10, pady=10)
frame.pack()

entry = tk.Entry(frame, relief=tk.SUNKEN, borderwidth=3, width=30)
entry.grid(row=0, column=0, columnspan=4, padx=2, pady=2)
entry.insert(0, '0')

normal_buttons = [                                         ('/', 2, 3),
                    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('×', 3, 3),
                    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('−', 4, 3),
                    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
                                 ('0', 6, 1), ('.', 6, 2)
                ]

operators = ['+','−','×','/','%']
def click(char):
    curr = entry.get()
    if curr == '0':
        if char in operators or char == '0':
            return
        entry.delete(0, tk.END)
        entry.insert(0, char)

    elif char in operators:
        if curr[-1] not in operators:
            entry.insert(tk.END, char)

    else:
        entry.insert(tk.END, char)

for txt, r, c in normal_buttons:
    tk.Button(frame, text=txt, padx= 15, pady= 5,bg='black', fg='white', width=3, command= lambda t = txt : click(t)).grid(row=r, column=c, padx=2, pady=2)

def equal():
    expression = entry.get()
    expression = expression.replace('×', '*')
    expression = expression.replace('−', '-')
    try:
        result = str(eval(expression))
        if result.endswith('.0'):
            result = result[:-2]
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except:
        tkinter.messagebox.showinfo("Error", "Syntax Error!")
        entry.delete(0, tk.END)
tk.Button(frame, text='=', padx=15, pady=5, bg='black', fg='white', width=3, command=equal).grid(row=6,column=3)

def clear_all():
    entry.delete(0, tk.END)
    entry.insert(0, '0')
tk.Button(frame, text='C', padx=15, pady=5, bg='black', fg='white', width=3, command= clear_all).grid(row=1,column=2)

def backspace():
    curr = entry.get()
    if curr:
        entry.delete(len(curr)-1, tk.END)
tk.Button(frame, text='⌫', padx=15, pady=5, bg='black', fg='white', width=3, command= backspace).grid(row=1,column=3)


def clear_till_last_op():
    curr = entry.get()
    if curr:
        if any(op in curr for op in operators):
            pass
        else:
            clear_all()
tk.Button(frame, text='CE', padx=15, pady=5, bg='black', fg='white', width=3, command= clear_till_last_op).grid(row=1,column=1)

def inverse():
    curr = entry.get()
    if any(op in curr for op in operators):
        tkinter.messagebox.showerror("Error", "Invalid input!")
        return
    try:
        result = str(float(curr)**-1)
        if result.endswith('.0'):
            result = result[:-2]
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except ZeroDivisionError:
        tkinter.messagebox.showerror("Error", "Cannot divide by zero!")
tk.Button(frame, text='1/x', padx=15, pady=5, bg='black', fg='white', width=3, command=inverse).grid(row=2,column=0)

def square():
    curr = entry.get()
    if any(op in curr for op in operators):
        tkinter.messagebox.showerror("Error", "Invalid input!")
        return
    result = str(float(curr)**2)
    if result.endswith('.0'):
            result = result[:-2]
    entry.delete(0, tk.END)
    entry.insert(0, result)
tk.Button(frame, text='x^2', padx=15, pady=5, bg='black', fg='white', width=3, command=square).grid(row=2,column=1)

def square_root():
    curr = entry.get()
    if any(op in curr for op in operators):
        tkinter.messagebox.showerror("Error", "Invalid input!")
        return
    result = str(float(curr)**(1/2))
    if result.endswith('.0'):
            result = result[:-2]
    entry.delete(0, tk.END)
    entry.insert(0, result)
tk.Button(frame, text='√x', padx=15, pady=5, bg='black', fg='white', width=3, command=square_root).grid(row=2,column=2)

def percentage():
    curr = entry.get()

root.mainloop()

#to-do:
#clear_till_last_op() -> CE 
#add a section above entry, call it b2 while main entry widget is b1. Entering an operator will put the whole expression up until that point into b2, while b1 still shows the number entered b4 the operator. Entering a new number will directly replace the no. in b1. Pressing '=' or pressing 'enter' will clear b2 and show result in b1. Pressing 'CE' will clear b1 and make it 0, b2 will remain. Pressing 'C' will clear everything.
#bind keys
#dont allow to add space 
#rather, dont allow user to write directly in the entry widget
#pressing 'space' bar button repeats the last no. entered, and doesn't repeat if the last char entered was an operator or the decimal point
#percentage operator
#1/x,x^2,x^1/2 all need to be performed on the last entered number (no. showing in b1). The new number after the operation displayed in b1. If b2 was empty, show the particular operation being performed on the number (eg: b2 - 1/(7), b1 - 0.14285....). If b2 was not empty and had an expression (eg:- 7 x ), then the operation being performed will be appended to b2, while the result of the op will be shown in b1 
# (eg b2- 7 x 1/(7), b1 - 0.14285.... ).

#done:
#insert a 0 at the start and after every clear
#prevent entering an operator as the first char
#prevent consecutive operators
#dont allow operator to be entered if the last and only char is 0
#dont allow 0 to be entered if the last and only char is 0
#replace the initial 0 when a digit is entered