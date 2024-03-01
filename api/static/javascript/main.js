const removeAccents = str =>
  str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');

/**
 * Convert any number to milliseconds
 * @param {number} value - `int` value to be converted to milliseconds
 * @param {'seconds' | 'minutes'| 'hours'} type - Type of `value` sent to convert
 * @returns 
 */
const convertToMilliseconds = (value, type) => {
  switch (type) {
    case 'seconds':
      return value * 1000;
    case 'minutes':
      return value * 60 * 1000;
    case 'hours':
      return value * 60 * 60 * 1000;
    default:
      throw new Error('Tipo inválido. Use "seconds", "minutes" ou "hours".');
  }
}

const toggleTheme = () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    document.querySelector('#darkModeToggle').checked = (savedTheme === 'dark');
  }

  document.getElementById('darkModeToggle').addEventListener('click', function () {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';

    document.documentElement.setAttribute('data-bs-theme', newTheme);

    localStorage.setItem('theme', newTheme);
  });
}

document.addEventListener('DOMContentLoaded', toggleTheme);
