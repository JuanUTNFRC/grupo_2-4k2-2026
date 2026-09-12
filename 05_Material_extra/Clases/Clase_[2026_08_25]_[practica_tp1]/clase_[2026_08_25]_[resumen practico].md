Sí. Esta transcripción corresponde a una clase **muy importante sobre User Stories, INVEST, Definition of Ready, criterios de aceptación, pruebas, Spikes y división vertical**.

Te la puedo ordenar para estudiar. Lo más importante que dijo el profesor es esto:

### La idea central de toda la clase

Una **User Story** no es una especificación técnica completa.

Sirve para expresar:

> **Quién** quiere hacer **qué**, y **para qué le sirve**.

La estructura es:

**Como [rol], quiero [acción], para [valor de negocio].**

Ejemplo de la clase:

> Como cliente, quiero **pagar un pedido en efectivo**, para **adquirir los productos que seleccioné**.

El profesor insiste muchísimo en el **valor de negocio**. Si no podés explicar qué valor obtiene el usuario, probablemente esa historia está mal planteada.

---

## 1. Las 3 partes de una User Story

El profesor habla de la famosa **tarjeta + conversación + confirmación**:

| Parte            | Qué significa                                                     |
| ---------------- | ----------------------------------------------------------------- |
| **Tarjeta**      | La User Story escrita brevemente                                  |
| **Conversación** | Lo que se habla para aclarar el requerimiento                     |
| **Confirmación** | Los criterios de aceptación que permiten comprobar que se cumplió |

Por eso:

**User Story ≠ especificación completa.**

La historia identifica la necesidad, pero después se conversa y se define cómo vamos a saber que está correctamente realizada.

---

# 2. INVEST

Esta es probablemente una de las partes que más te pueden preguntar.

Una User Story debería cumplir **INVEST**:

| Letra | Concepto    | Significado             |
| ----- | ----------- | ----------------------- |
| **I** | Independent | Independiente           |
| **N** | Negotiable  | Negociable              |
| **V** | Valuable    | Valiosa                 |
| **E** | Estimable   | Estimable               |
| **S** | Small       | Pequeña                 |
| **T** | Testable    | Verificable / testeable |

### I — Independent

La historia debería poder desarrollarse **sin depender de otra historia dentro del mismo Sprint**.

Ejemplo:

Si una historia necesita obligatoriamente que otra historia termine primero, tenemos una dependencia.

El profesor menciona el concepto de **mock**:

> Si todavía no existe un servicio que necesito, puedo simularlo para poder desarrollar y probar mi historia.

---

### N — Negotiable

La historia **no es un contrato cerrado**.

Se puede conversar y negociar con el Product Owner.

Por ejemplo:

Tenemos:

* Historia A → valor 8
* Historia B → valor 5
* Historia C → valor 3

Si el Sprint tiene capacidad para 8 puntos, se puede conversar qué entra primero.

El **valor de negocio** ayuda justamente a negociar prioridades.

---

### V — Valuable

Tiene que aportar **valor de negocio**.

Esta es una de las cosas que el profesor más repite.

No:

> "Como usuario quiero desarrollar la base de datos..."

Eso es técnico.

Mejor:

> "Como cliente quiero consultar mis gastos para poder controlar mis finanzas."

El cliente recibe un beneficio.

---

### E — Estimable

Tenemos que tener suficiente información para poder estimar cuánto esfuerzo implica.

Si todavía no sabemos cómo resolver algo técnicamente, puede aparecer un:

### Spike

Un **Spike** es una actividad de investigación técnica.

Ejemplo de la clase:

> "¿Cómo me conecto a la API para validar la condición fiscal de un cliente?"

Primero hago un Spike:

1. Investigo.
2. Pruebo.
3. Documento.
4. Determino cómo hacerlo.
5. Después puedo desarrollar la User Story.

El Spike puede estar en un Sprint anterior y la User Story en el siguiente.

---

### S — Small

Tiene que ser suficientemente pequeña como para poder **comenzarla y terminarla dentro de un Sprint**.

Si es demasiado grande:

**Épica → dividir → User Stories**

Por ejemplo:

**Gestión de pagos**

puede ser una épica.

Se divide en:

* Registrar pago.
* Pagar en efectivo.
* Pagar con tarjeta.
* etc.

---

### T — Testable

Tengo que poder comprobar objetivamente si la historia se cumplió.

Ahí aparecen los:

### Criterios de aceptación

Por ejemplo:

> El pedido debe poder pagarse con una única forma de pago.

Después puedo crear pruebas para comprobarlo.

---

# 3. Definition of Ready

Esta parte también es importante.

El profesor dice que una historia tiene que cumplir determinadas condiciones para poder entrar al **Sprint Backlog**.

Eso se conoce como:

### Definition of Ready — DoR

En términos simples:

> **¿La User Story está suficientemente preparada como para que el equipo pueda empezar a trabajarla?**

Tiene que cumplir, como mínimo, las condiciones que el equipo haya definido.

Por ejemplo:

* Tiene valor de negocio.
* Es entendible.
* Se puede negociar.
* Se puede estimar.
* Es suficientemente pequeña.
* Se puede probar.
* No tiene dependencias bloqueantes.

---

# 4. Definition of Done

No confundir:

### Ready

**¿Podemos empezar a trabajarla?**

