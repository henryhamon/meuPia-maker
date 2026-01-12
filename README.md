# meuPiá Maker – IoT & Robotics Plugin

![meuPia](assets/meuPia-maker.png)

## 📖 Overview

> **Nota:** Este é um **plugin oficial** para o compilador [meuPiá](https://www.google.com/search?q=https://github.com/SEU_USUARIO/meuPia-core).

**meuPiá Maker** é a extensão de **Internet das Coisas (IoT)** do ecossistema meuPiá.

Ele permite que estudantes programem microcontroladores reais (como **ESP32**, **ESP8266** e **Raspberry Pi Pico**) utilizando Portugol. O plugin substitui o motor de geração de código padrão para produzir scripts **MicroPython** altamente otimizados, gerenciando automaticamente a comunicação com o hardware.

**meuPiá Maker** fornece:

* **A Runtime IoT:** Wrappers simples (`iot_ligar`, `iot_ler`) que abstraem a complexidade da biblioteca `machine`.
* **O Gerador Otimizado:** Um *Code Generator* especializado que remove dependências pesadas de PC (como `sys`, `numpy`) para economizar memória RAM na placa.
* **Deploy Tool:** Ferramentas integradas para enviar o código compilado via USB diretamente para o microcontrolador.

## 🎯 Motivation

A barreira de entrada para Robótica e IoT geralmente é a linguagem C++ (Arduino) ou a complexidade de configurar ambientes de desenvolvimento.

**meuPiá Maker** resolve isso trazendo a lógica do Portugol para o mundo físico:

* **Abstração de Hardware:** O aluno escreve `iot_ligar(2)` em vez de configurar registradores ou instanciar objetos complexos.
* **Fluxo Contínuo:** O aluno aprende lógica no PC com o *meuPiá Core* e, quando quer piscar um LED, apenas adiciona `usar "maker"` ao código.
* **Poder do MicroPython:** Por baixo dos panos, utilizamos todo o poder e estabilidade do MicroPython, permitindo interatividade e debug em tempo real.

## ⚙️ How It Works

Este projeto funciona como uma extensão instalável sobre o Core:

### 1. The Plugin Injection

Ao instalar este pacote, o comando `usar "maker"` torna-se disponível no compilador. Isso instrui o **meuPiá** a carregar o `MakerCodeGenerator`, que altera a estratégia de transpilação.

### 2. Hardware Aware Generation

Diferente da versão Desktop, o código gerado aqui é "limpo". Imports desnecessários são removidos e substituídos por chamadas à API `machine` e `time` do microcontrolador.

### 3. The Deploy Pipeline

Incluímos um utilitário baseado no `ampy` (Adafruit MicroPython Tool). Após a compilação, o sistema automatiza o *soft-reset* da placa, o upload das bibliotecas e a execução do `main.py`.

---

## 🚀 Installation

Você pode instalar o Maker através do gerenciador de pacotes do meuPiá (`mpm`) ou via pip.

### Via MPM (Recomendado)

```bash
# Se você já tem o meuPiá Core instalado:
mpm install maker

```

### Via Git (Desenvolvimento)

```bash
pip install git+https://github.com/SEU_USUARIO/meuPia-maker.git

```

*(Nota: Requer Python 3.8+ e o pacote `meupia-core` pré-instalado).*

---

## 🛠️ Usage Examples

### 1. Pisca LED (Hello World)

O clássico da eletrônica. Configura o pino 2 (geralmente o LED onboard do ESP32) e o faz piscar.

```portugol
algoritmo "PiscaLed"
usar "maker"  // Carrega as funções IoT

var led: inteiro
inicio
    led <- 2
    iot_configurar_pino(led, "saida")
    
    enquanto verdadeiro faca
        iot_ligar(led)
        iot_esperar(500) // Espera 500ms
        
        iot_desligar(led)
        iot_esperar(500)
    fimenquanto
fimalgoritmo

```

### 2. Leitura de Botão e Controle

Lê um botão no pino 4 e acende o LED se pressionado.

```portugol
algoritmo "ControleBotao"
usar "maker"

var 
    btn, led: inteiro
    estado: inteiro
inicio
    btn <- 4
    led <- 2
    
    iot_configurar_pino(btn, "entrada")
    iot_configurar_pino(led, "saida")
    
    enquanto verdadeiro faca
        estado <- iot_ler(btn)
        
        se estado = 1 entao
            iot_ligar(led)
        senao
            iot_desligar(led)
        fim_se
        
        iot_esperar(50) // Debounce simples
    fimenquanto
fimalgoritmo

```

### 3. Realizando o Upload

Para compilar e enviar para a placa conectada na porta `COM3` (Windows) ou `/dev/ttyUSB0` (Linux/Mac):

```bash
# Compila e faz o deploy automático
meupia pisca_led.por --target esp32 --port COM3

```

---

## 🔍 Supported Hardware

O **meuPiá Maker** é compatível com qualquer placa que rode **MicroPython** ou **CircuitPython**.

| Placa | Status | Observação |
| --- | --- | --- |
| **ESP32** (DevKit V1) | ✅ Estável | Hardware de referência. |
| **Raspberry Pi Pico** | ✅ Estável | Testado com firmware oficial. |
| **ESP8266** (NodeMCU) | ⚠️ Beta | Funciona, mas tem menos memória. |

---

## 🙌 Credits

Desenvolvido como parte do ecossistema educacional **meuPiá** que é desenvolvido com ❤️ por **[@henryhamon](https://github.com/henryhamon)**.

* Core Compiler: [meuPia-core](https://github.com/henryhamon/meuPia-core.git)
* Deploy Tooling: Baseado no [adafruit-ampy](https://github.com/adafruit/ampy)