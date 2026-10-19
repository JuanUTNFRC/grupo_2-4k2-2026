// Página de reserva: toda la lógica de negocio vive en la API; este script
// arma los pasos, mantiene el resumen del pase y muestra lo que responde la API.

const $ = (id) => document.getElementById(id);

const POCOS_LUGARES = 3;
const DIAS_VISIBLES = 7;

const ICONOS = {
  tirolesa: '<path d="M3 6l18 6"/><path d="M12 9v4"/><circle cx="12" cy="15" r="2"/><path d="M10 21l2-4 2 4"/>',
  safari: '<circle cx="7" cy="15" r="4"/><circle cx="17" cy="15" r="4"/><path d="M11 15h2M5 11l2-6h3l1 6M19 11l-2-6h-3l-1 6"/>',
  palestra: '<path d="M3 21l6-10 4 6 3-4 5 8z"/><circle cx="9" cy="6" r="1.5"/><circle cx="16" cy="8" r="1.5"/>',
  jardineria: '<path d="M12 21v-8"/><path d="M12 13c0-4 3-6 7-6 0 4-3 6-7 6z"/><path d="M12 15c0-3-2-5-6-5 0 3 2 5 6 5z"/>',
  otra: '<path d="M12 3c5 4 7 8 7 12a7 7 0 0 1-14 0c0-4 2-8 7-12z"/>',
};

const estado = {
  actividades: [],
  actividad: null,
  horarios: [],
  horario: null,
};

// ---------- Utilidades ----------

function leerCookie(nombre) {
  const valor = document.cookie.split('; ').find((cookie) => cookie.startsWith(`${nombre}=`));
  return valor ? decodeURIComponent(valor.split('=')[1]) : '';
}

async function api(url, opciones = {}) {
  try {
    const respuesta = await fetch(url, {
      credentials: 'same-origin',
      ...opciones,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        // SessionAuthentication exige el token CSRF en los POST.
        'X-CSRFToken': leerCookie('csrftoken'),
        ...opciones.headers,
      },
    });
    return { ok: respuesta.ok, datos: await respuesta.json() };
  } catch {
    return {
      ok: false,
      datos: { detalle: 'No pudimos conectar con el parque. Revisá tu conexión e intentá de nuevo.' },
    };
  }
}

function claveActividad(nombre) {
  return nombre.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
}

// "2026-10-13" -> Date local, sin corrimientos por zona horaria.
function aFecha(texto) {
  const [anio, mes, dia] = texto.split('-').map(Number);
  return new Date(anio, mes - 1, dia);
}

const formatoDiaLargo = new Intl.DateTimeFormat('es-AR', { weekday: 'long', day: 'numeric', month: 'long' });
const formatoDiaCorto = new Intl.DateTimeFormat('es-AR', { weekday: 'short' });
const formatoNumeroMes = new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'short' });

function lugares(cantidad) {
  return cantidad === 1 ? '1 lugar' : `${cantidad} lugares`;
}

function crear(etiqueta, clase, texto) {
  const elemento = document.createElement(etiqueta);
  if (clase) elemento.className = clase;
  if (texto !== undefined) elemento.textContent = texto;
  return elemento;
}

// Radio nativo dentro de una etiqueta: teclado, foco y lectores de pantalla gratis.
function opcion(nombre, valor, contenido) {
  const etiqueta = crear('label', 'opcion');
  const radio = document.createElement('input');
  radio.type = 'radio';
  radio.name = nombre;
  radio.value = valor;
  etiqueta.append(radio, contenido);
  return etiqueta;
}

// ---------- Paso 1: actividad ----------

async function cargarActividades() {
  const contenedor = $('actividades');
  const { ok, datos } = await api('/api/actividades/');
  contenedor.removeAttribute('aria-busy');
  if (!ok) {
    contenedor.replaceChildren(crear('p', 'aviso aviso--error', datos.detalle));
    return;
  }
  estado.actividades = datos;
  contenedor.replaceChildren(
    ...datos.map((actividad) => {
      const tarjeta = crear('span', 'actividad');
      const icono = ICONOS[claveActividad(actividad.nombre)] || ICONOS.otra;
      tarjeta.innerHTML = `<svg class="actividad__icono" viewBox="0 0 24 24" aria-hidden="true">${icono}</svg>`;
      tarjeta.append(
        crear('span', 'actividad__nombre', actividad.nombre),
        crear('span', 'etiqueta', actividad.requiere_talle ? 'Pide talle' : 'Sin talle'),
      );
      return opcion('actividad', actividad.id, tarjeta);
    }),
  );
}

