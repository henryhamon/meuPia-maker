try:
    import machine
    import time
    IS_PC = False
except ImportError:
    IS_PC = True
    import time

def iot_configurar_pino(pino, modo):
    """
    Configura um pino em modo de entrada ou saída.
    pino: int (número do GPIO)
    modo: str ('ENTRADA' ou 'SAIDA')
    """
    if IS_PC:
        print(f"[SIMULADOR] iot_configurar_pino({pino}, {modo})")
        return

    # Mapeamento simples de strings para constantes do MicroPython
    # Assumindo que o compilador envia strings ou constantes numéricas
    dir_map = {
        'ENTRADA': machine.Pin.IN,
        'SAIDA': machine.Pin.OUT
    }
    
    # Se o modo for passado como string pelo compilador
    mode_val = dir_map.get(str(modo).upper(), machine.Pin.OUT)
    
    # Inicializa o pino e guarda referência se necessário, 
    # mas o MicroPython permite instanciar on-the-fly sem problemas de memória graves para casos simples.
    # Para performance, idealmente guardaríamos em um dict global, mas vamos manter simples.
    machine.Pin(pino, mode_val)

def iot_ligar(pino):
    """Define o pino como nível alto (3.3V)."""
    if IS_PC:
        print(f"[SIMULADOR] iot_ligar({pino})")
        return
    machine.Pin(pino).value(1)

def iot_desligar(pino):
    """Define o pino como nível baixo (0V)."""
    if IS_PC:
        print(f"[SIMULADOR] iot_desligar({pino})")
        return
    machine.Pin(pino).value(0)

def iot_esperar(ms):
    """Pausa a execução por ms milissegundos."""
    if IS_PC:
        print(f"[SIMULADOR] iot_esperar({ms})")
        time.sleep(ms / 1000.0)
        return
    time.sleep_ms(ms)
