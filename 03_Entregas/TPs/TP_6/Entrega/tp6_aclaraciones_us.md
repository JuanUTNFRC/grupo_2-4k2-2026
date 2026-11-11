# TP 6 - Aclaraciones de la User Story "Inscribirme a actividad"

**Grupo:** 2 - 4K2 - 2026
**Caso de estudio:** EcoHarmony Park

## Propósito del documento

El enunciado del caso de estudio y la User Story no definen varias reglas de negocio necesarias para implementar y probar la funcionalidad (cupos, horarios, días de apertura, talles, etc.). Este documento registra las reglas que el grupo definió para cubrir esos huecos. Cada regla indica su origen:

- **Enunciado:** surge del enunciado del caso de estudio o de la User Story.
- **Guía del PO:** surge de la guía de preguntas frecuentes publicada por los PO ("FAQ PO TDD EcoHarmony Park"). Se indica el número de pregunta.
- **Definida por el grupo:** no está especificada y fue decidida por el grupo.

Cuando la guía del PO se publicó, varias reglas que el grupo había definido se corrigieron para respetarla. Esas reglas ahora citan la pregunta de la guía.

## User Story

> **Inscribirme a actividad** (5 puntos)
>
> **COMO** visitante **QUIERO** inscribirme a una actividad **PARA** reservar mi lugar en la misma.

### Criterios de aceptación

1. Debe requerir seleccionar una actividad del conjunto de actividades de la lista de "Tirolesa", "Safari", "Palestra" y "Jardinería", siempre y cuando tengan cupos disponibles para el horario seleccionado.
2. Debe requerir seleccionar el horario dentro de los disponibles.
3. Debe indicar la cantidad de personas que participarán de la actividad.
4. Para cada persona que participa, debe ingresar los datos del visitante: nombre, DNI, edad y talla de vestimenta si la actividad lo demanda.
5. Debe requerir aceptar los términos y condiciones específicos de la actividad en la que participarán.
6. Al finalizar la inscripción, se debe enviar un correo electrónico con información de la inscripción realizada. Debe contener un código QR.

### Pruebas de usuario

| ID | Prueba | Resultado esperado |
|----|--------|--------------------|
| PU1 | Inscribirse a una actividad del listado que posee cupos disponibles, seleccionando un horario, ingresando los datos del visitante (nombre, DNI, edad, talla si la actividad lo requiere), aceptando los términos y condiciones y recibiendo el email de confirmación. | Pasa |
| PU2 | Inscribirse a una actividad que no tiene cupo para el horario seleccionado. | Falla |
| PU3 | Inscribirse a una actividad sin ingresar talle de vestimenta porque la actividad no lo requiere. | Pasa |
| PU4 | Inscribirse a una actividad seleccionando un horario en el cual el parque está cerrado o la actividad no está disponible. | Falla |
| PU5 | Inscribirse a una actividad sin aceptar los términos y condiciones de la actividad. | Falla |
| PU6 | Inscribirse a una actividad sin ingresar el talle de vestimenta requerido por la actividad. | Falla |

## Reglas de negocio

### RN1 - Actividades

| Actividad | Cupo por horario | Requiere talle | Edad mínima |
|-----------|------------------|----------------|-------------|
| Tirolesa | 10 | Sí (arnés) | 8 años |
| Safari | 8 | No | Todas las edades |
| Palestra | 12 | Sí (arnés) | 12 años |
| Jardinería | 12 | No | Todas las edades |

- Las cuatro actividades son las del enunciado. **(Enunciado)**
- Los cupos por horario. **(Guía del PO, pregunta 13)**
- Las actividades que requieren talle de vestimenta: Palestra y Tirolesa. **(Guía del PO, pregunta 9)**
- La edad mínima por actividad. **(Guía del PO, pregunta 15)**
- Cada actividad tiene sus propios términos y condiciones. **(Enunciado)**
- Una actividad puede estar desactivada por el administrador. Una actividad desactivada no admite inscripciones ("la actividad no está disponible", PU4). **(Definida por el grupo)**

### RN2 - Horarios

- Cada actividad dura una hora. **(Enunciado)**
- Los horarios se ofrecen cada una hora, de 09:00 a 17:00. A las 18:00 no hay turno: es la cota superior. **(Guía del PO, pregunta 12)**
- La inscripción a un horario **abre 24 horas antes** de su inicio. Por ejemplo, un martes no se puede inscribir a una actividad del viernes. **(Guía del PO, pregunta 23)**
- La inscripción a un horario **cierra 15 minutos antes** de su inicio. **(Guía del PO, pregunta 30)**
- Un horario es **disponible** cuando cumple todas estas condiciones:
  - existe y pertenece a la actividad seleccionada;
  - la actividad está activa;
  - la inscripción está abierta: faltan 24 horas o menos para el inicio y más de 15 minutos;
  - cae en un día y hora en que el parque está abierto (RN3).