async function elegirActividad(id) {
  estado.actividad = estado.actividades.find((actividad) => actividad.id === id) || null;
  estado.horario = null;
  $('terminos-texto').textContent = estado.actividad.terminos_condiciones;
  $('acepta-terminos').checked = false;
  $('dias').replaceChildren();
  $('turnos').replaceChildren();
  $('paso-horario').disabled = false;
  $('horario-ayuda').textContent = 'Buscando horarios con lugar…';
  actualizar();

  const { ok, datos } = await api(`/api/horarios-disponibles/?actividad_id=${id}`);
  if (!ok) {
    $('horario-ayuda').textContent = datos.detalle;
    return;
  }
  estado.horarios = datos;
  dibujarDias();
}

// ---------- Paso 2: día y horario ----------

function dibujarDias() {
  const porDia = Map.groupBy(estado.horarios, (horario) => horario.fecha);
  if (porDia.size === 0) {
    $('horario-ayuda').textContent = 'Esta actividad no tiene horarios con lugar en los próximos días. Probá con otra.';
    return;
  }
  $('horario-ayuda').textContent = 'Los horarios muestran los lugares que quedan.';
  const dias = [...porDia.keys()].map((fecha) => {
    const dia = aFecha(fecha);
    const chip = crear('span', 'chip');
    chip.append(
      crear('span', 'chip__dia', formatoDiaCorto.format(dia).replace('.', '')),
      crear('span', 'chip__principal', formatoNumeroMes.format(dia).replace('.', '')),
    );
    return opcion('dia', fecha, chip);
  });
  // Primero la semana que viene; el resto, a pedido.
  dias.slice(DIAS_VISIBLES).forEach((dia) => { dia.hidden = true; });
  $('dias').replaceChildren(...dias);
  if (dias.length > DIAS_VISIBLES) {
    const boton = crear('button', 'mas-dias', `Ver ${dias.length - DIAS_VISIBLES} días más`);
    boton.type = 'button';
    boton.addEventListener('click', () => {
      dias.forEach((dia) => { dia.hidden = false; });
      boton.remove();
      dias[DIAS_VISIBLES].querySelector('input').focus();
    });
    $('dias').append(boton);
  }
  const primero = $('dias').querySelector('input');
  primero.checked = true;
  dibujarTurnos(primero.value);
}

function dibujarTurnos(fecha) {
  estado.horario = null;
  $('turnos').replaceChildren(
    ...estado.horarios
      .filter((horario) => horario.fecha === fecha)
      .map((horario) => {
        const pocos = horario.cupo_disponible <= POCOS_LUGARES;
        const chip = crear('span', 'chip');
        chip.append(
          crear('span', 'chip__principal', horario.hora_inicio),
          crear(
            'span',
            pocos ? 'chip__detalle chip__detalle--pocos' : 'chip__detalle',
            pocos ? `Quedan ${lugares(horario.cupo_disponible)}` : lugares(horario.cupo_disponible),
          ),
        );
        return opcion('horario', horario.id, chip);
      }),
  );
  actualizar();
}

function elegirHorario(id) {
  estado.horario = estado.horarios.find((horario) => horario.id === id) || null;
  const maximo = estado.horario.cupo_disponible;
  $('cantidad').max = maximo;
  $('cantidad').value = Math.min(Number($('cantidad').value) || 1, maximo);
  $('cupo-ayuda').textContent = `En este horario quedan ${lugares(maximo)}.`;
  $('paso-personas').disabled = false;
  $('paso-terminos').disabled = false;
  dibujarParticipantes();
}

// ---------- Paso 3: personas ----------

function cantidad() {
  const maximo = estado.horario ? estado.horario.cupo_disponible : 1;
  return Math.min(Math.max(1, Math.trunc(Number($('cantidad').value)) || 1), maximo);
}

function cambiarCantidad(delta) {
  $('cantidad').value = cantidad() + delta;
  $('cantidad').value = cantidad();
  dibujarParticipantes();
}

function dibujarParticipantes() {
  const contenedor = $('participantes');
  const total = estado.horario ? cantidad() : 0;
  const requiereTalle = Boolean(estado.actividad && estado.actividad.requiere_talle);

  // Conserva lo ya cargado al cambiar la cantidad.
  while (contenedor.children.length > total) contenedor.lastElementChild.remove();
  while (contenedor.children.length < total) {
    contenedor.append($('plantilla-participante').content.cloneNode(true));
  }
  [...contenedor.children].forEach((fieldset, indice) => {
    fieldset.querySelector('legend').textContent = `Persona ${indice + 1}`;
    fieldset.querySelector('.participante__campos').classList.toggle('sin-talle', !requiereTalle);
    fieldset.querySelector('.campo-talle').hidden = !requiereTalle;
    for (const campo of fieldset.querySelectorAll('[name]')) {
      campo.id = `persona-${indice}-${campo.name}`;
      campo.previousElementSibling.htmlFor = campo.id;
    }
  });
  $('menos').disabled = total <= 1;
  $('mas').disabled = !estado.horario || total >= estado.horario.cupo_disponible;
  actualizar();
}

