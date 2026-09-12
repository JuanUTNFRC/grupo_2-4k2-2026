# 📚 ICS — Clase práctica 08/09/2026

## 1. Poker Estimation

### ¿Para qué sirve?

Para **estimar User Stories de manera relativa** usando Story Points.

La idea NO es decir:

> "Esta historia tardará exactamente 3 días."

Sino:

> "Esta historia es aproximadamente el doble de compleja/esforzada/incierta que nuestra referencia."

---

## 2. Proceso de Poker Estimation

El profesor explicó este proceso:

### Paso 1 — Elegir la User Story

Se toma una User Story que:

* está suficientemente refinada,
* está lista,
* cumple con **INVEST**,
* está arriba en el Product Backlog.

### Paso 2 — Cada integrante piensa su estimación

Cada uno analiza la historia considerando:

* complejidad,
* esfuerzo,
* incertidumbre.

Y elige una carta.

### Paso 3 — Se muestran las cartas

Todos muestran simultáneamente su valor.

### Paso 4 — Se buscan las discrepancias

No necesariamente se discuten todos los valores.

Se pide especialmente explicación a:

* quien puso el **valor más alto**;
* quien puso el **valor más bajo**.

### Paso 5 — Se explica el motivo

Por ejemplo:

> "Yo puse 8 porque no sé cómo vamos a implementar el QR y eso me genera mucha incertidumbre."

Otro podría decir:

> "Yo puse 3 porque ya usamos una librería para QR anteriormente."

### Paso 6 — Se vuelve a votar

⚠️ **Importantísimo:**

Después de escuchar las explicaciones:

> **SE VUELVE A VOTAR.**

No se termina directamente la estimación.

### Paso 7 — Se repite

Se puede repetir:

**votar → comparar → explicar → discutir → votar**

tantas veces como sea necesario.

### Paso 8 — Acuerdo

Finalmente el equipo llega a un valor.

⚠️ **NO se hace promedio.**

Por ejemplo:

* 5
* 5
* 5
* 3

→ se puede acordar **5**.

Pero:

* 2
* 2
* 3
* 3

→ NO:

> `(2+2+3+3)/4 = 2,5 → 3`

No funciona así.

Hay que discutir hasta alcanzar un acuerdo.

---

# 3. Fibonacci

La escala que utiliza la cátedra es:

**1 → 2 → 3 → 5 → 8 → 13 → 20 → 40 → 100**

No se inventan valores intermedios como:

❌ 4
❌ 6
❌ 7
❌ 10

Son valores discretos.

---

# 4. ¿Por qué Fibonacci?

Porque a medida que aumenta el tamaño de la historia también aumenta la incertidumbre.

Por eso las diferencias entre números se hacen mayores.

Por ejemplo:

**3 → 5 → 8 → 13**

La diferencia no pretende representar exactamente una cantidad de horas.

Representa una **magnitud relativa**.

---

# 5. ¿Qué significa 13?

Esta fue una de las advertencias más importantes.

Si una User Story da:

> **13 puntos**

hay que preguntarse:

> "¿Realmente es una User Story o debería dividirse?"

Porque probablemente sea demasiado grande para trabajar cómodamente dentro de un Sprint.

---

# 6. Incluso un 8 puede ser riesgoso

El profesor dijo algo interesante:

> Incluso una User Story de **8** se intenta evitar dentro de un Sprint.

¿Por qué?

Porque si no se termina:

**mucho valor de negocio queda sin entregar.**

Por eso:

### 13

🚨 Revisar seriamente si se puede dividir.

### 8

⚠️ También genera riesgo.

### 5 o menos

Generalmente es más manejable.

---

# 7. No hablar de "tareas grandes"

El profesor corrigió una expresión.

No necesariamente hay que decir:

> "Tarea de 20."

Es mejor hablar de:

> **Ítem del Product Backlog**

porque pueden existir ítems grandes de:

* 20
* 40
* 100

que después deberán subdividirse.

---

# 8. User Story Canónica

Este concepto es **MUY importante para el parcial**.

La User Story canónica funciona como:

> 🪜 **metro patrón**

Es la referencia que utilizamos para comparar las demás historias.

Por ejemplo:

> Registrar usuario por email = 2 puntos

Entonces:

> Enviar prendas = 5 puntos

significa que enviar prendas se considera significativamente más grande que la canónica.

---

# 9. ¿Cómo elegir la canónica?

Buscar una User Story:

* sencilla,
* conocida,
* de baja complejidad,
* con poco esfuerzo,
* con poca incertidumbre,
* sin integraciones complicadas,
* sin manejo complejo de sesiones.

### Buenas candidatas

Por ejemplo:

* alta sencilla;
* consulta sencilla;
* registro sencillo.

---

# 10. ¿Qué NO conviene elegir como canónica?

El profesor dio varios ejemplos.

### ❌ Inicio de sesión

Puede parecer sencillo:

> usuario + contraseña

Pero detrás puede haber:

* manejo de sesión,
* seguridad,
* persistencia de sesión,
* autenticación.

Por eso puede ser más complejo de lo que parece.

### ❌ Integración con Google

Tiene una integración externa.

### ❌ QR si no sabemos cómo implementarlo

Tiene incertidumbre.

### ❌ Integraciones externas

En general no son buenas candidatas para ser el metro patrón.

---

# 11. La canónica NO tiene que estar obligatoriamente en el MVP

Esto es importante.

La canónica se elige principalmente para:

> **tener una referencia para estimar.**

No significa:

> "Como es canónica, obligatoriamente pertenece al MVP."

Puede pertenecer al MVP o no.

---

# 12. Pero tampoco hay una regla absoluta

Si una User Story del MVP es:

> "Registrar producto"

y es extremadamente sencilla y conocida,

perfectamente puede ser la canónica.

Lo importante es:

> **justificar la elección.**

---

# 13. Las tres variables de la estimación

El profesor repite varias veces estas tres:

## ① Complejidad

¿Qué tan complicada es la solución?

Ejemplo:

> Calcular automáticamente un precio considerando varios factores.

Puede tener mayor complejidad.

---

## ② Esfuerzo

¿Cuánto trabajo requiere?

Ejemplo:

Una historia que requiere:

* muchas validaciones,
* varias pantallas,
* pruebas,
* emails,
* procesamiento de archivos,

requiere más esfuerzo.

---

## ③ Incertidumbre

¿Qué cosas todavía no sabemos?

Este punto es **MUY importante**.

Ejemplo:

> "No sabemos cómo vamos a implementar el lector QR."

Eso genera incertidumbre.

---

# 14. La incertidumbre puede aumentar mucho la estimación

Esto fue una pregunta específica de un alumno.

Supongamos:

> "No sé cómo implementar QR."

No significa necesariamente que QR sea extremadamente complejo.

Puede ser que:

> **simplemente no sepamos todavía cómo hacerlo.**

Entonces aumenta la **incertidumbre**.

Y esa incertidumbre puede justificar un:

**5 u 8**, por ejemplo.

---

# 15. ¿Y si después descubrimos que era fácil?

No importa.

La estimación inicial se hace con:

> **el conocimiento disponible en ese momento.**

Si después investigamos y descubrimos que era sencillo, podemos:

> **reestimar.**

Por eso existe el proceso iterativo.

---

# 16. ¿Cuándo podría aparecer un 13?

Cuando la incertidumbre es muy grande o la historia es demasiado grande.

Por ejemplo:

> "No tenemos idea de cómo implementar esta tecnología."

Puede justificar una estimación alta.

Pero también puede significar:

> 🔎 necesitamos un **Spike**.

---

# 17. Spike

Esto aparece relacionado con lo que trabajaron en la clase.

Un **Spike** es trabajo de investigación para reducir incertidumbre.

