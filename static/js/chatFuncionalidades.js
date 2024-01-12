/* const botonAdjunto = document.querySelector('#file-attached-button')
const inputAdjuntos = document.getElementById('file-attached')
botonAdjunto.addEventListener('click', inputAdjuntos.click()) */
/* 
const emojiButton = document.querySelector('#emoji-button');


 */

const emojiButton = document.getElementById('emojiButton')
emojiButton.addEventListener('click', () => {
  var emojiContainer = document.getElementById('emojiContainer');

  if (emojiContainer.style.display === 'none') {
      emojiContainer.style.display = 'block';
  } else {
      emojiContainer.style.display = 'none';
  }
});

document.querySelector('emoji-picker')
  .addEventListener('emoji-click', event => {
    console.log(event.detail)
    const inputText = document.querySelector('#chat-message-input');
    inputText.value += event.detail.unicode
});

// Cierra el emoji-picker si se hace clic fuera de él
/* document.addEventListener('click', function(event) {
  var emojiContainer = document.getElementById('emojiContainer');
  var emojiButton = document.getElementById('emojiButton');

  if (event.target !== emojiButton && !emojiContainer.contains(event.target)) {
      emojiContainer.style.display = 'none';
  }
}); */

