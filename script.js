// Показывает приветствие по нажатию на кнопку. Повторные нажатия
// просто перезаписывают текст, поэтому дубликатов не возникает.
document.getElementById('greet-button').addEventListener('click', function () {
  document.getElementById('message').textContent = 'Добрый вечер';
});