function leerParticipantes() {
  return [...$('participantes').children].map((fieldset) => {
    const valor = (nombre) => fieldset.querySelector(`[name="${nombre}"]`).value.trim();
    return {
      nombre: valor('nombre'),
      dni: valor('dni'),
      edad: valor('edad'),
      talle: estado.actividad.requiere_talle ? valor('talle') : '',
    };
  });
}

// ---------- Resumen del pase y estado de los pasos ----------

function actualizar() {
  const participantes = estado.horario ? leerParticipantes() : [];
  const personasCompletas =
    participantes.length > 0 &&
    participantes.every((p) => p.nombre && p.dni && p.edad && (!estado.actividad.requiere_talle || p.talle));

  $('paso-actividad').classList.toggle('completo', Boolean(estado.actividad));
  $('paso-horario').classList.toggle('completo', Boolean(estado.horario));
  $('paso-personas').classList.toggle('completo', personasCompletas);
  $('paso-terminos').classList.toggle('completo', $('acepta-terminos').checked);

  $('resumen-actividad').textContent = estado.actividad ? estado.actividad.nombre : '—';
  $('resumen-dia').textContent = estado.horario ? formatoDiaLargo.format(aFecha(estado.horario.fecha)) : '—';
  $('resumen-hora').textContent = estado.horario ? `${estado.horario.hora_inicio} hs` : '—';
  $('resumen-personas').textContent = estado.horario ? String(participantes.length) : '—';

  $('confirmar').disabled = !estado.horario;
  $('confirmar-ayuda').textContent = estado.horario
    ? 'Revisá los datos antes de confirmar.'
    : 'Elegí actividad y horario para continuar.';
}

// ---------- Errores ----------

function mensajeDe(campo) {
  return campo.closest('.campo').querySelector('.campo__error');
}

function marcarCampo(campo, mensaje) {
  campo.setAttribute('aria-invalid', 'true');
  mensajeDe(campo).textContent = mensaje;
}

function desmarcarCampo(campo) {
  campo.removeAttribute('aria-invalid');
  mensajeDe(campo).textContent = '';
}

function limpiarErrores() {
  $('error-general').hidden = true;
  for (const campo of document.querySelectorAll('#form-reserva [aria-invalid]')) desmarcarCampo(campo);
}

// ---------- Validación en el navegador ----------
// Los mismos mensajes que devuelve la API: el usuario los ve antes de enviar,
// y la API los vuelve a validar igual.

const REGLAS = {
  nombre: (valor) => {
    if (!valor) return 'Ingresá el nombre y apellido.';
    if (valor.length > 100) return 'El nombre puede tener hasta 100 caracteres.';
    return '';
  },
  dni: (valor) => {
    if (!valor) return 'Ingresá el DNI.';
    if (!/^\d{7,8}$/.test(valor)) return 'El DNI tiene que tener 7 u 8 números, sin puntos.';
    return '';
  },
  edad: (valor) => {
    if (!valor) return 'Ingresá la edad.';
    if (!/^\d+$/.test(valor)) return 'Ingresá la edad en números.';
    if (Number(valor) < 1) return 'La edad tiene que ser mayor a 0.';
    if (Number(valor) > 130) return 'La edad tiene que ser 130 o menos.';
    return '';
  },
  talle: (valor) => (estado.actividad && estado.actividad.requiere_talle && !valor ? 'Elegí un talle.' : ''),
};

function validarCampo(campo) {
  const mensaje = REGLAS[campo.name](campo.value.trim());
  if (mensaje) marcarCampo(campo, mensaje);
  else desmarcarCampo(campo);
  return !mensaje;
}

function validarTerminos() {
  if ($('acepta-terminos').checked) {
    desmarcarCampo($('acepta-terminos'));
    return true;
  }
  marcarCampo($('acepta-terminos'), 'Tenés que aceptar los términos y condiciones para reservar.');
  return false;
}

function validarFormulario() {
  const campos = [...$('participantes').querySelectorAll('[name]')];
  // Sin cortocircuito: se marcan todos los errores de una vez.
  const camposValidos = campos.map(validarCampo).every(Boolean);
  const terminosValidos = validarTerminos();
  return camposValidos && terminosValidos;
}

function esCampoDeParticipante(elemento) {
  return Boolean(elemento.name && REGLAS[elemento.name] && elemento.closest('.participante'));
}

