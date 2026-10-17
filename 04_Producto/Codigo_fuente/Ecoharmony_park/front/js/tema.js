// Tema claro u oscuro. Se carga en el <head>, antes de pintar, para que la
// página no parpadee con el tema equivocado al recargar.

(() => {
  const CLAVE = 'tema';
  const raiz = document.documentElement;
  const sistemaOscuro = window.matchMedia('(prefers-color-scheme: dark)');

  function leerGuardado() {
    try {
      return localStorage.getItem(CLAVE);
    } catch {
      return null; // Navegación privada o almacenamiento bloqueado: sigue al sistema.
    }
  }

  function guardar(tema) {
    try {
      localStorage.setItem(CLAVE, tema);
    } catch {
      // Sin almacenamiento la elección dura hasta recargar, y está bien.
    }
  }

  function temaActivo() {
    return leerGuardado() || (sistemaOscuro.matches ? 'oscuro' : 'claro');
  }

  function aplicar() {
    const guardado = leerGuardado();
    if (guardado) raiz.dataset.tema = guardado;
    else delete raiz.dataset.tema;
    raiz.dataset.temaActivo = temaActivo();

    const boton = document.getElementById('boton-tema');
    if (boton) {
      const destino = temaActivo() === 'oscuro' ? 'claro' : 'oscuro';
      boton.setAttribute('aria-label', `Cambiar a modo ${destino}`);
      boton.title = `Cambiar a modo ${destino}`;
    }
  }

  aplicar();
  sistemaOscuro.addEventListener('change', aplicar);

  document.addEventListener('DOMContentLoaded', () => {
    aplicar();
    document.getElementById('boton-tema').addEventListener('click', () => {
      guardar(temaActivo() === 'oscuro' ? 'claro' : 'oscuro');
      aplicar();
    });
  });
})();
