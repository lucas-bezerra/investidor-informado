// Get the input field and table
let searchInput = document.getElementById('searchInput');
let table = document.querySelector('.table');
let tableRows = table.getElementsByTagName('tr');

// Add keyup event listener to the input field
searchInput.addEventListener('keyup', function () {
  let filter = searchInput.value.toLowerCase();
  filter = removeAccents(filter)

  // Loop through all table rows and hide those that don't match the search input
  for (let i = 1; i < tableRows.length; i++) {
    let row = tableRows[i];
    let cells = row.getElementsByTagName('td');
    let displayRow = false;

    // Check each cell in current row for the search input value
    for (let j = 0; j < cells.length; j++) {
      let cell = cells[j];
      if (cell) {
        let cellValue = cell.textContent || cell.innerText;
        cellValue = removeAccents(cellValue)
        if (cellValue.toLowerCase().indexOf(filter) > -1) {
          displayRow = true;
          break;
        }
      }
    }

    // Show or hide the row based on search input match
    if (displayRow) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  }
});

function sortTable (n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("datatable");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}