function mostrarErrores({ codigo, detalle, errores }) {
  $('error-general').textContent = detalle;
  $('error-general').hidden = false;
  const fieldsets = $('participantes').children;

  // Formato: errores.participantes es {indice: {campo: [mensajes]}}.
  const porParticipante = (errores && errores.participantes) || {};
  for (const [indice, campos] of Object.entries(porParticipante)) {
    if (typeof campos !== 'object' || Array.isArray(campos) || !fieldsets[indice]) continue;
    for (const [nombre, mensajes] of Object.entries(campos)) {
      const campo = fieldsets[indice].querySelector(`[name="${nombre}"]`);
      if (campo) marcarCampo(campo, mensajes.join(' '));
    }
  }

  // Reglas de negocio que se pueden ubicar en un campo concreto.
  if (codigo === 'talle_requerido') {
    for (const select of $('participantes').querySelectorAll('select[name="talle"]')) {
      if (!select.value) marcarCampo(select, 'Elegí un talle.');
    }
  }
  if (codigo === 'terminos_no_aceptados') {
    marcarCampo($('acepta-terminos'), 'Tenés que aceptar los términos y condiciones para reservar.');
  }

  const primerCampo = document.querySelector('#form-reserva [aria-invalid="true"]');
  (primerCampo || $('error-general')).focus();
  $('error-general').scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// ---------- Confirmación ----------

function mostrarConfirmacion(inscripcion) {
  $('confirmacion-actividad').textContent = inscripcion.actividad;
  $('confirmacion-fecha').textContent =
    `${formatoDiaLargo.format(aFecha(inscripcion.fecha))} · ${inscripcion.hora_inicio} hs`;
  $('confirmacion-codigo').textContent = inscripcion.codigo;
  $('confirmacion-participantes').replaceChildren(
    ...inscripcion.participantes.map((participante) => {
      const item = crear('li', null, participante.nombre);
      const talle = participante.talle ? ` · Talle ${participante.talle}` : '';
      item.append(crear('span', null, `DNI ${participante.dni}${talle}`));
      return item;
    }),
  );
  document.querySelector('.encabezado').hidden = true;
  $('reserva').hidden = true;
  $('confirmacion').hidden = false;
  window.scrollTo({ top: 0 });
  $('confirmacion').focus();
}

async function confirmar(evento) {
  evento.preventDefault();
  if (!estado.horario) return;
  limpiarErrores();
  if (!validarFormulario()) {
    $('error-general').textContent = 'Revisá los datos marcados en rojo antes de confirmar.';
    $('error-general').hidden = false;
    document.querySelector('#form-reserva [aria-invalid="true"]').focus();
    return;
  }
  $('confirmar').disabled = true;
  $('confirmar').setAttribute('aria-busy', 'true');

  const { ok, datos } = await api('/api/inscripciones/', {
    method: 'POST',
    body: JSON.stringify({
      actividad_id: estado.actividad.id,
      horario_id: estado.horario.id,
      acepta_terminos: $('acepta-terminos').checked,
      participantes: leerParticipantes(),
    }),
  });

  $('confirmar').removeAttribute('aria-busy');
  $('confirmar').disabled = false;
  if (ok) {
    mostrarConfirmacion(datos);
  } else {
    mostrarErrores(datos);
  }
}

// ---------- Eventos ----------

$('form-reserva').addEventListener('change', (evento) => {
  const { name, value } = evento.target;
  if (name === 'actividad') elegirActividad(Number(value));
  else if (name === 'dia') dibujarTurnos(value);
  else if (name === 'horario') elegirHorario(Number(value));
  else actualizar();
});
$('form-reserva').addEventListener('input', (evento) => {
  // Un campo marcado se revalida mientras se corrige, así el error se va apenas está bien.
  if (esCampoDeParticipante(evento.target) && evento.target.hasAttribute('aria-invalid')) {
    validarCampo(evento.target);
  }
  actualizar();
});
// Validación al salir del campo, no mientras se escribe por primera vez.
$('form-reserva').addEventListener('focusout', (evento) => {
  if (esCampoDeParticipante(evento.target) && evento.target.value.trim()) validarCampo(evento.target);
});
$('acepta-terminos').addEventListener('change', () => {
  if ($('acepta-terminos').hasAttribute('aria-invalid')) validarTerminos();
});
$('cantidad').addEventListener('change', () => cambiarCantidad(0));
$('menos').addEventListener('click', () => cambiarCantidad(-1));
$('mas').addEventListener('click', () => cambiarCantidad(1));
$('form-reserva').addEventListener('submit', confirmar);

cargarActividades();