Ejemplo:

> "Necesitamos saber qué capacidad de servidor necesitamos antes de poder estimar correctamente la implementación."

Entonces hacemos una investigación.

El objetivo es:

> **obtener conocimiento para poder estimar o desarrollar posteriormente.**

No es simplemente "hacer una tarea".

---

# 18. User Story y MVP

En el ejercicio de **Recircula prendas** trabajaron sobre un MVP.

El proceso fue:

**Hipótesis → criterio → alcance del MVP → User Stories**

---

# 19. Hipótesis del MVP

La hipótesis identificada fue:

> **Existen personas dispuestas a comprar y vender prendas usadas.**

Esa es la suposición de negocio que se quiere validar.

---

# 20. ¿Qué NO entra en el MVP?

El profesor marcó varias cosas.

### ❌ E-commerce completo

Se utiliza temporalmente:

> Tienda Nube.

¿Por qué?

Porque primero se quiere validar el modelo de negocio.

No tiene sentido desarrollar todo el e-commerce antes de saber si el negocio funciona.

---

### ❌ Registro con Google

Se decidió utilizar:

> registro mediante email.

Google queda fuera.

---

### ❌ WhatsApp

Aunque el enunciado lo menciona:

> queda fuera del MVP.

Se utilizan emails.

---

### ❌ ABM completo

No se desarrolla toda una gestión de:

* altas,
* bajas,
* modificaciones.

Algunas cosas se manejan directamente desde la base de datos.

---

### ❌ Liquidación para administrador

Queda fuera.

---

# 21. MVP debe cerrar de punta a punta

Este fue un concepto MUY bueno del profesor.

Aunque una parte no sea software, el MVP debe tener sentido completo.

Ejemplo:

El sistema vende una prenda.

Entonces alguien debe:

* enterarse de que se vendió;
* recibir el dinero;
* saber qué pasó con la prenda.

Aunque el pago sea manual, el proceso de negocio tiene que cerrar.

---

# 22. Emails

Los emails sí tienen valor dentro del MVP.

Por ejemplo:

Cuando se genera una propuesta:

📧 se informa al vendedor.

Cuando se confirma:

📧 se puede notificar.

Cuando se vende una prenda:

📧 el vendedor debe enterarse.

El profesor incluso dijo que:

> automatizar el envío del mail agrega valor.

---

# 23. User Story — sintaxis

El profesor fue bastante estricto con esto.

La estructura:

> **Como [rol] quiero [acción]**

Ejemplo:

> Como vendedor quiero enviar prendas.

⚠️ La frase verbal debe ser **corta**.

No meter toda la explicación ahí.

---

# 24. No llenar el "Quiero" de detalles

Incorrecto como práctica:

> Como vendedor quiero enviar las prendas especificando categorías, cantidades, sucursal, fotos, etc.

Mejor:

> **Como vendedor quiero enviar prendas.**

Los detalles van en:

* valor de negocio;
* criterios de aceptación;
* reglas;
* etc.

---

# 25. Valor de negocio

Ahí sí se puede explicar un poco más.

El profesor dijo aproximadamente:

> No más de dos líneas.

Debe explicar:

> **¿Qué valor obtiene el negocio/usuario?**

---

# 26. Criterios de aceptación

Los criterios indican:

> **qué debe cumplirse para considerar que la User Story funciona correctamente.**

Ejemplo de la clase:

El vendedor:

* debe indicar cantidades;
* debe indicar categorías;
* debe completar la información requerida;
* debe enviar mínimo 10 prendas;
* puede subir foto;
* la foto tiene límite de tamaño;
* se envía email.

---

# 27. Reglas de negocio dentro de los criterios

Ejemplo:

> Mínimo 10 prendas.

Eso es una regla de negocio.

No es simplemente una decisión técnica.

---

# 28. Fotos

En la User Story de enviar prendas:

La foto era:

> **opcional**