### RN3 - Calendario del parque

**(Guía del PO, preguntas 1 y 11)**

- El parque abre de **martes a domingo**, de **08:30 a 19:00**.
- El parque permanece **cerrado todos los lunes**, el **1 de enero** y el **25 de diciembre**.
- Un horario solo es válido si la actividad empieza y termina dentro del horario de apertura del parque.

### RN4 - Cupos

- El cupo disponible de un horario es: `cupo por horario de la actividad − participantes ya inscriptos en ese horario`. Se calcula, no se almacena. **(Definida por el grupo)**
- Una inscripción se rechaza si la cantidad de participantes supera el cupo disponible. Completar exactamente el cupo disponible está permitido. **(Definida por el grupo)**

### RN5 - Participantes

- Se debe indicar al menos **un** participante. No hay otro tope que el cupo disponible del horario. **(Guía del PO, pregunta 31)**
- Por cada participante se ingresa nombre, DNI, edad y talle si la actividad lo requiere. **(Enunciado)**
- Validaciones de los datos **(definidas por el grupo)**:
  - **Nombre:** obligatorio.
  - **DNI:** obligatorio, de 7 u 8 dígitos numéricos. Solo se acepta DNI, no pasaporte. **(Guía del PO, pregunta 32)**
  - **Edad:** obligatoria, número entero entre 1 y 130.
  - **Edad mínima:** cada participante debe tener la edad mínima de la actividad (RN1). **(Guía del PO, pregunta 15)**
  - **Talle:** obligatorio solo si la actividad lo requiere. Valores posibles: XS, S, M, L, XL, XXL. **(Guía del PO, pregunta 14)**
- Un mismo DNI **no puede inscribirse dos veces a la misma hora**: ni en el mismo horario, ni en otra actividad que empieza el mismo día a la misma hora. Vale tanto dentro de la misma inscripción como en inscripciones distintas. **(Guía del PO, pregunta 29)**

### RN6 - Términos y condiciones

- Sin la aceptación de los términos y condiciones de la actividad no se puede realizar la inscripción. **(Enunciado)**
- La aceptación queda registrada en la inscripción como evidencia del consentimiento. **(Definida por el grupo)**

### RN7 - Correo de confirmación

- Al finalizar la inscripción se envía un correo con el resumen de la inscripción y el código QR. **(Enunciado; Guía del PO, pregunta 28)**
- El correo se envía al email de la cuenta del usuario, ya que los datos de cada participante no incluyen email. **(Definida por el grupo)**
- El correo contiene **(definida por el grupo)**:
  - código de la inscripción;
  - actividad, fecha y hora;
  - listado de participantes (nombre, DNI y talle si corresponde);
  - código QR que codifica el código de la inscripción.
- Si la inscripción es rechazada, no se envía ningún correo. **(Definida por el grupo)**

## Identidad visual

- Fuente **Lato** y la paleta `#386641`, `#6a994e`, `#a7c957`, `#f2e8cf` y `#bc4749`. **(Guía del PO, pregunta 3)** Los verdes claros no alcanzan el contraste mínimo de texto sobre el fondo, así que se usan en tintes, bordes y en el tema oscuro. Los textos de error usan una variante más oscura de `#bc4749`.
- **Logo:** el grupo diseñó una propuesta (`front/img/logo.svg` y el emblema `front/img/emblema.svg`), que se envía al PO para su validación. **(Guía del PO, pregunta 17)**
- **Términos y condiciones:** uno diferente por cada actividad, redactado por el grupo, que se envía al PO para su validación. **(Guía del PO, pregunta 16)**

## Fuera de alcance

| Ítem | Motivo |
|------|--------|
| Registro e inicio de sesión de usuarios | La User Story no lo requiere: se puede comenzar con la sesión y el usuario mockeados (Guía del PO, pregunta 19). Se utiliza un usuario de prueba con email cargado. |
| Alta y edición de actividades y horarios desde la app | El enunciado indica que los administradores lo gestionan por fuera de la aplicación. Se utiliza el panel de administración de Django. |
| Autocompletar los datos del titular de la cuenta | No está entre los criterios de aceptación. Requeriría guardar DNI y edad en el usuario. |
| Consulta de "mis actividades" | No está entre los criterios de aceptación. |

## Trazabilidad

| Prueba de usuario | Reglas involucradas |
|-------------------|---------------------|
| PU1 | RN1, RN2, RN3, RN4, RN5, RN6, RN7 |
| PU2 | RN4 |
| PU3 | RN1, RN5 |
| PU4 | RN1, RN2, RN3 |
| PU5 | RN6 |
| PU6 | RN1, RN5 |
