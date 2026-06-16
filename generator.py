def generar_sql(arbol_sintactico):
    if not arbol_sintactico or arbol_sintactico.get("nodo") != "PROGRAMA":
        return "-- Error: Árbol sintáctico inválido"

    sentencias_sql = []
    sentencias_sql.append("-- ===============================================")
    sentencias_sql.append("-- SCRIPT SQL GENERADO POR COMPILADOR MEDLANG")
    sentencias_sql.append("-- ===============================================\n")

    # Variables temporales para guardar el DNI y asegurar la relación
    dni_paciente = None
    id_receta_ficticio = "LAST_INSERT_ID()" # O un ID correlativo si prefieres

    for hijo in arbol_sintactico["hijos"]:
        tipo_nodo = hijo["nodo"]
        detalles = hijo["detalles"]

        if tipo_nodo == "LINEA_PACIENETE":
            dni_paciente = detalles.get("DNI")
            # Usamos INSERT IGNORE para que si el DNI ya existe, no falle ni duplique
            sql = (
                f"INSERT IGNORE INTO Pacientes (DNI, Nombre, Edad, Sexo) "
                f"VALUES ({detalles.get('DNI')}, '{detalles.get('NOMBRE')}', {detalles.get('EDAD')}, '{detalles.get('SEXO')}');"
            )
            sentencias_sql.append(sql)

        elif tipo_nodo == "LINEA_CONSULTA":
            # Insertamos la consulta/receta enlazada al DNI del paciente
            sql = (
                f"INSERT INTO Recetas (DNI_Paciente, Fecha, Diagnostico, Alergias) "
                f"VALUES ({detalles.get('DNI')}, '{detalles.get('FECHA')}', '{detalles.get('DIAGNOSTICO')}', '{detalles.get('ALERGIAS')}');"
            )
            sentencias_sql.append(sql)

        elif tipo_nodo == "LINEA_MEDICAMENTO":
            # Insertamos los medicamentos de la receta. 
            # En un entorno real usaríamos el ID de la receta insertada arriba
            sql = (
                f"INSERT INTO Medicamentos_Receta (DNI_Paciente, Generico, Presentacion, Dosis, Frecuencia, Via, Duracion) "
                f"VALUES ({detalles.get('DNI')}, '{detalles.get('GENERICO')}', '{detalles.get('PRES')}', "
                f"'{detalles.get('DOSIS')}', '{detalles.get('FREC')}', '{detalles.get('VIA')}', '{detalles.get('TIEMPO')}');"
            )
            sentencias_sql.append(sql)

    return "\n".join(sentencias_sql)

# --- PRUEBA LOCAL DE TODO EL COMPILADOR ---
if __name__ == '__main__':
    from extractor import html_a_medlang
    from lexer import analizar_lexico
    from parser import AnalizadorSintactico

    # 1. Extractor: HTML -> MedLang
    codigo_medlang = html_a_medlang('receta_ejemplo.html')

    # 2. Lexer: MedLang -> Lista de Tokens
    tokens = analizar_lexico(codigo_medlang)

    # 3. Parser: Lista de Tokens -> Árbol Sintáctico
    parser = AnalizadorSintactico(tokens)
    arbol = parser.parsear()

    # 4. Generator: Árbol Sintáctico -> SQL
    codigo_sql_final = generar_sql(arbol)

    print("=== SQL FINAL GENERADO ===")
    print(codigo_sql_final)