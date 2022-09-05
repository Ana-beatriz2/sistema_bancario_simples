from abc import abstractmethod, ABC


class Pessoa:
    def __init__(self, nome, idade):
        self._nome = nome
        self._idade = idade

    @property
    def nome(self):
        return self._nome

    @property
    def idade(self):
        return self._idade


class Cliente(Pessoa):
    def __init__(self, nome, idade):
        super().__init__(nome, idade)
        self.conta = None

    def inserir_conta(self, conta):
        self.conta = conta


class Banco:
    def __init__(self):
        self.agencias = [1111, 2222, 3333]
        self.clientes = []
        self.contas = []

    def inserir_cliente(self, cliente):
        self.clientes.append(cliente)

    def inserir_conta(self, conta):
        self.contas.append(conta)

    def autenticar(self, cliente):
        if cliente not in self.clientes:
            return False

        if cliente.conta not in self.contas:
            return False

        if cliente.conta.agencia not in self.agencias:
            return False

        return True


class Conta(ABC):
    def __init__(self, agencia, conta, saldo):
        self._agencia = agencia
        self._conta = conta
        self._saldo = saldo

    @property
    def agencia(self):
        return self._agencia

    @property
    def conta(self):
        return self._conta

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

    def detalhes(self):
        print(f'\nAgencia: {self.agencia}\nConta: {self.conta}\nSaldo: R$', end='')
        print(f'\033[31m{self.saldo:.2f}\033[m\n' if self.saldo < 0 else f'\033[32m{self.saldo:.2f}\033[m\n')

    def depositar(self, valor):
        self._saldo += valor
        self.detalhes()

    @abstractmethod
    def sacar(self, valor):
        pass


class ContaPoupanca(Conta):
    def sacar(self, valor):
        if not isinstance(valor, (int, float)):
            print('Erro! O valor a ser sacado precisa ser numérico.')
            return

        if self.saldo < valor:
            print('\033[31mSaldo insuficente!\033[m')
            return

        self._saldo -= valor
        self.detalhes()


class ContaCorrente(Conta):
    def __init__(self, agencia, conta, saldo, limite=100):
        Conta.__init__(self, agencia, conta, saldo)
        self._limite = limite

    def sacar(self, valor):

        if not isinstance(valor, (int, float)):
            print('O valor a ser sacado precisa ser numérico.')
            return

        if (self.saldo + self._limite) < valor:
            print('\033[31mSaldo insuficiente!\033[m')
            return

        self._saldo -= valor
        self.detalhes()


if __name__ == '__main__':
    banco = Banco()

    cliente1 = Cliente('Fernanda', 54)
    cliente2 = Cliente('Caio Gael', 23)
    cliente3 = Cliente('Bianca Alves', 38)

    conta1 = ContaPoupanca(1111, 1234, 0)
    conta2 = ContaCorrente(2222, 1233, 0)
    conta3 = ContaCorrente(7777, 1222, 0)

    cliente1.inserir_conta(conta1)
    cliente2.inserir_conta(conta2)
    cliente3.inserir_conta(conta3)

    banco.inserir_cliente(cliente1)
    banco.inserir_cliente(cliente2)
    banco.inserir_cliente(cliente3)

    banco.inserir_conta(conta1)
    banco.inserir_conta(conta2)
    banco.inserir_conta(conta3)

    if banco.autenticar(cliente1):
        cliente1.conta.depositar(100)
    else:
        print('Cliente não autenticado.')

    if banco.autenticar(cliente3):
        cliente3.conta.sacar(300)
    else:
        print('Cliente não autenticado.')
