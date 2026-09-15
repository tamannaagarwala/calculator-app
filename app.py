import ast
import operator
import tkinter as tk


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("360x640")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f172a")

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        main_frame = tk.Frame(root, bg="#0f172a", padx=18, pady=18)
        main_frame.pack(fill="both", expand=True)

        display = tk.Entry(
            main_frame,
            textvariable=self.display_var,
            font=("Arial", 30, "bold"),
            justify="right",
            bd=0,
            bg="#111827",
            fg="#f8fafc",
            relief="flat",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", ipady=18, pady=(0, 18))

        button_specs = [
            ("C", 1, 0, "#1e293b", "#f8fafc"),
            ("⌫", 1, 1, "#1e293b", "#f8fafc"),
            ("%", 1, 2, "#1e293b", "#f8fafc"),
            ("÷", 1, 3, "#f59e0b", "#fff"),
            ("7", 2, 0, "#334155", "#f8fafc"),
            ("8", 2, 1, "#334155", "#f8fafc"),
            ("9", 2, 2, "#334155", "#f8fafc"),
            ("x", 2, 3, "#f59e0b", "#fff"),
            ("4", 3, 0, "#334155", "#f8fafc"),
            ("5", 3, 1, "#334155", "#f8fafc"),
            ("6", 3, 2, "#334155", "#f8fafc"),
            ("-", 3, 3, "#f59e0b", "#fff"),
            ("1", 4, 0, "#334155", "#f8fafc"),
            ("2", 4, 1, "#334155", "#f8fafc"),
            ("3", 4, 2, "#334155", "#f8fafc"),
            ("+", 4, 3, "#f59e0b", "#fff"),
            ("0", 5, 0, "#334155", "#f8fafc"),
            (".", 5, 1, "#334155", "#f8fafc"),
            ("=", 5, 2, "#34d399", "#052e16"),
            ("/", 5, 3, "#f59e0b", "#fff"),
        ]

        for label, row, col, bg, fg in button_specs:
            btn = tk.Button(
                main_frame,
                text=label,
                width=5,
                height=2,
                font=("Arial", 22, "bold"),
                bg=bg,
                fg=fg,
                highlightthickness=0,
                bd=0,
                activebackground="#475569",
                activeforeground=fg,
                command=lambda value=label: self.handle_button(value),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)

        for i in range(6):
            main_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            main_frame.grid_columnconfigure(j, weight=1)

    def handle_button(self, value):
        if value == "C":
            self.clear()
            return

        if value == "⌫":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
            return

        if value == "=":
            self.calculate()
            return

        if value in {"÷", "x"}:
            value = "/" if value == "÷" else "*"

        if value == "%":
            if not self.expression:
                return
            try:
                self.expression = str(float(self.safe_eval(self.expression)) / 100)
                self.display_var.set(self.expression)
            except Exception:
                self.display_var.set("Error")
                self.expression = ""
            return

        if value in {"+", "-", "*", "/", "."}:
            if value == "." and "." in self.expression.split("/")[-1].split("*")[-1].split("+")[-1].split("-")[-1]:
                return
            self.expression += value
            self.display_var.set(self.expression)
            return

        self.expression += str(value)
        self.display_var.set(self.expression)

    def clear(self):
        self.expression = ""
        self.display_var.set("0")

    def calculate(self):
        if not self.expression:
            return

        try:
            result = self.safe_eval(self.expression)
            self.display_var.set(str(result))
            self.expression = str(result)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def safe_eval(self, expression):
        expression = expression.replace("÷", "/").replace("x", "*")
        tree = ast.parse(expression, mode="eval")

        def eval_node(node):
            if isinstance(node, ast.Expression):
                return eval_node(node.body)
            if isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                ops = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                }
                if type(node.op) not in ops:
                    raise ValueError("Unsupported operator")
                return ops[type(node.op)](left, right)
            if isinstance(node, ast.UnaryOp):
                operand = eval_node(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return +operand
                if isinstance(node.op, ast.USub):
                    return -operand
                raise ValueError("Unsupported unary operator")
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid input")

        return eval_node(tree)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()