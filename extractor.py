from bs4 import BeautifulSoup

def html_a_medlang(ruta_html):
    # 1. Leer el archivo HTML estético
    with open(ruta_html, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    
    soup = BeautifulSoup(contenido, 'html.parser')
    
    # 2. Extraer datos del Paciente
    dni = soup.find(id='dni').text.strip()
    nombre = soup.find(id='nombre').text.strip()
    # Limpiamos "21 años" para quedarnos solo con el número 21
    edad = ''.join(filter(str.isdigit, soup.find(id='edad').text))
    sexo = soup.find(id='sexo').text.strip()
    
    # 3. Extraer datos de la Consulta
    fecha = soup.find(id='fecha').text.strip()
    diagnostico = soup.find(id='diagnostico').text.strip()
    alergias = soup.find(id='alergias').text.strip()
    
    # 4. Construir las primeras líneas de nuestro Lenguaje Intermedio
    lineas_medlang = []
    lineas_medlang.append(f'CREAR_PACIENTE -> DNI={dni}, NOMBRE="{nombre}", EDAD={edad}, SEXO="{sexo}";')
    lineas_medlang.append(f'REGISTRAR_CONSULTA -> DNI={dni}, FECHA="{fecha}", DIAGNOSTICO="{diagnostico}", ALERGIAS="{alergias}";')
    
    # 5. Extraer todos los medicamentos (soporta múltiples bloques automáticamente)
    items_medicamentos = soup.find_all(class_='med-item')
    for item in items_medicamentos:
        generico = item.find(class_='med-generico').text.strip()
        dosis = item.find(class_='med-dosis').text.strip()
        pres = item.find(class_='med-pres').text.strip()
        via = item.find(class_='med-via').text.strip()
        frec = item.find(class_='med-frec').text.strip()
        tiempo = item.find(class_='med-tiempo').text.strip()
        
        lineas_medlang.append(
            f'AGREGAR_MEDICAMENTO -> DNI={dni}, GENERICO="{generico}", PRES="{pres}", '
            f'DOSIS="{dosis}", FREC="{frec}", VIA="{via}", TIEMPO="{tiempo}";'
        )
    
    # Unimos todas las instrucciones con saltos de línea
    return "\n".join(lineas_medlang)

# --- PRUEBA LOCAL ---
if __name__ == '__main__':
    # Suponiendo que guardaste el HTML anterior como 'receta_ejemplo.html'
    codigo_intermedio = html_a_medlang('receta_ejemplo.html')
    print("=== CÓDIGO INTERMEDIO GENERADO (MedLang) ===")
    print(codigo_intermedio)