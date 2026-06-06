import tkinter as tk
import tkinter.messagebox
import re

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title('Calci')
        self.operators = ['+', '−', '×', '/', '%']
        self.normal_buttons = [                                         ('/', 2, 3),
                                ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('×', 3, 3),
                                ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('−', 4, 3),
                                ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
                                            ('0', 6, 1), ('.', 6, 2)
                            ]

        self.frame = tk.Frame(self.root, bg="darkgray", padx=10, pady=10)
        self.frame.pack()

        self.entry = tk.Entry(self.frame, relief=tk.SUNKEN, borderwidth=3, width=30, takefocus=False, state='readonly')
        self.entry.grid(row=0, column=0, columnspan=4, padx=2, pady=2)
        self.delete_insert('0')

        for txt, r, c in self.normal_buttons:
            tk.Button(self.frame, text=txt, padx= 15, pady= 5,bg='black', fg='white', width=3, command= lambda t = txt : self.click(t)).grid(row=r, column=c, padx=2, pady=2)

        tk.Button(self.frame, text='=', padx=15, pady=5, bg='black', fg='white', width=3, command=self.equal).grid(row=6,column=3)
        tk.Button(self.frame, text='C', padx=15, pady=5, bg='black', fg='white', width=3, command= self.clear_all).grid(row=1,column=2)
        tk.Button(self.frame, text='⌫', padx=15, pady=5, bg='black', fg='white', width=3, command= self.backspace).grid(row=1,column=3)
        tk.Button(self.frame, text='CE', padx=15, pady=5, bg='black', fg='white', width=3, command= self.clear_till_last_op).grid(row=1,column=1)
        tk.Button(self.frame, text='1/x', padx=15, pady=5, bg='black', fg='white', width=3, command=self.inverse).grid(row=2,column=0)
        tk.Button(self.frame, text='x^2', padx=15, pady=5, bg='black', fg='white', width=3, command=self.square).grid(row=2,column=1)
        tk.Button(self.frame, text='√x', padx=15, pady=5, bg='black', fg='white', width=3, command=self.square_root).grid(row=2,column=2)
        tk.Button(self.frame, text='%', padx=15, pady=5, bg='black', fg='white', width=3, command=self.percentage).grid(row=1,column=0)
        self.root.bind("<Key>", self.keyboard_handler)

    def delete_insert(self, x):
        self.entry.config(state='normal')
        self.entry.delete(0,tk.END)
        self.entry.insert(0,x)
        self.entry.config(state='readonly')

    def click(self, char):
        curr = self.entry.get()
        if curr == '0':  #curr is 0
            if char in self.operators or char == '0': #if entered char is an op or 0
                if char == '−': #only allow '-' to be written
                    self.delete_insert(char)
                    return
                else: 
                    return
            elif char == '.': #allow '.' to be entered if curr is 0, then return
                self.entry.config(state='normal')
                self.entry.insert(tk.END, char)
                self.entry.config(state='readonly')
                return
            self.delete_insert(char) #if entered char is not an op nor 0 nor '.', replace 0 with it (numbers)
        
        elif char in self.operators: #if entered char is an op (for when curr is not 0)
            if curr[-1] not in self.operators: #if the last char of curr is not an op
                self.entry.config(state='normal')
                self.entry.insert(tk.END, char)
                self.entry.config(state='readonly')

        else: #if curr is not 0, nor the entered char is '.', enter normally
            self.entry.config(state='normal')
            self.entry.insert(tk.END, char)
            self.entry.config(state='readonly')

    def clean_result(self, result):
        return f"{result:.10g}"

    def equal(self):
        expression = self.entry.get()
        expression = expression.replace('×', '*')
        expression = expression.replace('−', '-')
        try:
            result = eval(expression)
            r = self.clean_result(result)
            r = r.replace('-','−')
            self.delete_insert(r)
        except Exception:
            tkinter.messagebox.showinfo("Error", "Syntax Error!")
            self.clear_all()

    def clear_all(self):
        self.delete_insert('0')

    def backspace(self):
        curr = self.entry.get()
        if len(curr) > 1:
            self.entry.config(state='normal')
            self.entry.delete(len(curr)-1, tk.END)
            self.entry.config(state='readonly')
        else:
            self.delete_insert('0')

    def clear_till_last_op(self):
        curr = self.entry.get()
        if not any(op in curr for op in self.operators):
            self.clear_all()
            return
        self.entry.config(state='normal')
        while self.entry.get()[-1] not in self.operators:
            self.entry.delete(len(self.entry.get())-1, tk.END)
        self.entry.config(state='readonly')
        if self.entry.get() == '−' or self.entry.get() == '-':
            self.clear_all()

    def inverse(self):
        curr = self.entry.get()
        try:
            if not any(op in curr for op in self.operators):
                result = float(curr) ** -1
                r = self.clean_result(result)
                self.delete_insert(r)

            elif curr[-1] in self.operators:
                no_b4_op = re.findall(r'[\d.]+', curr)[-1]
                result = float(no_b4_op) ** -1

                r = self.clean_result(result)
                new_expression = curr + r
                self.delete_insert(new_expression)
                
            else:
                match = re.search(r'[\d.]+$', curr)
                last_num = match.group()
                start_index = match.start()
                result = float(last_num) ** -1

                r = self.clean_result(result)
                new_expression = curr[:start_index] + r
                self.delete_insert(new_expression)
                
        except ZeroDivisionError:
            tkinter.messagebox.showerror("Error", "Cannot divide by zero!")


    def square(self):
        curr = self.entry.get()
        # only number
        if not any(op in curr for op in self.operators):
            result = float(curr) ** 2
            r = self.clean_result(result)
            self.delete_insert(r)

        # expression ends w operator
        elif curr[-1] in self.operators:
            no_b4_op = re.findall(r'[\d.]+', curr)[-1]

            #handle -x-
            if curr[0] == '−':
                no_b4_op = '-'+ no_b4_op

            result = float(no_b4_op) ** 2
            r = self.clean_result(result)
            new_expression = curr + r
            self.delete_insert(new_expression)
        
        # expression contains number after operator
        else:
            match = re.search(r'[\d.]+$', curr)
            last_num = match.group()
            start_index = match.start()
                
            result = float(last_num) ** 2
            r = self.clean_result(result)

            #handle -x
            if curr[0] == '−':
                self.delete_insert(r)
                return
            
            new_expression = curr[:start_index] + r
            self.delete_insert(new_expression)

    def square_root(self):
        curr = self.entry.get()
        try:
            # expression is just one number
            if not any(op in curr for op in self.operators):
                # handle -x
                if float(curr) < 0:
                    tkinter.messagebox.showerror("Error", "Invalid square root!")
                    return
                result = float(curr) ** (1/2)
                r = self.clean_result(result)
                self.delete_insert(r)

            # expression ends with operator
            elif curr[-1] in self.operators:
                no_b4_op = re.findall(r'[\d.]+', curr)[-1]

                # handle -x-
                if curr[0] == '−': #changing. the op after the no doesnt matter
                    tkinter.messagebox.showerror("Error", "Invalid square root!")
                    return
                result = float(no_b4_op) ** (1/2)
                r = self.clean_result(result)
                new_expression = curr + r
                self.delete_insert(new_expression)

            # expression ends with number
            else:
                match = re.search(r'[\d.]+$', curr)
                last_num = match.group()
                start_index = match.start()
                result = float(last_num) ** (1/2)
                r = self.clean_result(result)
                new_expression = curr[:start_index] + r
                self.delete_insert(new_expression)
        except:
            tkinter.messagebox.showerror("Error", "Invalid square root!")

    def percentage(self):
        curr = self.entry.get()

        if not any(op in curr for op in self.operators):
            self.delete_insert('0')

        elif curr[-1] in self.operators:
            no_b4_op = re.findall(r'[\d.]+', curr)[-1]
            result = float(no_b4_op) * float(no_b4_op)/100
            r = self.clean_result(result)
            new_expression = curr + r
            self.delete_insert(new_expression)

        else:
            second_last_num = re.findall(r'[\d.]+', curr)[-2]

            match = re.search(r'[\d.]+$', curr)
            last_num = match.group()
            start_index = match.start()

            result = float(last_num) / 100 * float(second_last_num)
            r = self.clean_result(result)
            new_expression = curr[:start_index] + r
            self.delete_insert(new_expression)

    def keyboard_handler(self, event):
        if event.keysym == 'Return':
            self.equal()
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Delete':
            self.clear_till_last_op()
        elif event.char in '0123456789.':
            self.click(event.char)
        elif event.char in '+-*/':
            char = event.char.replace('*', '×').replace('-', '−')
            self.click(char)

if __name__ == '__main__':
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()