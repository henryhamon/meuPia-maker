#!/usr/bin/env python3
import sys
import subprocess
import argparse
import time
import serial

def soft_reset(port):
    """Envia comandos Serial para parar o Python e resetar."""
    print(f"Conectando em {port} para Soft Reset...")
    try:
        with serial.Serial(port, 115200, timeout=1) as ser:
            # Envia Ctrl-C duas vezes para interromper qualquer loop
            ser.write(b'\x03')
            time.sleep(0.1)
            ser.write(b'\x03')
            time.sleep(0.1)
            # Envia Ctrl-D para soft reboot
            ser.write(b'\x04')
            time.sleep(1.0) # Espera reiniciar
        print("Soft reset enviado.")
    except Exception as e:
        print(f"Aviso: Erro ao tentar soft reset via serial: {e}")

def run_ampy_command(port, command_args):
    """Executa um comando ampy."""
    cmd = ["ampy", "--port", port] + command_args
    print(f"Executando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro no ampy: {result.stderr}")
        raise RuntimeError("Falha no comando ampy")
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Upload Tool para meuPia-maker")
    parser.add_argument('--port', required=True, help="Porta Serial da placa (ex: /dev/ttyUSB0 ou COM3)")
    parser.add_argument('--main', default="main.py", help="Arquivo main.py gerado para upload")
    parser.add_argument('--runtime', default="maker/plugin_iot.py", help="Caminho do runtime local")
    args = parser.parse_args()

    try:
        # 1. Parar execução atual (Soft Reset)
        soft_reset(args.port)
        
        # Espera um pouco para a placa voltar
        time.sleep(2)

        # 2. Enviar Runtime (plugin_iot.py) para /lib/
        print("Preparando diretório /lib na placa...")
        try:
            run_ampy_command(args.port, ["mkdir", "/lib"])
        except RuntimeError:
            print("Diretório /lib talvez já exista, continuando...")

        print("Enviando plugin_iot.py...")
        run_ampy_command(args.port, ["put", args.runtime, "/lib/plugin_iot.py"])

        # 3. Enviar arquivo compilado (main.py) para raiz
        print(f"Enviando {args.main}...")
        run_ampy_command(args.port, ["put", args.main, "/main.py"])

        # 4. Reiniciar a placa
        print("Reiniciando a placa...")
        run_ampy_command(args.port, ["reset"])
        
        print("\nUpload concluído com sucesso!")
        print("Pressione Reset na placa se o código não iniciar automaticamente.")

    except Exception as e:
        print(f"\nFalha no upload: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
