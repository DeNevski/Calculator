from tkinter import *
from functions.calculator_functions import CalculatorFunctions

class Calculator:
    def __init__(self):
        self.root = self._make_root()
        self.display = self.make_display(self.root)
        self.button = self.make_button(self.root)
        self.calc_func = CalculatorFunctions()
        self._current_value = ''

    # Cria e configura a janela da calculadora
    def _make_root(self):
        root = Tk()
        root.title('Calculator')
        root.resizable(False, False)
        root.config(padx=10, pady=10, background='#1C1C1C')
        return root
    
    # Cria e configura o display da calculadora, onde aparecerá os números
    def make_display(self, root):
        display = Entry(root)
        display.grid(row=0, column=0, columnspan=4, sticky='news', pady=(20,  40))
        display.config(
            font=('Arial', 20), fg='#FFFAFA', justify='right', background='#363636',
            highlightthickness=2, highlightbackground='#363636', highlightcolor='#4F4F4F',
            relief='flat'
        )
        return display
    
    # Cria os botões da calculadora
    def make_button(self, root):
        # Cria uma lista de tuplas com os botões da calculadora
        button_texts = [
            ('(', ')', 'C', '⌫'),  
            ('7', '8', '9', '÷'),
            ('4', '5', '6', 'x'),
            ('1', '2', '3', '-'),
            ('0', '.', '=', '+')
        ]

        # Percorre a lista com um for e as tuplas com outro for, criando cada botão e configurando
        for row_index, row_value in enumerate(button_texts, start=1):
            button_row = []
            for button_index, button_value in enumerate(row_value):
                btn = Button(root, text=button_value, command=lambda x=button_value: self.button_click(x))
                btn.grid(row=row_index, column=button_index, sticky='news', padx=5, pady=5)
                btn.config(
                    font=('Arial', 20), fg='#FFFAFA', background='#363636', bd=0,
                    cursor='hand2', highlightthickness=0, highlightcolor='#4F4F4F',
                    highlightbackground='#363636', activebackground='#4F4F4F', activeforeground='#FFFAFA', width=1
                )

                button_row.append(btn)
        return button_row
    
    # Configurações das ações ao clicar em um botão
    def button_click(self, value):
        # Quando clicado em "C" limpa o display
        if value == 'C':
            self.calc_func._delete_all()

        elif value == '⌫':
            self.calc_func._delete_one()

        # Quando clicado em "=" faz o replace do operador se necessário
        elif value in '=':
            self.calc_func._replace_operator()

            # Caso a função eval() não consiga executar uma conta, retorna "Error" no display
            try:
                calculation = self.calc_func.current_value()
                result = str(eval(calculation))
                self.calc_func._delete_all()
                self.calc_func._add_value(result)
            except:
                    self.calc_func._delete_all()
                    self.calc_func._add_value('Error')

        # Adiciona os números, operadores, parênteses, ponto e vírgula no display
        else:
            self.calc_func._add_value(value)
        self._update_display()

    # Toda vez que é chamada limpa o display e insere nele novamente com as atualizações
    def _update_display(self):
        self.display.delete(0, END)
        self.display.insert(END, self.calc_func.current_value())
