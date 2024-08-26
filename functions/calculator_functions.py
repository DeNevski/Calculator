# Permite "encapsular" cada valor em um nó
class Node:
    def __init__(self, data):
        self.data = data
        self.previous = None

class CalculatorFunctions:
    def __init__(self):
        self._top = None
        self._size = 0

    '''Envolve o valor em um nó, liga esse nó que acabou de chegar ao restante dos valores
      atráves de "node.previous = self._top,"e depois atribui o nó que acabou de chegar como o último valor que foi digitado.'''
    def add_value(self, value):
        node = Node(value)
        node.previous = self._top
        self._top = node
        self._size += 1

    '''Define que o último valor digitado pelo usúario seja o antecessor do atual último, sendo assim, excluindo-o.'''
    def delete_one(self):
        if self._size > 0:
            self._top = self._top.previous
            self._size -= 1

    '''A mesma lógica de "delete_one", porém agora em um while para limpar não apenas um, mas todos valores.'''
    def delete_all(self):
        while self._size > 0:
            self._top = self._top.previous
            self._size -= 1
        return ''

    # Substitui os operadores "x" e "÷" para "*" e "/" respectivamente
    def replace_operator(self):
        pointer = self._top
        while pointer:
            if pointer.data == 'x':
                pointer.data = '*'

            if pointer.data == '÷':
                pointer.data = '/'

            pointer = pointer.previous
    
    # Retorna todos os valores
    def current_value(self):
        values = []
        pointer = self._top
        while pointer:
            values.append(str(pointer.data))
            pointer = pointer.previous
        return ''.join(reversed(values))
