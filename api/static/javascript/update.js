function updateCache (btn) {
  if (btn) {
    btn.disabled = true;
  }
  
  fetch('/update-cache', {
    method: 'POST'
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro ao atualizar dados');
      }
      return response.text();
    })
    .then(data => {
      console.log(data);
      window.location.reload();
    })
    .catch(error => {
      console.error(error);
      if (btn) {
        btn.disabled = false;
      }
    });
}

// Update table after 30 minutes
const timeInMilliseconds = convertToMilliseconds(30, 'minutes');
var timer = setTimeout(updateCache, timeInMilliseconds);