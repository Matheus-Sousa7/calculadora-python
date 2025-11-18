import tkinter as tk
from tkinter import messagebox
from database import Database

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("340x460")
        self.root.configure(bg="#202020")

        self.db = Database("history.json")  # Banco de dados JSON

        self.expression = ""

        # Display
        self.display = tk.Entry(
            root,
            font=("Arial", 22),
            bd=4,
            relief=tk.RIDGE,
            justify="right",
            bg="#ffffff"
        )
        self.display.pack(fill="both", padx=10, pady=12, ipady=8)

        # Frame dos botões
        frame = tk.Frame(root, bg="#202020")
        frame.pack(fill="both", padx=8, pady=6)

        # Criação dos botões (posições fixas para evitar bugs)
        self.create_buttons(frame)

        # Botão de histórico
        tk.Button(
            root,
            text="Ver Histórico",
            command=self.show_history,
            bg="#4cc2ff",
            fg="black",
            font=("Arial", 12, "bold"),
            height=2
        ).pack(fill="both", padx=10, pady=(6,12))

    def create_buttons(self, frame):
        # layout: (texto, comando, row, col, rowspan, colspan)
        layout = [
            ("C", self.clear, 0, 0, 1, 1),
            ("%", lambda: self.add("%"), 0, 1, 1, 1),
            ("/", lambda: self.add("/"), 0, 2, 1, 1),
            ("*", lambda: self.add("*"), 0, 3, 1, 1),

            ("7", lambda: self.add("7"), 1, 0, 1, 1),
            ("8", lambda: self.add("8"), 1, 1, 1, 1),
            ("9", lambda: self.add("9"), 1, 2, 1, 1),
            ("-", lambda: self.add("-"), 1, 3, 1, 1),

            ("4", lambda: self.add("4"), 2, 0, 1, 1),
            ("5", lambda: self.add("5"), 2, 1, 1, 1),
            ("6", lambda: self.add("6"), 2, 2, 1, 1),
            ("+", lambda: self.add("+"), 2, 3, 1, 1),

            ("1", lambda: self.add("1"), 3, 0, 1, 1),
            ("2", lambda: self.add("2"), 3, 1, 1, 1),
            ("3", lambda: self.add("3"), 3, 2, 1, 1),
            ("=", self.calculate, 3, 3, 2, 1),   # "=" ocupa 2 linhas (rows 3 e 4)

            ("0", lambda: self.add("0"), 4, 0, 1, 2),  # "0" ocupa 2 colunas
            (".", lambda: self.add("."), 4, 2, 1, 1),
        ]

        for text, cmd, r, c, rs, cs in layout:
            btn = tk.Button(
                frame,
                text=text,
                command=cmd,
                bg="#3a3a3a" if text not in ("=", "C", "%") else "#4cc2ff",
                fg="white" if text not in ("=", "C", "%") else "#000000",
                font=("Arial", 14, "bold"),
                bd=0,
                relief="raised",
            )

            btn.grid(row=r, column=c, rowspan=rs, columnspan=cs, sticky="nsew", padx=6, pady=6)

        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)
        for j in range(5):
            frame.grid_rowconfigure(j, weight=1)

    def add(self, char):
        if self.expression and char in "+-*/%" and self.expression[-1] in "+-*/%":
            self.expression = self.expression[:-1] + char
        else:
            self.expression += str(char)
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def clear(self):
        self.expression = ""
        self.display.delete(0, tk.END)

    def calculate(self, _=None):
        expr = self.expression.strip()
        if not expr:
            return
        try:
            safe_expr = expr.replace('%', '/100')
            result = eval(safe_expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.db.save({"expressao": expr, "resultado": str(result)})
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.expression = str(result)
        except ZeroDivisionError:
            messagebox.showerror("Erro", "Divisão por zero")
            self.display.delete(0, tk.END)
            self.expression = ""
        except Exception:
            messagebox.showerror("Erro", "Expressão inválida")
            self.display.delete(0, tk.END)
            self.expression = ""

    def show_history(self):
        history = self.db.load()
        if not history:
            messagebox.showinfo("Histórico", "Nenhum cálculo salvo.")
            return
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Histórico")
        hist_window.geometry("360x420")
        hist_window.configure(bg="#202020")
        text_area = tk.Text(hist_window, font=("Arial", 12), bg="#0f0f0f", fg="white")
        text_area.pack(fill="both", expand=True, padx=8, pady=8)
        for item in history:
            expr = item.get("expressao", "")
            res = item.get("resultado", "")
            text_area.insert(tk.END, f"{expr}  =  {res}\n")
        text_area.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
