class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    # Función auxiliar para obtener el token actual
    def token_actual(self):
        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]
        return None

    # Función para "consumir" un token si es del tipo esperado
    def emparejar(self, tipo_esperado):
        t = self.token_actual()
        if t and t['token'] == tipo_esperado:
            self.posicion += 1
            return t
        else:
            token_error = t['lexema'] if t else "FIN DE ARCHIVO"
            linea_error = t['linea'] if t else "desconocida"
            raise SyntaxError(f"Error Sintáctico: Se esperaba '{tipo_esperado}' pero se encontró '{token_error}' en la línea {linea_error}")

    # --- REGLAS DE LA GRAMÁTICA ---

    # Punto de entrada: <Programa>
    def parsear(self):
        instrucciones = []
        while self.token_actual() is not None:
            instrucciones.append(self.instruccion())
        return {
            "nodo": "PROGRAMA",
            "hijos": instrucciones
        }

    # <Instruccion>
    def instruccion(self):
        t = self.token_actual()
        if t['token'] == 'TK_CREAR_PAC':
            return self.linea_paciente()
        elif t['token'] == 'TK_REG_CONS':
            return self.linea_consulta()
        elif t['token'] == 'TK_ADD_MED':
            return self.linea_medicamento()
        else:
            raise SyntaxError(f"Error Sintáctico: Instrucción no reconocida '{t['lexema']}' en la línea {t['linea']}.")

    # <LineaPaciente>
    def linea_paciente(self):
        tk_inicio = self.emparejar('TK_CREAR_PAC')
        self.emparejar('TK_ARROW')
        asignaciones = self.lista_asignaciones()
        self.emparejar('TK_SEMICOLON')
        return {
            "nodo": "LINEA_PACIENETE",
            "instruccion": tk_inicio['lexema'],
            "detalles": asignaciones
        }

    # <LineaConsulta>
    def linea_consulta(self):
        tk_inicio = self.emparejar('TK_REG_CONS')
        self.emparejar('TK_ARROW')
        asignaciones = self.lista_asignaciones()
        self.emparejar('TK_SEMICOLON')
        return {
            "nodo": "LINEA_CONSULTA",
            "instruccion": tk_inicio['lexema'],
            "detalles": asignaciones
        }

    # <LineaMedicamento>
    def linea_medicamento(self):
        tk_inicio = self.emparejar('TK_ADD_MED')
        self.emparejar('TK_ARROW')
        asignaciones = self.lista_asignaciones()
        self.emparejar('TK_SEMICOLON')
        return {
            "nodo": "LINEA_MEDICAMENTO",
            "instruccion": tk_inicio['lexema'],
            "detalles": asignaciones
        }

    # <ListaAsignaciones>
    def lista_asignaciones(self):
        asignaciones = {}
        # Procesamos la primera asignación
        attr, valor = self.asignacion()
        asignaciones[attr] = valor
        
        # Mientras haya comas, seguimos acumulando asignaciones en el mismo bloque
        while self.token_actual() and self.token_actual()['token'] == 'TK_COMMA':
            self.emparejar('TK_COMMA')
            attr, valor = self.asignacion()
            asignaciones[attr] = valor
            
        return asignaciones

    # <Asignacion> ::= TK_ATTR TK_EQUALS <Valor>
    def asignacion(self):
        tk_attr = self.emparejar('TK_ATTR')
        self.emparejar('TK_EQUALS')
        
        tk_val = self.token_actual()
        if tk_val and tk_val['token'] in ['TK_NUM', 'TK_TEXT']:
            self.posicion += 1 # Consumimos el valor
            return tk_attr['lexema'], tk_val['lexema']
        else:
            token_error = tk_val['lexema'] if tk_val else "NADA"
            raise SyntaxError(f"Error Sintáctico: Se esperaba un valor numérico o texto, pero se encontró '{token_error}'")

# --- PRUEBA LOCAL ---
if __name__ == '__main__':
    from extractor import html_a_medlang
    from lexer import analizar_lexico
    import json # Usaremos JSON solo para imprimir el árbol bonito en consola
    
    # 1. Obtener tokens
    codigo = html_a_medlang('receta_ejemplo.html')
    tokens = analizar_lexico(codigo)
    
    # 2. Correr el Parser
    parser = AnalizadorSintactico(tokens)
    try:
        arbol_sintactico = parser.parsear()
        print("\n=== ÁRBOL SINTÁCTICO GENERADO EXITOSAMENTE ===")
        print(json.dumps(arbol_sintactico, indent=4, ensure_ascii=False))
    except SyntaxError as e:
        print(e)