try:
    from meupia.analyzers.code_generator import CodeGenerator
except ImportError:
    # Fallback para desenvolvimento sem o pacote instalado
    class CodeGenerator:
        def __init__(self):
            self.code = []
        def generate(self, ast):
            pass
        def _add_line(self, line):
            self.code.append(line)

class MakerCodeGenerator(CodeGenerator):
    """
    Extensão do CodeGenerator para gerar código otimizado para MicroPython.
    Remove bibliotecas pesadas e injeta dependências de IoT.
    """
    
    def generate(self, ast):
        """
        Sobrescreve o método principal de geração para controlar o cabeçalho.
        Assume que a classe base possui um fluxo que podemos interceptar ou recriar.
        Como não temos o código fonte base, vamos recriar o cabeçalho e chagar a geração do corpo.
        """
        self.code = []
        self._generate_header()
        
        # Aqui, idealmente chamaríamos o restante da geração da superclasse.
        # Se a superclasse tiver um método `_generate_body(ast)` ou similar, seria ideal.
        # Caso contrário, e `super().generate(ast)` gere tudo (incluindo header indesejado),
        # precisaríamos de uma estratégia diferente (ex: gerar tudo e substituir strings).
        # 
        # Assumiremos aqui que podemos chamar super().generate(ast) e depois limpar o header,
        # OU que estamos reimplementando a 'receita' de bolo.
        #
        # Vamos tentar uma abordagem híbrida segura: 
        # Chamar super().generate(ast) para popular self.code, e depois substituir as primeiras linhas.
        
        super().generate(ast)
        
        # Pós-processamento para substituir o cabeçalho padrão
        self._replace_header()
        
        return "\n".join(self.code)

    def _generate_header(self):
        # Este método existe para ser chamado explicitamente se controlarmos o fluxo total,
        # mas na estratégia de pós-processamento, usaremos _replace_header.
        pass

    def _replace_header(self):
        """
        Remove imports padrão do meupia-core e insere os do MicroPython.
        """
        new_header = [
            "# Código gerado por meuPia-maker para MicroPython (ESP32/Pico)",
            "import time",
            "import machine",
            "from lib.plugin_iot import *",
            "",
            "# Início do código do usuário"
        ]
        
        # Identifica onde começam os imports padrão para removê-los.
        # O Core gera algo como:
        # import sys
        # import os
        # from meupia_libs import ...
        
        # Vamos filtrar linhas que contêm imports proibidos
        forbidden = ["import sys", "import os", "from meupia_libs", "import meupia_libs"]
        
        cleaned_code = []
        header_injected = False
        
        for line in self.code:
            is_forbidden = any(bad in line for bad in forbidden)
            if not is_forbidden:
                cleaned_code.append(line)
            
            # Injeta nosso header logo no início se ainda não foi
            if not header_injected and not line.startswith("#"): 
                # Assumindo que comentários iniciais são preservados ou ignorados
                # Vamos apenas prependar nosso header na lista final
                pass

        # Reconstrói a lista, colocando nosso header no topo
        self.code = new_header + cleaned_code
