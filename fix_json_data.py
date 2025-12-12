#!/usr/bin/env python3
"""
Script para corregir la estructura de los archivos JSON.

Ahora sobrescribe los archivos originales (sin crear copias _fixed) para
garantizar que todo el contenido quede listo para la aplicación sin
tareas manuales de limpieza.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any


def mapear_campo(campo_viejo: str) -> str:
    """Mapea nombres de campos viejos a nuevos"""
    mapeo = {
        'conceptos_clave': '1_conceptos_clave',
        'utilidad_practica': '2_utilidad_practica',
        'mapa_conocimiento': '3_relaciones',
        'contexto_profesional': '4_aplicaciones_industria',
        'actividad_practica': '6_reto_proyecto'
    }
    return mapeo.get(campo_viejo, campo_viejo)


def extraer_aplicaciones_industria(contexto: Dict) -> Dict[str, Any]:
    """Extrae y formatea la sección de aplicaciones en industria"""
    aplicaciones = contexto.get('aplicaciones_industria', {})
    
    return {
        'titulo': aplicaciones.get('titulo', '¿Dónde se usa en el mundo real?'),
        'sectores': aplicaciones.get('sectores', []),
        'empresas_que_lo_usan': aplicaciones.get('empresas_referencia', [])
    }


def extraer_roles_laborales(contexto: Dict) -> Dict[str, Any]:
    """Extrae y formatea la sección de roles laborales"""
    roles = contexto.get('roles_laborales', {})
    
    return {
        'titulo': roles.get('titulo', '¿En qué puestos es indispensable?'),
        'roles': roles.get('roles', []),
        'salario_promedio_mx': roles.get('salario_promedio_mx', 'No especificado')
    }


def transformar_actividad(actividad: Dict) -> Dict[str, Any]:
    """Transforma la sección de actividad práctica"""
    tipo = actividad.get('tipo', 'conceptual')
    
    resultado = {
        'tipo': 'programacion' if tipo == 'reto_programacion' else 'conceptual',
        'titulo': actividad.get('titulo', ''),
        'descripcion': actividad.get('descripcion', ''),
        'dificultad': actividad.get('dificultad', 'intermedio')
    }
    
    if tipo == 'reto_programacion':
        # Es un reto de programación
        resultado.update({
            'codigo_inicial': actividad.get('codigo_plantilla', actividad.get('codigo_inicial', '')),
            'solucion_referencia': actividad.get('solucion_referencia', ''),
            'pistas': actividad.get('instrucciones', actividad.get('pistas', [])),
            'casos_prueba_visibles': transformar_casos_prueba(actividad.get('casos_prueba', [])),
            'recursos_adicionales': actividad.get('recursos_adicionales', [])
        })
    else:
        # Es un proyecto conceptual
        resultado.update({
            'objetivos': actividad.get('instrucciones', []),
            'pasos_sugeridos': actividad.get('pasos', actividad.get('instrucciones', [])),
            'recursos_adicionales': actividad.get('recursos_adicionales', [])
        })
    
    return resultado


def transformar_casos_prueba(casos: list) -> list:
    """Transforma casos de prueba al formato esperado"""
    casos_transformados = []
    
    for caso in casos:
        caso_nuevo = {
            'entrada': caso.get('entrada', {}),
            'salida_esperada': caso.get('salida_esperada'),
            'explicacion': caso.get('nota', caso.get('explicacion', ''))
        }
        casos_transformados.append(caso_nuevo)
    
    return casos_transformados


def corregir_estructura(data: Dict) -> Dict[str, Any]:
    """
    Corrige la estructura del JSON para que coincida con los modelos.
    
    Estructura vieja:
    {
      "modulo_educativo": {
        "metadata": {...},
        "contenido": {
          "conceptos_clave": {...},
          ...
        },
        "actividad_practica": {...}
      }
    }
    
    Estructura nueva:
    {
      "metadata": {...},
      "1_conceptos_clave": {...},
      "2_utilidad_practica": {...},
      ...
    }
    """
    
    # Verificar si ya tiene la estructura correcta
    if 'metadata' in data and '1_conceptos_clave' in data:
        print("  ✓ Estructura ya correcta")
        return data
    
    # Verificar si tiene la estructura vieja
    if 'modulo_educativo' not in data:
        print("  ⚠ Estructura desconocida")
        return data
    
    modulo = data['modulo_educativo']
    contenido = modulo.get('contenido', {})
    contexto = contenido.get('contexto_profesional', {})
    
    # Construir nueva estructura
    nuevo = {
        'metadata': modulo.get('metadata', {})
    }
    
    # 1. Conceptos Clave
    if 'conceptos_clave' in contenido:
        ck = contenido['conceptos_clave']
        nuevo['1_conceptos_clave'] = {
            'titulo': ck.get('titulo', '¿Qué es esto?'),
            'contenido': ck.get('definicion', ck.get('contenido', '')),
            'puntos_clave': ck.get('puntos_clave', []),
            'formulas': transformar_formulas(ck.get('formulas', []))
        }
    
    # 2. Utilidad Práctica
    if 'utilidad_practica' in contenido:
        up = contenido['utilidad_practica']
        nuevo['2_utilidad_practica'] = {
            'titulo': up.get('titulo', '¿Para qué sirve?'),
            'contenido': up.get('descripcion', up.get('contenido', '')),
            'aplicaciones': up.get('aplicaciones_comunes', up.get('aplicaciones', [])),
            'ejemplos_vida_real': up.get('ejemplos_vida_real', [])
        }
    
    # 3. Relaciones
    if 'mapa_conocimiento' in contenido:
        mk = contenido['mapa_conocimiento']
        nuevo['3_relaciones'] = {
            'titulo': mk.get('titulo', 'Conceptos relacionados'),
            'prerequisitos': mk.get('prerequisitos', []),
            'temas_siguientes': mk.get('temas_siguientes', []),
            'conceptos_auxiliares': mk.get('conceptos_auxiliares', [])
        }
    
    # 4. Aplicaciones en Industria
    if contexto:
        nuevo['4_aplicaciones_industria'] = extraer_aplicaciones_industria(contexto)
    
    # 5. Roles Laborales
    if contexto:
        nuevo['5_roles_laborales'] = extraer_roles_laborales(contexto)
    
    # 6. Reto/Proyecto
    if 'actividad_practica' in modulo:
        nuevo['6_reto_proyecto'] = transformar_actividad(modulo['actividad_practica'])
    
    return nuevo


def transformar_formulas(formulas: list) -> list:
    """Transforma fórmulas al formato esperado"""
    formulas_transformadas = []
    
    for formula in formulas:
        if isinstance(formula, str):
            # Es una string simple, convertir a dict
            formulas_transformadas.append({
                'latex': formula,
                'descripcion': ''
            })
        elif isinstance(formula, dict):
            # Ya es un dict, verificar formato
            formulas_transformadas.append({
                'latex': formula.get('latex', formula.get('formula', '')),
                'descripcion': formula.get('descripcion', '')
            })
    
    return formulas_transformadas


def procesar_archivo(ruta: Path):
    """Procesa un archivo JSON individual y lo sobrescribe"""
    print(f"\n📄 Procesando: {ruta.name}")
    
    try:
        # Leer archivo
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Corregir estructura
        data_corregida = corregir_estructura(data)
        
        # Guardar siempre en el mismo archivo para no dejar copias
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data_corregida, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ Guardado en: {ruta.name}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def procesar_directorio(directorio: Path):
    """Procesa todos los archivos JSON en un directorio recursivamente"""
    archivos_procesados = 0
    archivos_exitosos = 0
    
    # Buscar todos los archivos .json
    for archivo in directorio.rglob("*.json"):
        # Ignorar archivos que ya terminan en _fixed.json
        if archivo.name.endswith('_fixed.json'):
            continue
        
        # Ignorar curriculum.json
        if archivo.name == 'curriculum.json':
            continue
        
        archivos_procesados += 1
        if procesar_archivo(archivo):
            archivos_exitosos += 1
    
    return archivos_procesados, archivos_exitosos


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Corrige la estructura de archivos JSON para Wikia Cognitiva',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:

    Sin argumentos (por defecto procesa src/data/content/):
        python fix_json_data.py

    Procesar un archivo (sobrescribe el original):
        python fix_json_data.py src/data/content/semestre_1/algebra_superior/algebra_booleana.json
  
    Procesar un directorio específico:
        python fix_json_data.py alguna/otra/ruta
        """
    )

    parser.add_argument(
        'ruta',
        nargs='?',
        default=None,
        help='Ruta al archivo o directorio; si se omite, usa src/data/content/'
    )
    
    args = parser.parse_args()
    
    # Ruta por defecto: carpeta de contenidos
    default_dir = Path(__file__).parent / "src" / "data" / "content"
    ruta = Path(args.ruta) if args.ruta else default_dir
    
    if not ruta.exists():
        print(f"❌ Error: La ruta '{ruta}' no existe")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("  CORRECTOR DE ESTRUCTURA JSON - WIKIA COGNITIVA")
    print("="*70)
    
    if ruta.is_file():
        # Procesar archivo individual
        if procesar_archivo(ruta):
            print("\n✅ Archivo procesado exitosamente")
        else:
            print("\n❌ Error procesando archivo")
            sys.exit(1)
    
    elif ruta.is_dir():
        # Procesar directorio
        print(f"\n📁 Procesando directorio: {ruta}")
        print("⚠️  MODO: Sobrescribir archivos originales")
        
        total, exitosos = procesar_directorio(ruta)
        
        print("\n" + "="*70)
        print(f"📊 RESUMEN")
        print("="*70)
        print(f"  Archivos procesados: {total}")
        print(f"  Exitosos: {exitosos}")
        print(f"  Fallidos: {total - exitosos}")
        
        if exitosos == total:
            print("\n✅ Todos los archivos procesados correctamente")
        else:
            print(f"\n⚠️  {total - exitosos} archivos con errores")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()