import inspect
import traceback
from PySide6.QtCore import QThread, Signal

class TarefaSegundoPlano(QThread):
    """
    Thread de execução em segundo plano para operações intensivas de I/O e processamento.
    Mantém a interface PySide6 responsiva emitindo sinais de progresso, conclusão e erro.
    """
    progresso = Signal(int, str)
    sucesso = Signal(object)
    erro = Signal(str)

    def __init__(self, funcao, *args, **kwargs):
        super().__init__()
        self.funcao = funcao
        self.argumentos = list(args)
        self.argumentos_nomeados = dict(kwargs)

    def run(self):
        try:
            try:
                parametros = inspect.signature(self.funcao).parameters
                if "callback_progresso" in parametros and "callback_progresso" not in self.argumentos_nomeados:
                    self.argumentos_nomeados["callback_progresso"] = self.progresso.emit
            except (ValueError, TypeError):
                pass

            resultado = self.funcao(*self.argumentos, **self.argumentos_nomeados)
            self.sucesso.emit(resultado)
        except Exception as excecao:
            detalhes = traceback.format_exc()
            self.erro.emit(f"{str(excecao)}\n\nDetalhes:\n{detalhes}")
