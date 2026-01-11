#!/usr/bin/env python3
import sys
import argparse
import os

# Adiciona o diretório atual ao path para garantir que imports locais funcionem
sys.path.append(os.getcwd())

try:
    from meupia.lexical_analyzer import LexicalAnalyzer
    from meupia.syntax_analyzer import Parser
    from meupia.semantic_analyzer import SemanticAnalyzer
except ImportError:
    print("Erro: O pacote 'meupia-core' não foi encontrado.")
    print("Certifique-se de instalá-lo conforme o requirements.txt")
    # Para fins de bootstrap, não vou fechar se for apenas geração de arquivo pelo agente,
    # mas em produção deve falhar.
    # sys.exit(1)
    pass

from maker.compiler_extension import MakerCodeGenerator

def main():
    parser = argparse.ArgumentParser(description="meuPia-maker: Compilador para ESP32/Pico (IoT)")
    parser.add_argument('arquivo', help="Arquivo fonte .por")
    parser.add_argument('-o', '--output', help="Nome do arquivo de saída", default="main.py")
    args = parser.parse_args()

    if not os.path.exists(args.arquivo):
        print(f"Erro: Arquivo '{args.arquivo}' não encontrado.")
        sys.exit(1)

    try:
        print(f"Compilando {args.arquivo}...")
        
        with open(args.arquivo, 'r', encoding='utf-8') as f:
            source_code = f.read()

        # 1. Análise Léxica
        lexer = LexicalAnalyzer(source_code)
        tokens = lexer.tokenize()

        # 2. Análise Sintática
        parser = Parser(tokens)
        ast = parser.parse()

        # 3. Análise Semântica
        semantic = SemanticAnalyzer(ast)
        semantic.analyze()

        # 4. Geração de Código MicroPython (Maker)
        generator = MakerCodeGenerator()
        code = generator.generate(ast)

        # Salva o resultado
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(code)

        print(f"Sucesso! Código gerado em '{args.output}'.")
        print("Use 'python3 tools/upload.py --port <PORTA>' para enviar para a placa.")

    except Exception as e:
        print(f"Erro durante a compilação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
