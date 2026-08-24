# Grupo_2-4k2-2026
**Institución:** Universidad Tecnológica Nacional - Facultad Regional Córdoba

**Carrera:** Ingeniería en Sistemas de Información

**Asignatura:** Ingeniería y Calidad de Software

**Año:** 2026

**Comisión:** 4k2

**Grupo:** 2

# Integrantes del grupo

| Apellidos |Nombres | Legajo |
| --------- | --------- |--------| 
| Maldonado | Gustavo Emiliano | 93370 |
| Quispe Ricra | Junior Jesus | 97139 |
| D'Andrea Escoda | Thiago Augusto | 87381 |
| Pons            | Katerinne      |91093  |
| Rolando Corbalan  |Javier Efrain |401363 |
| Giannantonio |Fabrizio Giael |401422 |
| Piaggio   | Uriel Agustin     | 87599 |
| Melkón | Emanuel Sebastián | 401423 |
| Cruz | María Victoria | 407549 |
| Chaui | Camilo | 95148 |
|Soria  |Mikaela Carolina|84829|
# Estructura del repositorio

```

grupo_2-4k2_2026
├── 01_Catedra/                 # Material provisto por los profesores (enunciados, guías)  
│   ├── Bibliografia/ 
│   │       ├── Material_de_referencia/
│   │       │   ├── Agilismo/
│   │       │   ├── Gestion_de_configuracion_de_software/
│   │       │   ├── Ingenieria_de_software/
│   │       │   ├── Lean_y_kanban/
│   │       │   ├── Test_driven_development/
│   │       │   └── Testing_de_software/
│   │       ├── Material_recomendado_en_clase/
│   │       ├── Presentaciones/
│   │       └── Clases_grabadas/
│   ├── Modalidad/
│   ├── Templates_para_practicos_y_parciales/
│   └── Parciales/
├── 02_Gestion_grupo/ 
│   ├── Comunicacion_docente/                    # Medio de comunicacion con los docentes y formato sugerido
│   │   ├──Mails/
│   │   └── Otros
│   ├── Minutas/                                 # Minutas de reunión, cronogramas y el Plan de SCM.
│   └── Cronograma/                              # Planificación y seguimiento
├── 03_Entregas/                                 # Trabajos entregables
│   ├── TIs/                                     # Trabajos de Investigación
│   │   └── TI_[N]/                           
│   │       ├── Consigna/
│   │       └── Entrega/                    
│   └── TPs/                                     # Trabajos Prácticos             
│       └── TP_[N]/ 
│           ├── Consigna/
│           └── Entrega/                          
├── 04_Producto/                         # Artefactos que forman parte del producto 
│   ├── Documentacion/                   # ERS, Arquitectura, Manuales.
│   └── Codigo_fuente/                   # Repositorio del código desarrollado en el TP 6.
└── 05_Material_extra/
    ├── Clases/
    │   └── Clase_[yyyy_mm_dd]_[Descripcion]/ 
    └── Otros    
 ``` 
# Nomenclatura
Los nombres de las carpetas deberán comenzar con mayúscula y utilizar guion bajo (`_`) como separador entre palabras. Los nombres de los archivos deberán escribirse estrictamente en minúsculas, sin tildes ni caracteres especiales, utilizando guion bajo (`_`) como separador entre palabras.

