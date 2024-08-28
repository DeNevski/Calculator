from tkinter import *
from functions.calculator_functions import CalculatorFunctions

class Calculator:
    def __init__(self):
        self._root = self.make_root()
        self._display = self.make_display(self._root)
        self._button = self.make_button(self._root)
        self.calc_func = CalculatorFunctions()
        self._history_text = None
        self._save_values = []

    # Cria e configura a janela da calculadora
    def make_root(self):
        root = Tk()
        root.title('Calculator')
        root.resizable(False, False)
        root.config(padx=10, pady=10, background='#1C1C1C')
        return root
    
    # Cria e configura o display da calculadora, onde aparecerá os números
    def make_display(self, root):
        display = Entry(root)
        display.grid(row=0, column=0, columnspan=4, sticky='news', pady=(20,  20))
        display.config(
            font=('Arial', 20), fg='#DCDCDC', justify='right', background='#363636',
            highlightthickness=2, highlightbackground='#363636', highlightcolor='#4F4F4F',
            relief='flat'
        )
        return display
    
    '''Verifica toda vez que o botão é pressionado se a "tela" do histórico existe e está ativa.
        Caso esteja, a "tela" é destruida. E se não estiver, cria uma.'''
    def make_history_display(self):
        if self._history_text and self._history_text.winfo_exists():
            self._history_text.destroy()
        else:
            self._history_text = Text(self._root, state='disabled')
            self._history_text.grid(row=7, column=0, columnspan=4, sticky='news', padx=5, pady=5)
            self._history_text.config(
                font=('Arial', 15), fg='#DCDCDC', background='#363636', bd=0,
                cursor='arrow', width=10, height=10
            )
            '''Percorre a lista de tuplas com as contas e resultados e passa para "self._add_history_value(),
               Onde será formatado e adicionado ao histórico.'''
            for value in self._save_values:
                self._add_history_value(value[0], value[1])

    # Cria os botões da calculadora
    def make_button(self, root):
        # Lista de tuplas com os botões da calculadora
        button_texts = [
            ('⟲'),
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
                    font=('Arial', 20), fg='#DCDCDC', background='#363636', bd=0,
                    cursor='hand2', highlightthickness=0, highlightcolor='#4F4F4F',
                    highlightbackground='#363636', activebackground='#4F4F4F', activeforeground='#DCDCDC', width=1
                )

                button_row.append(btn)
        return button_row
    
    # Formata e adiciona as contas ao histórico
    def _add_history_value(self, calc, result):
        if '*' in calc:
            calc = calc.replace('*', 'x')
        if '/' in calc:
            calc = calc.replace('/', '÷')

        h = f'{calc} = {result}\n'

        self._history_text['state'] = 'normal'
        self._history_text.insert(END, h)
        self._history_text['state'] = 'disabled'
    
    # Designa as funções ao clicar em um botão específico
    def _button_click(self, value):
        # Quando clicado em "C" limpa o display totalmente
        if value == 'C':
            self.calc_func.delete_all()
        
        # Deleta um valor por vez
        elif value == '⌫':
            self.calc_func.delete_one()

        # Abre e fecha o histórico de contas
        elif value == '⟲':
            self.make_history_display()

        # Faz as contas
        elif value in '=':
            # Altera o operador caso necessário
            self.calc_func.replace_operator()
            # Fecha o histórico caso aberto, para que esteja sempre atualizado
            if self._history_text and self._history_text.winfo_exists():
                self._history_text.destroy()

            try:
                calculation = self.calc_func.current_value()
                result = str(eval(calculation))
                # Salva os valores da conta e do resultado
                self._save_values.append((calculation, result))  

                self.calc_func.delete_all()
                self.calc_func.add_value(result)
            # Caso o método eval() não consiga executar uma conta, retorna "Error" no display
            except:
                    self.calc_func.delete_all()
                    self.calc_func.add_value('Error')
            
        else:
            # Fecha o histórico caso aberto, para que esteja sempre atualizado
            if self._history_text and self._history_text.winfo_exists():
                self._history_text.destroy()

            # Adiciona os números, operadores, parênteses, ponto e vírgula no display
            self.calc_func.add_value(value)
        self._update_display()

    # Toda vez que é chamada limpa o display e insere nele novamente com as atualizações
    def _update_display(self):
        self._display.delete(0, END)
        self._display.insert(END, self.calc_func.current_value())

    def run(self):
        return self._root.mainloop()
