from tkinter import *
from functions.calculator_functions import CalculatorFunctions

class Calculator:
    def __init__(self):
        self._root = self._make_root()
        self._display = self._make_display(self._root)
        self._button = self._make_button(self._root)
        self.calc_func = CalculatorFunctions()

    # Cria e configura a janela da calculadora
    def _make_root(self):
        root = Tk()
        root.title('Calculator')
        root.resizable(False, False)
        root.config(padx=10, pady=10, background='#1C1C1C')
        return root
    
    # Cria e configura o display da calculadora, onde aparecerá os números
    def _make_display(self, root):
        display = Entry(root)
        display.grid(row=0, column=0, columnspan=4, sticky='news', pady=(20,  40))
        display.config(
            font=('Arial', 20), fg='#FFFAFA', justify='right', background='#363636',
            highlightthickness=2, highlightbackground='#363636', highlightcolor='#4F4F4F',
            relief='flat'
        )
        return display
    
    # Cria os botões da calculadora
    def _make_button(self, root):
        # Lista de tuplas com os botões da calculadora
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
                btn = Button(root, text=button_value, command=lambda x=button_value: self._button_click(x))
                btn.grid(row=row_index, column=button_index, sticky='news', padx=5, pady=5)
                btn.config(
                    font=('Arial', 20), fg='#FFFAFA', background='#363636', bd=0,
                    cursor='hand2', highlightthickness=0, highlightcolor='#4F4F4F',
                    highlightbackground='#363636', activebackground='#4F4F4F', activeforeground='#FFFAFA', width=1
                )

                button_row.append(btn)
        return button_row
    
    # Designa as funções ao clicar em um botão específico
    def _button_click(self, value):
        # Quando clicado em "C" limpa o display totalmente
        if value == 'C':
            self.calc_func.delete_all()
        
        # Deleta um valor por vez
        elif value == '⌫':
            self.calc_func.delete_one()

        # Quando clicado em "=" faz o replace do operador se necessário
        elif value in '=':
            self.calc_func.replace_operator()

            try:
                calculation = self.calc_func.current_value()
                result = str(eval(calculation))
                self.calc_func.delete_all()
                self.calc_func.add_value(result)
            # Caso o método eval() não consiga executar uma conta, retorna "Error" no display
            except:
                    self.calc_func.delete_all()
                    self.calc_func.add_value('Error')

        # Adiciona os números, operadores, parênteses, ponto e vírgula no display
        else:
            self.calc_func.add_value(value)
        self._update_display()

    # Toda vez que é chamada limpa o display e insere nele novamente com as atualizações
    def _update_display(self):
        self._display.delete(0, END)
        self._display.insert(END, self.calc_func.current_value())

    def run(self):
        return self._root.mainloop()