pero tenía una restricción:

> máximo **512 KB**.

Esto debía aparecer en los criterios de aceptación.

---

# 29. Otra User Story: completar ficha

Para la ficha de publicación aparecían:

* nombre de prenda;
* peso;
* precio sugerido;
* atributos dinámicos;
* fotos;
* QR;
* previsualización.

---

# 30. Precio sugerido

Este punto es importante.

El precio:

> **se calcula automáticamente**

considerando:

* categoría;
* marca;
* estacionalidad;
* estado.

Después:

> **el precio puede editarse.**

---

# 31. No confundir "calcular" con "ingresar"

El precio sugerido:

❌ no es simplemente otro campo que el usuario escribe.

Primero:

**Sistema → calcula precio**

Después:

**Usuario → puede editarlo**

---

# 32. Incertidumbre del precio

También puede existir incertidumbre porque no necesariamente se sabe:

* cuánto pesa cada factor;
* qué marca vale más;
* qué categoría vale menos;
* qué precio corresponde a cada condición.

Por lo tanto:

> **precio sugerido = complejidad + posible incertidumbre.**

---

# 33. QR

El QR también agrega elementos a considerar:

* escanear QR;
* saber cómo implementarlo;
* posible incertidumbre tecnológica.

⚠️ Pero:

> **generar QR y escanear QR son cosas distintas.**

En esta User Story se hablaba de:

> **escanear el QR.**

---

# 34. Subida de imágenes

También puede generar complejidad.

Hay que pensar:

* dónde se almacenan;
* límite de tamaño;
* cantidad máxima;
* procesamiento;
* repositorio/almacenamiento.

Por eso no es simplemente:

> "subir foto".

---

# 35. Previsualización

La ficha debe poder:

> **previsualizarse como la verá el cliente.**

Esto también forma parte de la User Story.

---

# 36. Pruebas de aceptación

El profesor dio una regla concreta:

Las pruebas deberían comenzar con:

> **Probar + acción**

Ejemplos de la clase:

> Probar enviar prendas.

> Probar confirmar propuesta de venta.

> Probar completar ficha de prenda.

---

# 37. No son pruebas exhaustivas del sistema

⚠️ MUY IMPORTANTE.

El profesor aclaró:

> Son **pruebas de aceptación de usuario**.

No son:

> pruebas completas del sistema.

El Product Owner debería poder sentarse y validar rápidamente:

> "Sí, esto cumple."

---

# 38. No hace falta probar cada campo individualmente

Pregunta de un alumno:

Si tengo:

* nombre,
* peso,
* categoría,
* marca,
* etc.

¿Tengo que hacer una prueba de error por cada uno?

Respuesta:

**No necesariamente.**

Si las validaciones son equivalentes:

> se puede probar un campo representativo.

Pero hay que analizar si algún campo tiene:

* una regla diferente;
* un valor de negocio especial;
* una validación distinta.

---

# 39. Ejemplo

Si todos estos campos son obligatorios:

* nombre;
* peso;
* marca;
* categoría.

Podrías probar:

> **Probar completar la ficha sin ingresar un campo obligatorio.**

No necesariamente:

❌ una prueba para nombre
❌ otra para peso
❌ otra para marca
❌ otra para categoría

salvo que exista una razón particular.

---

# 40. CBU

En la clase discutieron el CBU.

El profesor aclaró:

La User Story de **enviar prendas** no debería encargarse de validar el CBU.

El CBU pertenece al:

> **registro del usuario/vendedor.**

Además:

❌ No hace falta integrar una API externa para comprobar que el CBU realmente pertenece a una persona.

Pero:

✅ sí pueden existir validaciones básicas del formato.

Por ejemplo:

> algoritmo/formato del CBU.

---

# 41. Diferencia entre "registrado" y "no registrado"

En este ejercicio se asumió:

**Primero me registro → después puedo realizar el resto de operaciones.**

