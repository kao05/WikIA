"""
Validador de contenido para Wikia Cognitiva
Verifica que todos los archivos JSON de temas tengan la estructura correcta
con las 6 secciones obligatorias.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import sys

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Secciones obligatorias que debe tener cada tema
SECCIONES_OBLIGATORIAS = [
    "metadata",
    "1_conceptos_clave",
    "2_utilidad_practica",
    "3_relaciones",
    "4_aplicaciones_industria",
    "5_roles_laborales",
    "6_reto_proyecto"
]

# Campos obligatorios en metadata
CAMPOS_METADATA = [
    "id",
    "titulo",
    "materia",
    "semestre"
]

# Campos obligatorios en cada sección
CAMPOS_SECCIONES = {
    "1_conceptos_clave": ["titulo", "contenido"],
    "2_utilidad_practica": ["titulo", "contenido"],
    "3_relaciones": ["titulo"],
    "4_aplicaciones_industria": ["titulo"],
    "5_roles_laborales": ["titulo"],
    "6_reto_proyecto": ["tipo", "titulo", "descripcion"]
}

# Campos específicos según tipo de reto
CAMPOS_RETO_PROGRAMACION = ["codigo_inicial", "solucion_referencia"]
CAMPOS_RETO_CONCEPTUAL = ["objetivos"]


class ValidadorJSON:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.errores_totales = 0
        self.advertencias_totales = 0
        self.archivos_validados = 0
        self.archivos_con_errores = 0
        
    def validar_json_syntax(self, ruta_archivo: Path) -> Tuple[bool, str]:
        """Valida que el archivo sea un JSON válido"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, ""
        except json.JSONDecodeError as e:
            return False, f"Error de sintaxis JSON: {str(e)}"
        except Exception as e:
            return False, f"Error al leer archivo: {str(e)}"
    
    def validar_estructura_tema(self, data: dict, ruta_archivo: Path) -> List[str]:
        """Valida que el tema tenga todas las secciones obligatorias"""
        errores = []
        
        # Verificar secciones obligatorias
        for seccion in SECCIONES_OBLIGATORIAS:
            if seccion not in data:
                errores.append(f" Falta sección obligatoria: '{seccion}'")
            elif not data[seccion]:
                errores.append(f" Sección vacía: '{seccion}'")
        
        return errores
    
    def validar_metadata(self, metadata: dict) -> List[str]:
        """Valida que metadata tenga los campos requeridos"""
        errores = []
        
        if not metadata:
            return [" Metadata está vacío"]
        
        for campo in CAMPOS_METADATA:
            if campo not in metadata:
                errores.append(f" Falta campo en metadata: '{campo}'")
            elif not metadata[campo]:
                errores.append(f"  Campo vacío en metadata: '{campo}'")
        
        return errores
    
    def validar_seccion(self, nombre_seccion: str, data_seccion: dict) -> List[str]:
        """Valida que una sección tenga sus campos requeridos"""
        errores = []
        
        if nombre_seccion not in CAMPOS_SECCIONES:
            return errores
        
        campos_requeridos = CAMPOS_SECCIONES[nombre_seccion]
        
        for campo in campos_requeridos:
            if campo not in data_seccion:
                errores.append(f" Falta campo '{campo}' en sección '{nombre_seccion}'")
            elif not data_seccion[campo]:
                errores.append(f"  Campo vacío '{campo}' en sección '{nombre_seccion}'")
        
        return errores
    
    def validar_reto_proyecto(self, reto_data: dict) -> List[str]:
        """Valida la sección de reto/proyecto según su tipo"""
        errores = []
        
        tipo = reto_data.get('tipo', '')
        
        if tipo == 'programacion':
            for campo in CAMPOS_RETO_PROGRAMACION:
                if campo not in reto_data:
                    errores.append(f"  Reto de programación sin '{campo}'")
                elif not reto_data[campo]:
                    errores.append(f"  Campo vacío '{campo}' en reto de programación")
        
        elif tipo == 'conceptual':
            for campo in CAMPOS_RETO_CONCEPTUAL:
                if campo not in reto_data:
                    errores.append(f"  Proyecto conceptual sin '{campo}'")
        
        elif not tipo:
            errores.append(" Reto/Proyecto sin campo 'tipo' definido")
        
        return errores
    
    def validar_archivo(self, ruta_archivo: Path) -> Tuple[bool, List[str], List[str]]:
        """
        Valida un archivo JSON completo
        
        Returns:
            (es_valido, lista_errores, lista_advertencias)
        """
        errores = []
        advertencias = []
        
        # 1. Validar sintaxis JSON
        es_valido, error_msg = self.validar_json_syntax(ruta_archivo)
        if not es_valido:
            errores.append(error_msg)
            return False, errores, advertencias
        
        # 2. Cargar datos
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 3. Validar estructura general
        errores_estructura = self.validar_estructura_tema(data, ruta_archivo)
        errores.extend([e for e in errores_estructura if e.startswith('Error')])
        advertencias.extend([e for e in errores_estructura if e.startswith('Advertencia')])
        
        # 4. Validar metadata
        if 'metadata' in data:
            errores_metadata = self.validar_metadata(data['metadata'])
            errores.extend([e for e in errores_metadata if e.startswith('Error')])
            advertencias.extend([e for e in errores_metadata if e.startswith('Advertencia')])
        
        # 5. Validar cada sección
        for seccion in SECCIONES_OBLIGATORIAS[1:]:  # Saltar metadata
            if seccion in data:
                errores_seccion = self.validar_seccion(seccion, data[seccion])
                errores.extend([e for e in errores_seccion if e.startswith('Error')])
                advertencias.extend([e for e in errores_seccion if e.startswith('Advertencia')])
        
        # 6. Validar reto/proyecto específicamente
        if '6_reto_proyecto' in data:
            errores_reto = self.validar_reto_proyecto(data['6_reto_proyecto'])
            advertencias.extend(errores_reto)
        
        es_valido = len(errores) == 0
        return es_valido, errores, advertencias
    
    def validar_directorio(self, semestre: int = None):
        """
        Valida todos los archivos JSON en el directorio de contenido
        
        Args:
            semestre: Si se especifica, solo valida ese semestre (1-4)
        """
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE} VALIDADOR DE CONTENIDO - WIKIA COGNITIVA{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        # Determinar qué semestres validar
        if semestre:
            semestres = [semestre]
            print(f" Validando solo Semestre {semestre}...\n")
        else:
            semestres = [1, 2, 3, 4]
            print(f" Validando todos los semestres...\n")
        
        for sem in semestres:
            semestre_path = self.base_path / f"semestre_{sem}"
            
            if not semestre_path.exists():
                print(f"{Colors.YELLOW}Advertencia  Semestre {sem} no encontrado en {semestre_path}{Colors.END}")
                continue
            
            print(f"{Colors.BOLD}━━━ SEMESTRE {sem} ━━━{Colors.END}")
            
            # Recorrer cada materia
            for materia_dir in sorted(semestre_path.iterdir()):
                if not materia_dir.is_dir():
                    continue
                
                materia_nombre = materia_dir.name.replace('_', ' ').title()
                print(f"\n   {Colors.BOLD}{materia_nombre}{Colors.END}")
                
                # Buscar todos los archivos JSON en la materia
                archivos_json = list(materia_dir.glob("*.json"))
                
                if not archivos_json:
                    print(f"    {Colors.YELLOW}Advertencia  No hay archivos JSON en esta materia{Colors.END}")
                    continue
                
                # Validar cada archivo
                for archivo in sorted(archivos_json):
                    if archivo.name.startswith('_'):
                        continue  # Ignorar archivos de metadata o plantillas
                    
                    self.archivos_validados += 1
                    tema_nombre = archivo.stem.replace('_', ' ').title()
                    
                    es_valido, errores, advertencias = self.validar_archivo(archivo)
                    
                    if es_valido and not advertencias:
                        print(f"    {Colors.GREEN}✓{Colors.END} {tema_nombre}")
                    else:
                        if not es_valido:
                            self.archivos_con_errores += 1
                            print(f"    {Colors.RED}✗{Colors.END} {tema_nombre}")
                        else:
                            print(f"    {Colors.YELLOW}⚠{Colors.END} {tema_nombre}")
                        
                        # Mostrar errores
                        for error in errores:
                            print(f"        {Colors.RED}{error}{Colors.END}")
                            self.errores_totales += 1
                        
                        # Mostrar advertencias
                        for advertencia in advertencias:
                            print(f"        {Colors.YELLOW}{advertencia}{Colors.END}")
                            self.advertencias_totales += 1
        
        # Resumen final
        self.mostrar_resumen()
    
    def mostrar_resumen(self):
        """Muestra el resumen de la validación"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}📊 RESUMEN DE VALIDACIÓN{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        print(f"  Archivos validados: {Colors.BOLD}{self.archivos_validados}{Colors.END}")
        print(f"  Archivos con errores: {Colors.BOLD}{Colors.RED if self.archivos_con_errores > 0 else Colors.GREEN}{self.archivos_con_errores}{Colors.END}")
        print(f"  Total de errores: {Colors.BOLD}{Colors.RED if self.errores_totales > 0 else Colors.GREEN}{self.errores_totales}{Colors.END}")
        print(f"  Total de advertencias: {Colors.BOLD}{Colors.YELLOW if self.advertencias_totales > 0 else Colors.GREEN}{self.advertencias_totales}{Colors.END}")
        
        print()
        
        if self.errores_totales == 0 and self.advertencias_totales == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}¡TODOS LOS ARCHIVOS SON VÁLIDOS!{Colors.END}")
        elif self.errores_totales == 0:
            print(f"{Colors.YELLOW}{Colors.BOLD}  Archivos válidos pero con advertencias{Colors.END}")
        else:
            print(f"{Colors.RED}{Colors.BOLD} Hay errores que deben corregirse{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        # Código de salida
        sys.exit(0 if self.errores_totales == 0 else 1)


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validador de contenido para Wikia Cognitiva',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  
  Validar todos los semestres:
    python scripts/validate_all_content.py
  
  Validar solo el semestre 1:
    python scripts/validate_all_content.py --semestre 1
  
  Especificar ruta personalizada:
    python scripts/validate_all_content.py --path src/data/content
        """
    )
    
    parser.add_argument(
        '--semestre', '-s',
        type=int,
        choices=[1, 2, 3, 4],
        help='Validar solo un semestre específico (1-4)'
    )
    
    parser.add_argument(
        '--path', '-p',
        type=str,
        default='src/data/content',
        help='Ruta base del contenido (default: src/data/content)'
    )
    
    args = parser.parse_args()
    
    # Verificar que la ruta existe
    base_path = Path(args.path)
    if not base_path.exists():
        print(f"{Colors.RED} Error: La ruta '{base_path}' no existe{Colors.END}")
        print(f"\n segúrate de ejecutar desde el directorio raíz del proyecto:")
        print(f"   cd wikia-cognitiva")
        print(f"   python scripts/validate_all_content.py")
        sys.exit(1)
    
    # Crear validador y ejecutar
    validador = ValidadorJSON(base_path)
    validador.validar_directorio(semestre=args.semestre)


if __name__ == "__main__":
    main()
