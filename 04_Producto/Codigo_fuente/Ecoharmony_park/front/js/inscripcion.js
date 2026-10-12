// Página de inscripción: toda la lógica de negocio vive en la API; este
// script solo arma el formulario, envía la solicitud y muestra la respuesta.

const DIAS = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];

const $ = (id) => document.getElementById(id);

const estado = {
  actividades: [],
  actividad: null,
  horarios: [],
};

function leerCookie(nombre) {
  const valor = document.cookie
    .split('; ')
    .find((cookie) => cookie.startsWith(`${nombre}=`));
  return valor ? decodeURIComponent(valor.split('=')[1]) : '';
}

async function api(url, opciones = {}) {
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
  const datos = await respuesta.json();
  return { ok: respuesta.ok, datos };
}

// "2026-10-13" + "10:00" -> "Mar 13/10/2026 10:00", sin pasar por zonas horarias.
function formatearHorario(fecha, hora) {
  const [anio, mes, dia] = fecha.split('-').map(Number);
  const nombreDia = DIAS[new Date(anio, mes - 1, dia).getDay()];
  return `${nombreDia} ${String(dia).padStart(2, '0')}/${String(mes).padStart(2, '0')}/${anio} ${hora}`;
}

function opcion(valor, texto) {
  const elemento = document.createElement('option');
  elemento.value = valor;
  elemento.textContent = texto;
  return elemento;
}

async function cargarActividades() {
  const { datos } = await api('/api/actividades/');
  estado.actividades = datos;
  for (const actividad of datos) {
    $('actividad').append(opcion(actividad.id, actividad.nombre));
  }
}

async function elegirActividad() {
  const id = Number($('actividad').value);
  estado.actividad = estado.actividades.find((actividad) => actividad.id === id) || null;

  $('horario').replaceChildren(opcion('', 'Elegí un horario'));
  $('horario').disabled = true;
  $('sin-horarios').hidden = true;
  $('terminos').hidden = !estado.actividad;
  $('acepta-terminos').checked = false;
  elegirHorario();

  if (!estado.actividad) return;

  $('terminos-texto').textContent = estado.actividad.terminos_condiciones;
  const { datos } = await api(`/api/horarios-disponibles/?actividad_id=${id}`);
  estado.horarios = datos;
  for (const horario of datos) {
    const lugares = horario.cupo_disponible === 1 ? '1 lugar' : `${horario.cupo_disponible} lugares`;
    $('horario').append(
      opcion(horario.id, `${formatearHorario(horario.fecha, horario.hora_inicio)} — ${lugares}`),
    );
  }
  $('horario').disabled = datos.length === 0;
  $('sin-horarios').hidden = datos.length > 0;
}

function horarioElegido() {
  const id = Number($('horario').value);
  return estado.horarios.find((horario) => horario.id === id) || null;
}

function elegirHorario() {
  const horario = horarioElegido();
  $('cantidad').disabled = !horario;
  $('confirmar').disabled = !horario;
  $('cantidad').max = horario ? horario.cupo_disponible : '';
  $('cupo-ayuda').textContent = horario ? `Máximo ${horario.cupo_disponible} personas.` : '';
  dibujarParticipantes();
}

function dibujarParticipantes() {
  const contenedor = $('participantes');
  const cantidad = horarioElegido() ? Math.max(1, Number($('cantidad').value) || 1) : 0;
  const requiereTalle = Boolean(estado.actividad && estado.actividad.requiere_talle);

  // Conserva lo ya cargado al cambiar la cantidad.
  while (contenedor.children.length > cantidad) contenedor.lastElementChild.remove();
  while (contenedor.children.length < cantidad) {
    contenedor.append($('plantilla-participante').content.cloneNode(true));
  }
  [...contenedor.children].forEach((fieldset, indice) => {
    fieldset.querySelector('legend').textContent = `Participante ${indice + 1}`;
    fieldset.querySelector('.campo-talle').hidden = !requiereTalle;
  });
}

function limpiarErrores() {
  $('error-general').hidden = true;
  for (const campo of document.querySelectorAll('[aria-invalid]')) {
    campo.removeAttribute('aria-invalid');
    campo.parentElement.querySelector('small').textContent = '';
  }
}

function mostrarErrores({ detalle, errores }) {
  $('error-general').textContent = detalle;
  $('error-general').hidden = false;

  // errores.participantes es {indice: {campo: [mensajes]}} cuando falla el formato.
  const porParticipante = (errores && errores.participantes) || {};
  const fieldsets = $('participantes').children;
  for (const [indice, campos] of Object.entries(porParticipante)) {
    if (typeof campos !== 'object' || Array.isArray(campos)) continue;
    for (const [nombre, mensajes] of Object.entries(campos)) {
      const campo = fieldsets[indice] && fieldsets[indice].querySelector(`[name="${nombre}"]`);
      if (!campo) continue;
      campo.setAttribute('aria-invalid', 'true');
      campo.parentElement.querySelector('small').textContent = mensajes.join(' ');
    }
  }
  $('error-general').scrollIntoView({ behavior: 'smooth' });
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

function mostrarConfirmacion(inscripcion) {
  $('confirmacion-codigo').textContent = inscripcion.codigo;
  $('confirmacion-detalle').textContent =
    `${inscripcion.actividad} — ${formatearHorario(inscripcion.fecha, inscripcion.hora_inicio)}`;
  $('confirmacion-participantes').replaceChildren(
    ...inscripcion.participantes.map((participante) => {
      const item = document.createElement('li');
      const talle = participante.talle ? ` — Talle ${participante.talle}` : '';
      item.textContent = `${participante.nombre} — DNI ${participante.dni}${talle}`;
      return item;
    }),
  );
  $('form-inscripcion').hidden = true;
  $('confirmacion').hidden = false;
}

async function confirmar(evento) {
  evento.preventDefault();
  limpiarErrores();
  $('confirmar').setAttribute('aria-busy', 'true');

  const { ok, datos } = await api('/api/inscripciones/', {
    method: 'POST',
    body: JSON.stringify({
      actividad_id: estado.actividad.id,
      horario_id: Number($('horario').value),
      acepta_terminos: $('acepta-terminos').checked,
      participantes: leerParticipantes(),
    }),
  });

  $('confirmar').removeAttribute('aria-busy');
  if (ok) {
    mostrarConfirmacion(datos);
  } else {
    mostrarErrores(datos);
  }
}

$('actividad').addEventListener('change', elegirActividad);
$('horario').addEventListener('change', elegirHorario);
$('cantidad').addEventListener('input', dibujarParticipantes);
$('form-inscripcion').addEventListener('submit', confirmar);
cargarActividades();
