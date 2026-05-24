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
#bind keyboard keys
#disable direct typing into the entry widget
#all input should happen only through button presses / keybind handlers
#prevent spaces from being inserted
#pressing '=' or Enter evaluates the expression
#result replaces the entire expression in the entry widget
#pressing 'CE' clears only the current number being entered (clear till last operator)
#implement percentage operator properly
#implement: 1/x,x²,√x. these operations should apply only to the most recently entered number
#examples:
#7+5 -> x² => 7+25
#7×9 -> √x => 7×3
#8 -> 1/x => 0.125

#space bar behavior:
#repeat the last valid digit entered
#do nothing if the last character is an operator or a decimal point

#backspace should restore '0' if expression becomes empty

#handle errors:
#division by zero
#invalid syntax
#invalid square root

#done:
#insert a 0 at the start and after every clear
#prevent entering an operator as the first char
#prevent consecutive operators
#dont allow operator to be entered if the last and only char is 0
#dont allow 0 to be entered if the last and only char is 0
#replace the initial 0 when a digit is entered