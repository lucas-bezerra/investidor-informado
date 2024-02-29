// Set the countdown date/time
var countdownDate = new Date();
countdownDate.setMinutes(countdownDate.getMinutes() + 360);

// Update the countdown every second
var timer = setInterval(function () {
  var now = new Date().getTime();
  var distance = countdownDate - now;

  // Calculate remaining time
  var hours = Math.floor((distance % (1000 * 60 * 60 * 60)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the countdown in the element with id="countdown"
  document.getElementById("countdown").innerHTML = "Atualização automática em: " + hours + "h " + minutes + "m " + seconds + "s ";

  // When the countdown is over, display a message
  if (distance < 0) {
    clearInterval(timer);
    document.getElementById("countdown").innerHTML = "ATUALIZANDO";
  }
}, 1000);