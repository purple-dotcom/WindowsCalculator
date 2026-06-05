import tkinter as tk
import tkinter.messagebox

root = tk.Tk()
root.title('Calci')

frame = tk.Frame(root, bg="darkgray", padx=10, pady=10)
frame.pack()

entry = tk.Entry(frame, relief=tk.SUNKEN, borderwidth=3, width=30, takefocus=False, state='readonly')
entry.grid(row=0, column=0, columnspan=4, padx=2, pady=2)
entry.insert(0, '0')

normal_buttons = [                                         ('/', 2, 3),
                    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('×', 3, 3),
                    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('−', 4, 3),
                    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
                                 ('0', 6, 1), ('.', 6, 2)
                ]

def delete_insert(x):
    entry.config(state='normal')
    entry.delete(0,tk.END)
    entry.insert(0,x)
    entry.config(state='readonly')

operators = ['+','−','×','/','%']
def click(char):
    curr = entry.get()
    if curr == '0':  #curr is 0
        if char in operators or char == '0': #if entered char is an op or 0
            if char == '−': #only allow '-' to be written
                delete_insert(char)
                return
            else: 
                return
        elif char == '.': #allow '.' to be entered if curr is 0, then return
            entry.config(state='normal')
            entry.insert(tk.END, char)
            entry.config(state='readonly')
            return
        delete_insert(char) #if entered char is not an op nor 0 nor '.', replace 0 with it (numbers)
        
    elif char in operators: #if entered char is an op (for when curr is not 0)
        if curr[-1] not in operators: #if the last char of curr is not an op
            entry.config(state='normal')
            entry.insert(tk.END, char)
            entry.config(state='readonly')

    else: #if curr is not 0, nor the entered char is '.', enter normally
        entry.config(state='normal')
        entry.insert(tk.END, char)
        entry.config(state='readonly')

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
        delete_insert(r)
    except Exception:
        tkinter.messagebox.showinfo("Error", "Syntax Error!")
        entry.config(state='normal')
        entry.delete(0, tk.END)
        entry.config(state='readonly')
tk.Button(frame, text='=', padx=15, pady=5, bg='black', fg='white', width=3, command=equal).grid(row=6,column=3)

def clear_all():
    delete_insert('0')
tk.Button(frame, text='C', padx=15, pady=5, bg='black', fg='white', width=3, command= clear_all).grid(row=1,column=2)

def backspace():
    curr = entry.get()
    if len(curr) > 1:
        entry.config(state='normal')
        entry.delete(len(curr)-1, tk.END)
        entry.config(state='readonly')
    else:
        delete_insert('0')
tk.Button(frame, text='⌫', padx=15, pady=5, bg='black', fg='white', width=3, command= backspace).grid(row=1,column=3)


def clear_till_last_op():
    curr = entry.get()
    if not any(op in curr for op in operators):
        clear_all()
        return
    while entry.get()[-1] not in operators:
        entry.config(state='normal')
        entry.delete(len(entry.get())-1, tk.END)
        entry.config(state='readonly')
    if entry.get() == '−' or entry.get() == '-':
        clear_all()
tk.Button(frame, text='CE', padx=15, pady=5, bg='black', fg='white', width=3, command= clear_till_last_op).grid(row=1,column=1)

def inverse():
    curr = entry.get()
    try:
        if not any(op in curr for op in operators):
            result = float(curr) ** -1
            r = clean_result(result)
            delete_insert(r)

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
            delete_insert(new_expression)
            
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
            delete_insert(new_expression)
            
    except ZeroDivisionError:
        tkinter.messagebox.showerror("Error", "Cannot divide by zero!")
tk.Button(frame, text='1/x', padx=15, pady=5, bg='black', fg='white', width=3, command=inverse).grid(row=2,column=0)

