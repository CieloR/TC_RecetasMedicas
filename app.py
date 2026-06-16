from flask import Flask, render_template, request, redirect, flash
import os
from extractor import html_a_medlang
from lexer import analizar_lexico
from parser import AnalizadorSintactico
from generator import generar_sql

app = Flask(__name__)
app.secret_key = "clave_secreta_para_alertas"

# Ruta principal: Muestra la página de carga
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar si el usuario subió un archivo
        if 'archivo_receta' not in request.files:
            return redirect(request.url)
            
        file = request.files['archivo_receta']
        
        if file.filename == '':
            return redirect(request.url)
            
        if file and file.filename.endswith('.html'):
            # Guardamos temporalmente el archivo subido
            ruta_temporal = os.path.join(os.getcwd(), 'temp_receta.html')
            file.save(ruta_temporal)
            
            try:
                # 1. Ejecutamos nuestro pipeline del compilador
                codigo_medlang = html_a_medlang(ruta_temporal)
                tokens = analizar_lexico(codigo_medlang)
                
                parser = AnalizadorSintactico(tokens)
                arbol = parser.parsear()
                
                sql_final = generar_sql(arbol)
                
                # Eliminamos el archivo temporal una vez procesado
                if os.path.exists(ruta_temporal):
                    os.remove(ruta_temporal)
                
                # Enviamos todos los resultados a la interfaz web
                return render_template('index.html', 
                                       resultado=True,
                                       codigo_medlang=codigo_medlang,
                                       tokens=tokens,
                                       arbol=arbol,
                                       sql=sql_final)
                                       
            except Exception as e:
                if os.path.exists(ruta_temporal):
                    os.remove(ruta_temporal)
                return render_template('index.html', error=str(e))
                
    return render_template('index.html', resultado=False)

if __name__ == '__main__':
    app.run(debug=True)