# Wikia A COGNITIVA  
## Arquitectura Extendida de Conocimiento para Estudiantes de Inteligencia Artificial  
### Sistema de Conexión Concepto → Práctica → Industria

## Descripción General

Wikia Cognitiva es una plataforma educativa diseñada para reducir la brecha entre los contenidos teóricos de la Licenciatura en Inteligencia Artificial y sus aplicaciones reales en la industria tecnológica. Su propósito es ofrecer una representación clara, comprensible y contextualizada de los conceptos fundamentales que se estudian durante los primeros semestres, permitiendo al estudiante comprender qué está aprendiendo, por qué es relevante y cómo se utiliza en entornos profesionales.

Este proyecto surge de una problemática común en la formación de estudiantes de IA: comprender los temas de manera operativa, pero sin tener claridad sobre el propósito final de procedimientos matemáticos, programación o estructuras teóricas que se estudian dentro del plan curricular. En numerosas ocasiones, la pregunta “¿y esto para qué sirve?” no encontraba una respuesta satisfactoria más allá de “porque viene en el plan de estudios”.

Wikia Cognitiva plantea una solución estructurada y escalable a este problema mediante un sistema que organiza, explica y contextualiza cada tema clave de los primeros cuatro semestres de la carrera.

---

## Objetivo

Proporcionar un marco conceptual y práctico que conecte la teoría académica con aplicaciones concretas en la industria tecnológica.  
El objetivo central es permitir al estudiante comprender:

- Qué está estudiando (concepto).  
- Para qué sirve en la práctica (utilidad).  
- En qué áreas o herramientas se usa (industria).  
- Qué roles laborales requieren ese conocimiento (profesionalización).  
- Cómo puede aplicarse en un ejercicio o proyecto (reto práctico).  

Con ello se busca crear una experiencia educativa más significativa, aplicada y coherente con el entorno laboral actual.

---

## Características Principales

1. **Navegación estructurada por semestres**  
   El sistema organiza los primeros cuatro semestres de la licenciatura, mostrando cada materia y su temario correspondiente.

2. **Desglose temático detallado**  
   Cada tema del plan curricular incluye seis secciones obligatorias:
   - Conceptos clave  
   - Utilidad práctica  
   - Relaciones con otros temas  
   - Aplicaciones en la industria  
   - Roles laborales  
   - Reto o proyecto práctico  

3. **Repositorio de conocimiento estructurado**  
   Toda la información está representada en formato JSON para permitir escalabilidad y edición sencilla.

4. **Interfaz intuitiva**  
   Menús por semestre, materias y contenido temático, con lectura clara y organizada.

5. **Integración de retos de programación**  
   Cada vez que el tema lo permite, se incluye un ejercicio práctico con plantilla y solución de referencia.

6. **Compatibilidad con tema claro y oscuro**  
   Orientado a la legibilidad y adaptación a preferencias del usuario.

---

## Instalación

Es necesario contar con Python 3.10 o superior.  
Las dependencias se instalan mediante:
pip install -r requirements.txt

---

## Uso

Para iniciar la aplicación:

python src/main.py


El sistema cargará automáticamente el contenido curricular y la navegación correspondiente.

---

## Arquitectura del Proyecto

La estructura principal es la siguiente:

- `src/`  
  Código central de la aplicación, navegación y renderizado.

- `data/`  
  Archivos JSON que contienen semestres, materias, temas y contenido educativo.

- `docs/`  
  Documentación técnica adicional sobre arquitectura, objetivos pedagógicos y diseño de software.

- `assets/`  
  Recursos gráficos, configuraciones y materiales de apoyo.

---

## Metodología Pedagógica

El proyecto está sustentado en tres principios:

1. **Aprendizaje significativo**  
   Relación clara entre teoría académica y su relevancia en problemas reales.

2. **Conexión transversal del conocimiento**  
   Visualización de relaciones entre temas y comprensión integral del plan curricular.

3. **Proyección profesional**  
   Exposición explícita de las áreas laborales, herramientas y roles donde se aplican los conceptos estudiados.

---

## Alcance

Actualmente, Wikia Cognitiva cubre los primeros cuatro semestres de la Licenciatura en Inteligencia Artificial.  
Futuros desarrollos incluirán:

- Visualización gráfica de mapas cognitivos.
- Módulos interactivos para simulaciones.
- Expansión hacia semestres posteriores.
- Recomendadores de rutas de estudio basados en progreso y afinidad temática.

---

## Licencia

Indicar la licencia correspondiente (MIT, Apache 2.0, GPL, etc.) según los requisitos del proyecto.