### Done

**¿Está realmente terminada y entregable?**

El profesor menciona ejemplos de condiciones de Done:

* Pasaron las pruebas.
* Se realizaron pruebas unitarias.
* Se alcanzó determinada cobertura.
* Se documentó lo necesario.
* Se completó la arquitectura/diseño correspondiente.
* Cumple los criterios establecidos por el equipo.

Entonces:

**DoR → antes de empezar**

**DoD → antes de decir que terminó**

---

# 5. Product Backlog vs Sprint Backlog

Esto también aparece en la clase.

### Product Backlog

Es la lista general de trabajo del producto.

Puede contener:

* User Stories
* Épicas
* Spikes
* etc.

### Sprint Backlog

Es solamente lo que se selecciona para trabajar durante **ese Sprint**.

Podés imaginar:

```text
PRODUCT BACKLOG
│
├── Épica
├── User Story
├── User Story
├── Spike
├── User Story
├── Épica
└── User Story
       ↓
   Selección
       ↓
SPRINT BACKLOG
├── User Story
├── User Story
└── Spike
```

---

# 6. División vertical vs horizontal

Esta es **muy importante** porque el profesor la repite varias veces.

### ❌ División horizontal

Separar por capas técnicas:

```text
Sprint 1 → Base de datos
Sprint 2 → Backend
Sprint 3 → Frontend
Sprint 4 → Seguridad
```

El problema:

al terminar el Sprint 1, el cliente no recibe algo que le aporte valor.

---

### ✅ División vertical

Cada historia atraviesa las capas necesarias y entrega **un pequeño incremento de valor**.

Ejemplo del e-commerce:

```text
Épica: Comprar productos

        ↓

Historia 1
Visualizar productos

        ↓

Historia 2
Armar carrito

        ↓

Historia 3
Registrar domicilio

        ↓

Historia 4
Pagar en efectivo

        ↓

Historia 5
Pagar con tarjeta
```

Cada una puede producir algo útil.

Eso es una **porción vertical** del producto.

---

# 7. Criterios de aceptación

Son las condiciones que tienen que cumplirse para considerar que la User Story funciona según lo acordado.

Ejemplo de la clase:

### User Story

> Como cliente, quiero pagar un pedido en efectivo para adquirir los productos seleccionados.

Criterios podrían ser:

* Debe existir stock de los productos.
* Debe aplicarse el descuento correspondiente.
* El pedido debe tener domicilio de entrega.
* El pedido debe tener una única forma de pago.
* Debe registrarse correctamente el pago.

---

# 8. Pruebas

El profesor explica algo interesante:

Las pruebas no son simplemente:

> "Probar todo."

Se escriben pensando en **qué quiero verificar**.

Por ejemplo:

> **Probar la confirmación de un pedido pagando en efectivo.**

También puede haber escenarios negativos:

> **Probar que no se permita combinar dos formas de pago.**

Entonces:

### Criterio de aceptación

> Un pedido solo puede utilizar una forma de pago.

### Prueba

> Probar que no sea posible combinar dos formas de pago.

---

# 9. El ejemplo de Gestión de Gastos

El profesor termina aplicando todo esto a un ejercicio.

Algunas User Stories que aparecen son:

* Registrar gasto.
* Registrar tipo de gasto.
* Registrar responsable del gasto.
* Visualizar planilla de gastos.
* Filtrar gastos.
* Ordenar gastos.
* Modificar fecha del gasto.
* Modificar gasto.
* etc.

Y aparece una discusión importante:

### ¿Visualizar gastos y filtrar gastos son la misma historia?

No necesariamente.

Podemos tener:

**Historia 1:**

> Como usuario, quiero visualizar mis gastos para llevar un registro de ellos.

Y posteriormente:

**Historia 2:**

> Como usuario, quiero filtrar y ordenar mis gastos para poder analizarlos según distintos criterios.

¿Por qué separarlas?

Porque la primera ya tiene **valor de negocio** por sí sola.

No necesito esperar a tener filtros para entregar una primera versión útil.

---

#
Si el profesor te pregunta:

### "¿Qué es una User Story?"

Podés responder:

> Es una descripción breve de una necesidad desde la perspectiva de un usuario, expresada mediante un rol, una acción y un valor de negocio.

### "¿Qué es INVEST?"

> Es un conjunto de características que debería cumplir una User Story: Independent, Negotiable, Valuable, Estimable, Small y Testable.

### "¿Qué es un Spike?"

> Es una actividad de investigación que permite obtener información o conocimiento necesario para poder estimar o desarrollar posteriormente una User Story.

### "¿Qué diferencia hay entre Definition of Ready y Definition of Done?"

> **Ready** determina cuándo una User Story está suficientemente preparada para comenzar a trabajarse. **Done** determina cuándo el trabajo realizado cumple todas las condiciones necesarias para considerarse terminado y entregable.

### "¿Qué significa dividir verticalmente?"

> Dividir una funcionalidad en pequeñas User Stories que atraviesan las capas necesarias y entregan valor de negocio en cada incremento, en lugar de separar el trabajo por capas técnicas.

### Y esta frase es CLAVE:

> **No divido una User Story porque sí; la divido de manera que cada parte siga teniendo valor de negocio.**

Esa es prácticamente **la idea central de toda esta clase**.