| Ítem de Configuración (SCI) | Ubicación                                                 | Regla de nombrado                      
| --------------------------- | --------------------------------------------------------- | ----------------------------------------- |
| README | `/`| `README.md`|
| Material de referencia      | `/01_Catedra/Bibliografia/Material_de_referencia/`| `[nombre].[extension]`|
| Material recomendado | `/01_Catedra/Bibliografia/Material_recomendado_en_clase/` | `[nombre].[extension]`                 |
| Presentaciones | `/01_Catedra/Bibliografia/Presentaciones` | `[nombre].[extension]`                     |
| Clases grabadas | `/01_Catedra/Bibliografia/Clases_grabadas/`               | `clases_grabadas.xlsx`         |
| Modalidad                   | `/01_Catedra/Modalidad/` | `[nombre_del_documento].pdf`                |
| Templates                   | `/01_Catedra/Templates_para_practicos_y_parciales/` | `[tipo_de_template].[extension]`                    |
| Parciales                   | `/01_Catedra/Parciales/`        | `[nombre_o_descripcion].[extension]`                |
| Mails                 | `/02_Gestion_grupo/Mails`                                      | `[asunto].pdf`                       |
| Otras comunicaciones                 | `/02_Gestion_grupo/Otro`                                      | `[asunto]_[medio].[extension]` |
| Minuta de reunión           | `/02_Gestion_grupo/Minutas/`                              | `minuta_[yyyy_mm_dd].pdf`                 |
| Cronograma                  | `/02_Gestion_grupo/Cronograma/`                           | `cronograma_g[N].xlsx`                    |
| Trabajo Práctico            | `/03_Entregas/TPs/TP_[N]/Entrega/`                        | `tp[N]_[nombre_corto]_g[N].pdf`           |
| Trabajo de Investigación    | `/03_Entregas/TIs/TI_[N]/Entrega/`                   | `ti[N]_[nombre_corto]_g[N].pdf`           |
| User Stories                | `/03_Entregas/TPs/TP_[N]/Entrega/`                        | `tp[N]_req_[ejercicio]_user_stories.md`   |
| MVP                         | `/03_Entregas/TPs/TP_[N]/Entrega/`                        | `tp[N]_req_[ejercicio]_mvp.pdf`           |
| Estimaciones                | `/03_Entregas/TPs/TP_[N]/Entrega/`                        | `tp[N]_req_[ejercicio]_estimaciones.xlsx` |
| Casos de prueba             | `/03_Entregas/TPs/TP_[N]/Entrega/`                        | `tp[N]_tst_[ejercicio]_casos_prueba.md`   |
| Retrospectiva de Sprint     | `/03_Entregas/TPs/TP_[N]/Entrega/`                        | `tp[N]_scr_retrospective_sprint_[N].md`   |
| Requerimientos (ERS)        | `/04_Producto/Documentacion/`                             | `ers_[nombre_producto].pdf`               ||
| Arquitectura                | `/04_Producto/Documentacion/`                             | `arquitectura_[nombre_producto].pdf`      |
| Código fuente               | `/04_Producto/Codigo_fuente/`                             | `[nombre_modulo].[extension]`             |
| Manual de usuario           | `/04_Producto/Documentacion/`                             | `manual_usuario_[nombre_producto].pdf`|
|Notas de clases| `/05_Material_extra/Clases/Clase_[yyyy_mm_dd]_[Descripcion]/`               | `clase_[yyyy_mm_dd]_[descripcion].[extension]`         |
| Otros | `/05_Material_extra/Clases/Otros`| `[nombre]_[extension]` |


# Glosario

| Sigla | Significado |
| ------- | -------------------------------------------------------------------------- |
| **TIs** | Trabajos de Investigación |
| **TPs** | Trabajos Prácticos |
| **TI** | Trabajo de Investigación |
| **TP** | Trabajo Práctico |
| **SCM** | Gestión de Configuración de Software (*Software Configuration Management*) |
| **SCI** | Ítem de Configuración de Software (*Software Configuration Item*) |
| **N**   | Número de ítem o trabajo (1, 2, ..., n) |
| **G**   | Número de grupo |
| **REQ** | Requerimientos |
| **TST** | Testing |
| **SCR** | Scrum |
| **MVP** | Producto Mínimo Viable (*Minimum Viable Product*) |
| **LB**  | Línea Base |
| **ERS** | Especificación de Requisitos de Software |




# Línea Base

## Historial de Líneas Base

| Línea Base | Fecha| Descripción |
| --------- | --------- |--------|
|  |  |  |

## Criterios de Línea Base

### 1.  Establecimiento de Línea Base

Se marcará una nueva línea base inmediatamente después de la entrega formal de cada tarea evaluable, como Trabajos Prácticos o Trabajos de Investigación.

### 2 . Convención de Etiquetas (Tags)
Para mantener consistencia, las etiquetas en Git se escribirán en minúscula, sin espacios ni caracteres especiales.


Regla de nombrado para tags:

`base_tp[N]_[nombre_corto]`

Ejemplo:

`base_tp4_SCM`
 