Por eso no necesariamente hay que repetir:

> "El vendedor debe estar registrado"

en absolutamente todas las User Stories.

---

# 42. Comparación con EcoHarmony Park

El profesor utilizó otro ejemplo para explicar esto.

Si una aplicación permite:

* navegar sin registrarse;
* elegir entrada;
* y recién exige registro al pagar,

entonces sí tiene sentido indicar:

> usuario no registrado
> usuario registrado

como escenarios distintos.

Pero en Recircula:

> primero sos vendedor registrado → después realizás el proceso.

---

# 43. Confirmar propuesta de venta

Esta User Story tiene bastante contenido.

El vendedor puede recibir una propuesta y decidir qué hacer.

Para las prendas **seleccionadas**:

* vender;
* retirar.

Para las prendas **no seleccionadas**:

* retirar;
* donar.

---

# 44. No confundir "estado" de la prenda

El profesor hizo una aclaración importante.

"Seleccionada/no seleccionada" no necesariamente es el **estado de la prenda**.

El estado puede referirse a algo propio del dominio, por ejemplo:

* nueva;
* usada;
* etc.

Mientras que:

> seleccionada / no seleccionada

describe otra característica del proceso.

---

# 45. No todas las prendas tienen las mismas opciones

### Prenda seleccionada

Puede:

* venderse;
* retirarse.

### Prenda no seleccionada

Puede:

* retirarse;
* donarse.

No tiene sentido:

> vender una prenda que el negocio ya rechazó.

---

# 46. El usuario puede decidir parcialmente

En la propuesta:

No necesariamente tiene que aceptar todas.

Puede:

* aceptar algunas;
* rechazar algunas;
* aceptar todas;
* no aceptar ninguna.

Esto debe quedar claro en los criterios.

---

# 47. Confirmación de propuesta

No pensar:

> "Es solamente un botón."

Porque detrás puede haber:

* consulta de información;
* selección de prendas;
* decisiones;
* actualización de datos;
* emails;
* estados/resultados.

Por eso el profesor consideró que podía estar más cerca de:

> **5**

que de:

> **3**

dependiendo de la comparación con la canónica.

---

# 48. La comparación es lo más importante

No preguntes solamente:

> "¿Esta historia parece un 5?"

Preguntate:

> **"¿Es más o menos grande que mi canónica?"**

Ese es el corazón de la estimación relativa.

---

# 49. Ser consistente

El profesor dio una regla fundamental para el parcial:

> **Sean consistentes consigo mismos.**

Ejemplo:

Canónica:

**Registrar usuario = 2**

Entonces:

Enviar prendas = **5**

Completar ficha = **8**

Tiene que existir una lógica de comparación.

No vale:

> "A esta le puse 3 porque me pareció."

Tenés que poder explicar:

> "Es mayor que la canónica porque tiene X, Y y Z."

---

# 50. No usar 4, 6, 7...

El profesor lo remarcó directamente.

Si la escala es Fibonacci:

**1, 2, 3, 5, 8, 13...**

No:

❌ 4
❌ 6
❌ 7

---

# 51. Si algo es más de 3 veces la canónica

El profesor dijo algo muy importante:

> Si algo cuesta más del triple, ya debería saltar a un valor mayor.

Por eso hay que evitar incoherencias.

Ejemplo conceptual:

Canónica = 2

Una historia muchísimo mayor no debería terminar siendo:

> 3

si claramente tiene mucha más complejidad.

---

# 52. Si una historia tiene complejidad + incertidumbre

Probablemente no corresponda un valor bajo.

Por ejemplo:

* QR desconocido;
* cálculo de precio;
* almacenamiento de imágenes.

Hay varias cosas que investigar.

Por eso:

> **3 probablemente sería demasiado bajo.**

Podría estar entre:

> **5 y 8**

dependiendo de la justificación.

---

# 53. Justificar la estimación

Para el parcial, no alcanza con:

> "Le puse 5."

Hay que explicar:

### Complejidad

¿Qué cosas son técnicamente complejas?

### Esfuerzo

¿Qué cantidad de trabajo requiere?

### Incertidumbre

¿Qué cosas todavía no conocemos?

---

# 54. Ejemplo de justificación

Una historia de "Enviar prendas" podría tener:

### Complejidad

* validaciones;
* mínimo de 10 prendas;
* fotografías;
* email.

### Esfuerzo

* formulario;
* validaciones;
* procesamiento;
* pruebas.

### Incertidumbre

* envío de emails;
* manejo de archivos;
* detalles de implementación.

Por eso podría justificarse:

> **5 puntos.**

---

# 55. Una historia con QR

Podría tener:

### Complejidad

Integración del lector QR.

### Esfuerzo

Implementar y probar el escaneo.

### Incertidumbre

No sabemos todavía qué tecnología/librería utilizar.

Entonces:

> puede aumentar la estimación.

---

# 56. Pero incertidumbre ≠ complejidad

Esto también apareció en la clase.

No saber cómo hacer algo:

❌ no significa automáticamente que sea muy complejo.

Puede significar:

> **no sabemos todavía qué tan complejo es.**

Eso es incertidumbre.

---

# 57. Una User Story demasiado grande

Si termina en:

> **13**

hay que preguntarse:

> ¿La puedo dividir?

Si no puedo terminarla dentro del Sprint:

> hay riesgo de perder valor de negocio.

---

# 58. INVEST

Al principio de la clase el profesor menciona que una historia debe estar lista y cumplir:

> **INVEST**

Aunque en esta clase no desarrolla todas las letras.

Para el parcial conviene recordar:

| Letra | Idea        |
| ----- | ----------- |
| **I** | Independent |
| **N** | Negotiable  |
| **V** | Valuable    |
| **E** | Estimable   |
| **S** | Small       |
| **T** | Testable    |

---

# 59. Qué estudiar SÍ O SÍ para el parcial

Yo marcaría estos como 🔥:

### 🔥 1. User Story

Saber escribir:

> Como [rol] quiero [acción] para [valor].

### 🔥 2. Criterios de aceptación

Saber identificar qué debe cumplirse.

### 🔥 3. Pruebas de aceptación

Recordar:

> **Probar + acción**

### 🔥 4. MVP

Entender:

**hipótesis → criterio → alcance**

### 🔥 5. User Story canónica

Entender:

> **metro patrón.**

### 🔥 6. Poker Estimation

Memorizar:

**votar → revelar → alto/bajo explican → discutir → volver a votar → repetir → acuerdo**

### 🔥 7. Fibonacci

**1, 2, 3, 5, 8, 13, 20, 40, 100**

### 🔥 8. Tres variables

**Complejidad + Esfuerzo + Incertidumbre**

### 🔥 9. Relatividad

No estimar "en horas".

Comparar contra la canónica.

### 🔥 10. 13 puntos

Preguntarse:

> **¿hay que dividir la historia?**

### 🔥 11. Justificación

Siempre explicar **por qué**.

### 🔥 12. No promediar

El equipo debe **llegar a un acuerdo**.

---

# 🧠 La frase para memorizar toda la clase

Si mañana te preguntan **"¿cómo se estima una User Story?"**, pensá:

> **Elijo una canónica como metro patrón → analizo complejidad, esfuerzo e incertidumbre → cada integrante vota con Fibonacci → se revelan las cartas → los valores más alto y más bajo justifican → se debate → se vuelve a votar → se repite hasta llegar a un acuerdo.**

Y si te preguntan:

**"¿Qué pasa si da 13?"**

> **Reviso si la User Story puede dividirse porque es demasiado grande/riesgosa para un Sprint.**

Y si te preguntan:

**"¿Qué es una canónica?"**

> **Es la User Story elegida como referencia o metro patrón para realizar estimaciones relativas.**
