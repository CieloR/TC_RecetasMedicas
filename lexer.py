import re

# 1. Definición de Expresiones Regulares para cada Token
TOKEN_REGEX = [
    ('TK_CREAR_PAC',     r'CREAR_PACIENTE'),
    ('TK_REG_CONS',      r'REGISTRAR_CONSULTA'),
    ('TK_ADD_MED',       r'AGREGAR_MEDICAMENTO'),
    ('TK_ARROW',         r'->'),
    ('TK_EQUALS',        r'='),
    ('TK_COMMA',         r','),
    ('TK_SEMICOLON',     r';'),
    ('TK_NUM',           r'\d+'),                                # Números (DNI, Edad)
    ('TK_TEXT',          r'"[^"\\]*(?:\\.[^"\\]*)*"'),           # Textos entre comillas
    ('TK_ATTR',          r'[A-Z_]+'),                            # Atributos (DNI, NOMBRE, etc.)
    ('SKIP',             r'[ \t\n\r]+'),                         # Espacios y saltos de línea (ignorar)
    ('MISMATCH',         r'.'),                                  # Cualquier otro caracter (Error Léxico)
]

def analizar_lexico(codigo_fuente):
    # Combinamos todas las expresiones regulares en una sola master-regex
    regex_combinada = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_REGEX)
    
    lista_tokens = []
    linea_actual = 1
    
    # Buscamos coincidencias en el texto
    for match in re.finditer(regex_combinada, codigo_fuente):
        tipo_token = match.lastgroup
        lexema = match.group(tipo_token)
        
        if tipo_token == 'SKIP':
            continue
        elif tipo_token == 'MISMATCH':
            raise SyntaxError(r"Error Léxico: Caracter ilegal '{lexema}' en la línea {linea_actual}")
        else:
            # Si el token es un texto entre comillas, le quitamos las comillas para el lexema limpio
            if tipo_token == 'TK_TEXT':
                lexema = lexema[1:-1]
                
            lista_tokens.append({
                'token': tipo_token,
                'lexema': lexema,
                'linea': linea_actual
            })
            
        # Si hay un salto de línea en el código fuente, aumentamos el contador (para el control de errores)
        if '\n' in match.group():
            linea_actual += 1
            
    return lista_tokens

# --- PRUEBA LOCAL ---
if __name__ == '__main__':
    from extractor import html_a_medlang
    
    # 1. Extraemos el código intermedio
    codigo = html_a_medlang('receta_ejemplo.html')
    
    # 2. Lo pasamos por el Analizador Léxico
    tokens_encontrados = analizar_lexico(codigo)
    
    print("\n=== TABLA DE TOKENS GENERADA ===")
    print(f"{'TOKEN':<20} | {'LEXEMA'}")
    print("-" * 45)
    for t in tokens_encontrados:
        print(f"{t['token']:<20} | {t['lexema']}")