def square():
    curr = entry.get()
    # only number
    if not any(op in curr for op in operators):
        result = float(curr) ** 2
        r = clean_result(result)
        delete_insert(r)

    # expression ends w operator
    elif curr[-1] in operators:
        i = len(curr) - 1
        no_b4_op = ''
        while i > 0 and curr[i-1] not in operators:
            no_b4_op += curr[i-1]
            i -= 1
        no_b4_op = no_b4_op[::-1]

        #handle -x-
        if curr[0] == '−':
            no_b4_op = '-'+ no_b4_op

        result = float(no_b4_op) ** 2
        r = clean_result(result)
        new_expression = curr + r
        delete_insert(new_expression)
    
    # expression contains number after operator
    else:
        i = len(curr) - 1
        last_num = ''
        while curr[i] not in operators:
            last_num += curr[i]
            i -= 1
        last_num = last_num[::-1]
            
        result = float(last_num) ** 2
        r = clean_result(result)

        #handle -x
        if curr[0] == '−':
            delete_insert(r)
            return
        
        new_expression = curr[:i+1] + r
        delete_insert(new_expression)
tk.Button(frame, text='x^2', padx=15, pady=5, bg='black', fg='white', width=3, command=square).grid(row=2,column=1)

def square_root():
    curr = entry.get()
    try:
        # expression is just one number
        if not any(op in curr for op in operators):
            # handle -x
            if float(curr) < 0:
                tkinter.messagebox.showerror("Error", "Invalid square root!")
                return
            result = float(curr) ** (1/2)
            r = clean_result(result)
            delete_insert(r)

        # expression ends with operator
        elif curr[-1] in operators:
            i = len(curr) - 1
            no_b4_op = ''
            while i > 0 and curr[i-1] not in operators:
                no_b4_op += curr[i-1]
                i -= 1
            no_b4_op = no_b4_op[::-1]

            # handle -x-
            if curr[0] == '−' and curr.count('−') == 2:
                # # DOUBT
                # no_b4_op = '-' + no_b4_op
                # if float(no_b4_op) < 0:
                    tkinter.messagebox.showerror("Error", "Invalid square root!")
                    return
            result = float(no_b4_op) ** (1/2)
            r = clean_result(result)
            new_expression = curr + r
            delete_insert(new_expression)

        # expression ends with number
        else:
            i = len(curr) - 1
            last_num = ''
            while curr[i] not in operators:
                last_num += curr[i]
                i -= 1
            last_num = last_num[::-1]
            result = float(last_num) ** (1/2)
            r = clean_result(result)
            new_expression = curr[:i+1] + r
            delete_insert(new_expression)
    except:
        tkinter.messagebox.showerror("Error", "Invalid square root!")
tk.Button(frame, text='√x', padx=15, pady=5, bg='black', fg='white', width=3, command=square_root).grid(row=2,column=2)

def percentage():
    curr = entry.get()

    if not any(op in curr for op in operators):
        delete_insert('0')

    elif curr[-1] in operators:
        no_b4_op = ''
        i = len(curr) - 1
        while i > 0 and curr[i-1] not in operators:
            no_b4_op += curr[i-1]
            i -= 1
        no_b4_op = no_b4_op[::-1]
        result = float(no_b4_op) * float(no_b4_op)/100
        r = clean_result(result)
        new_expression = curr + r
        delete_insert(new_expression)

    else:
        i = len(curr) - 1
        last_num = ''
        while i >= 0 and curr[i] not in operators:
            last_num += curr[i]
            i -= 1
        last_num = last_num[::-1]
        op_index = i  # i now sits on the operator

        j = op_index - 1
        second_last_num = ''
        while j >= 0 and curr[j] not in operators:
            second_last_num += curr[j]
            j -= 1
        second_last_num = second_last_num[::-1]

        result = float(last_num) / 100 * float(second_last_num)
        r = clean_result(result)
        new_expression = curr[:op_index + 1] + r
        delete_insert(new_expression)
tk.Button(frame, text='%', padx=15, pady=5, bg='black', fg='white', width=3, command=percentage).grid(row=1,column=0)

def keyboard_handler(event):
    if event.keysym == 'Return':
        equal()
    elif event.keysym == 'BackSpace':
        backspace()
    elif event.keysym == 'Delete':
        clear_till_last_op()
    elif event.char in '0123456789.':
        click(event.char)
    elif event.char in '+-*/':
        char = event.char.replace('*', '×').replace('-', '−')
        click(char)
root.bind("<Key>", keyboard_handler)
root.mainloop()