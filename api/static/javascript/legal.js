$(document).ready(function () {
  // Verifica se o modal deve ser exibido
  var ultimaExibicao = localStorage.getItem('legalModal');
  var agora = new Date().getTime();

  if (!ultimaExibicao || agora - ultimaExibicao > 24 * 60 * 60 * 1000) {
    // Se não foi exibido nas últimas 24 horas, exibe o modal
    $('#avisoLegalModal').modal('show');

    // Atualiza o timestamp da última exibição
    localStorage.setItem('legalModal', agora);
  }
});