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
    if curr == '0':  #curr is 0
        if char in operators or char == '0': #if entered char is an op or 0
            if char == '−': #only allow '-' to be written
                entry.delete(0,tk.END)
                entry.insert(0, char)
                return
            else: 
                return
        elif char == '.': #allow '.' to be entered if curr is 0, then return
            entry.insert(tk.END, char)
            return
        entry.delete(0, tk.END) #if entered char is not an op nor 0 nor '.', replace 0 with it (numbers)
        entry.insert(0, char)

    elif char in operators: #if entered char is an op (for when curr is not 0)
        if curr[-1] not in operators: #if the last char of curr is not an op
            entry.insert(tk.END, char)

    else: #if curr is not 0, nor the entered char is '.', enter normally
        entry.insert(tk.END, char)

for txt, r, c in normal_buttons:
    tk.Button(frame, text=txt, padx= 15, pady= 5,bg='black', fg='white', width=3, command= lambda t = txt : click(t)).grid(row=r, column=c, padx=2, pady=2)

def clean_result(result):
    result = str(result)
    if result.endswith('.0'):
        result = result[:-2]
    return result

def equal():
    expression = entry.get()
    expression = expression.replace('×', '*')
    expression = expression.replace('−', '-')
    try:
        result = eval(expression)
        r = clean_result(result)
        r = r.replace('-','−')
        entry.delete(0, tk.END)
        entry.insert(0, r)
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
    if len(curr) > 1:
        entry.delete(len(curr)-1, tk.END)
    else:
        entry.delete(0, tk.END)
        entry.insert(0, '0')
tk.Button(frame, text='⌫', padx=15, pady=5, bg='black', fg='white', width=3, command= backspace).grid(row=1,column=3)


def clear_till_last_op():
    curr = entry.get()
    if not any(op in curr for op in operators):
        clear_all()
        return
    while entry.get()[-1] not in operators:
        entry.delete(len(entry.get())-1, tk.END)
    if entry.get() == '−' or entry.get() == '-':
        clear_all()
tk.Button(frame, text='CE', padx=15, pady=5, bg='black', fg='white', width=3, command= clear_till_last_op).grid(row=1,column=1)

def inverse():
    curr = entry.get()
    try:
        if not any(op in curr for op in operators):
            result = float(curr) ** -1
            r = clean_result(result)
            entry.delete(0, tk.END)
            entry.insert(0, r)

        elif curr[-1] in operators:
            i = len(curr)-1
            no_b4_op = ''
            while i > 0 and curr[i-1] not in operators:
                no_b4_op += curr[i-1]
                i -= 1
            no_b4_op = no_b4_op[::-1]
            result = float(no_b4_op) ** -1

            r = clean_result(result)
            new_expression = curr + r
            entry.delete(0, tk.END)
            entry.insert(0, new_expression)
            
        else:
            i = len(curr) - 1
            last_num = ''
            while curr[i] not in operators:
                last_num += curr[i]
                i -= 1
            last_num = last_num[::-1]
            result = float(last_num) ** -1

            r = clean_result(result)
            new_expression = curr[:i+1] + r
            entry.delete(0, tk.END)
            entry.insert(0, new_expression)
            
    except ZeroDivisionError:
        tkinter.messagebox.showerror("Error", "Cannot divide by zero!")
tk.Button(frame, text='1/x', padx=15, pady=5, bg='black', fg='white', width=3, command=inverse).grid(row=2,column=0)

def square():
    curr = entry.get()
    if not any(op in curr for op in operators):
        result = float(curr) ** 2
        r = clean_result(result)
        entry.delete(0, tk.END)
        entry.insert(0, r)

    elif curr[-1] in operators:
        i = len(curr) - 1
        no_b4_op = ''
        while i > 0 and curr[i-1] not in operators:
            no_b4_op += curr[i-1]
            i -= 1
        no_b4_op = no_b4_op[::-1]
        result = float(no_b4_op) ** 2
        r = clean_result(result)
        new_expression = curr + r
        entry.delete(0, tk.END)
        entry.insert(0, new_expression)

    else:
        i = len(curr) - 1
        last_num = ''
        while curr[i] not in operators:
            last_num += curr[i]
            i -= 1
        last_num = last_num[::-1]
        result = float(last_num) ** 2
        r = clean_result(result)
        new_expression = curr[:i+1] + r
        if new_expression[0] == '−':
            new_expression = new_expression[1:]
        entry.delete(0, tk.END)
        entry.insert(0, new_expression)
tk.Button(frame, text='x^2', padx=15, pady=5, bg='black', fg='white', width=3, command=square).grid(row=2,column=1)

def square_root():
    curr = entry.get()
    if not any(op in curr for op in operators):
        result = float(curr)** (1/2)
        r = clean_result(result)
        entry.delete(0, tk.END)
        entry.insert(0, r)

    elif curr[-1] in operators:
        i = len(curr)-1
        no_b4_op = ''
        while curr[i-1] not in operators:
            no_b4_op += curr[i-1]
            i -= 1
            pass

tk.Button(frame, text='√x', padx=15, pady=5, bg='black', fg='white', width=3, command=square_root).grid(row=2,column=2)

def percentage():
    curr = entry.get()
    if not any(op in curr for op in operators):
        entry.delete(0, tk.END)
        entry.insert(0,'0')
    else:
        #keep looking for the last op from the end. then keep looking till you find the start or another operator. that's the no entered last. on this no will the percentage be calculated.
        #
        pass
        


root.mainloop()

#to-do:

#bind keyboard keys
#pressing '=' or Enter evaluates the expression
#disable direct typing into the entry widget
#all input should happen only through button presses / keybind handlers

#implement percentage operator properly:
#if expression has no operators, clear and enter 0. 
#if '%' clicked after operator, return x%. (x is the no b4 op). eg 7+% -> 7 + 7% of 7
#if '%' clicked after number(n), return n% of x. (x is the no b4 op). eg 7 + 9% -> 7 + 9% of 7
#if expression is x op1 y op2 and so on, RETURN TO THIS. FUNCTION UNCLEAR!!

#implement: 1/x,x²,√x. these operations should apply only to the most recently entered number
#examples:
#7+ -> x² => 7+49
#7×9 -> √x => 7×3
#8 -> 1/x => 0.125

#space bar behavior:
#repeat the last valid digit entered
#do nothing if the last character is an operator or a decimal point
#dont add space itself

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
#backspace should restore '0' if expression becomes empty
#if first entered char is a decimal, append it to the 0
#pressing 'CE' clears only the current number being entered (clear till last operator) (except when the exp is -x, then CE will clear everything)
#1/x and x^2 completed