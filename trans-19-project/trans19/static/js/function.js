function searching() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("INPUT");
  filter = input.value.toUpperCase();
  table = document.getElementById("TABLE");
  tr = table.getElementsByTagName("tr");
  myselect = document.getElementById("tableheading");
  for (i = 0; i < tr.length; i++) {
    if (myselect.selectedIndex == "0") {
      for (j = 0; j < myselect.value; j++) {
        td = tr[i].getElementsByTagName("td")[j];
        if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1){
            tr[i].style.display = "";
            break;
          } else
              tr[i].style.display = "none";
        }
      }
    } else {
      td = tr[i].getElementsByTagName("td")[myselect.value];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1){
          tr[i].style.display = "";
        } else
          tr[i].style.display = "none";
      }
    }
  }
}

function sorting(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("TABLE");
  switching = true;
  dir = "asc"; 
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("td")[n];
      y = rows[i + 1].getElementsByTagName("td")[n];
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++;      
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}