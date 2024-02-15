/* Ir a detalle al hacer click en un registro */

window.addEventListener("load", async () => {
  const rows = document.querySelectorAll('.tr-linea');
  rows.forEach((row) => {
    row.addEventListener('click', (e) => {
      // Redirige al usuario a la página correspondiente
      window.location.href = row.dataset['href'];
    });
  });
});
