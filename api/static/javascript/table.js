// Get the input field and table
let table = document.querySelector('.table');

$(table).DataTable({
  pageLength: 25,
  language: {
    decimal: "",
    emptyTable: "Tabela vazia",
    info: "Mostrando de _START_ até _END_ - TOTAL: _TOTAL_ linhas",
    infoEmpty: "Mostrando de 0 até 0 - TOTAL: 0 linhas",
    infoFiltered: "(filtrado de _MAX_ linhas)",
    infoPostFix: "",
    thousands: ",",
    lengthMenu: "_MENU_ linhas por página",
    loadingRecords: "Carregando...",
    processing: "",
    search: "Pesquisar:",
    zeroRecords: "Nenhum resultado encontrado",
    aria: {
      orderable: "Ordenar por esta coluna",
      orderableReverse: "Inverter ordem dessa coluna"
    }
  }
});