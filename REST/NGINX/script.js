// Initialisieren der Eingabefelder
var quantityInput = document.getElementById('quantity');
var bitsInput = document.getElementById('bits');

// Deaktivieren der Eingabefelder
quantityInput.disabled = true;
bitsInput.disabled = true;

/*------------------------------------------Init Button-----------------------------------------------*/
document.getElementById('initButton').addEventListener('click', function() {

  //zurücksetzen von status und description
  document.getElementById('description').innerText = '';
  document.getElementById('status').innerText = '';
  document.getElementById('result').innerText = '';

  showLoadingSpinner('Start-up tests and system initialization in progress.'); 

  fetch('https://172.16.78.57:5000/trng/randomNum/init')
    .then(response => {
      document.getElementById('status').innerText = 'Status: ' + response.status;
      return response.json();
    })
    .then(data => {
      document.getElementById('description').innerText = data.description;
      console.log('Initialisierung erfolgreich');
      
      // Deaktiviere Generate und Shutdown Buttons
      //document.getElementById('generateButton').disabled = false;
      document.getElementById('shutdownButton').disabled = false;
      // Aktiviere Initialize Button
      document.getElementById('initButton').disabled = true;
      
    // Aktivieren der Eingabefelder
    quantityInput.disabled = false;
    bitsInput.disabled = false;
    })
    .catch(error => {
      console.error('Fehler beim Initialisieren:', error);
    })
    .finally(() => {
      hideLoadingSpinner(); 
    });
});

/*------------------------------------------Generate Button-----------------------------------------------*/
document.getElementById('generateButton').addEventListener('click', function(event) {
  // Zurücksetzen von status und description
  document.getElementById('description').innerText = '';
  document.getElementById('status').innerText = '';
  document.getElementById('result').innerText = '';

  showLoadingSpinner('Generating and testing random numbers.'); 

  var quantity = document.getElementById('quantity').value;
  var bits = document.getElementById('bits').value;

  var url = 'https://172.16.78.57:5000/trng/randomNum/getRandom';
  if (quantity && bits) {
    url += '?quantity=' + quantity + '&numBits=' + bits;
  }

  fetch(url)
    .then(response => {
      document.getElementById('status').innerText = 'Status: ' + response.status;
      return response.json();
    })
    .then(data => {
      document.getElementById('status').innerText = 'Status: ' + data.status;
      document.getElementById('description').innerText = data.description;
    
      var resultDiv = document.getElementById('result');
      resultDiv.innerHTML = ''; // Clear previous results
  
      if (data.status !== 200) {
        return; 
      }

      if (data.status === 200) {
        var table = document.createElement('table');
        table.classList.add('table');
        var thead = document.createElement('thead');
        var tbody = document.createElement('tbody');
        var trHead = document.createElement('tr');
        var thNr = document.createElement('th');
        var thCopy = document.createElement('th');
        var thRandom = document.createElement('th');
        var copyAllButton = document.createElement('button');

        thNr.textContent = 'ID';
        thCopy.textContent = ' ';
        thRandom.textContent = 'Random Number';

        trHead.appendChild(thNr);
        trHead.appendChild(thCopy);
        trHead.appendChild(thRandom);
        thead.appendChild(trHead);
        table.appendChild(thead);

        var hexNumbers = JSON.parse(data.randomNumbers); // JSON-Array parsen

        for (var i = 0; i < hexNumbers.length; i++) {
          var tr = document.createElement('tr');
          var tdNr = document.createElement('td');
          var tdCopy = document.createElement('td');
          var tdRandom = document.createElement('td');
          var copyButton = document.createElement('button');

          tdNr.textContent = (i + 1).toString();
          tdRandom.textContent = hexNumbers[i];
          copyButton.textContent = 'Copy';
          copyButton.classList.add('copy-button');

          copyButton.addEventListener('click', function() {
            copyToClipboard(this.parentElement.nextElementSibling.textContent);
          });

          tdCopy.appendChild(copyButton);
          tr.appendChild(tdNr);
          tr.appendChild(tdCopy);
          tr.appendChild(tdRandom);
          tbody.appendChild(tr);
        }

        table.appendChild(tbody);
        resultDiv.appendChild(table);

        copyAllButton.textContent = 'Copy all';
        copyAllButton.classList.add('copy-button');
        copyAllButton.style.marginBottom = '5px'; // Setze den Abstand nach unten

        copyAllButton.addEventListener('click', function() {
          copyToClipboard(hexNumbers.join('\n'));
        });

        resultDiv.insertBefore(copyAllButton, table); // Füge den "Copy all" Button vor der Tabelle ein
      } else {
      document.getElementById('status').innerText = 'Status: ' + data.status;
      document.getElementById('description').innerText = data.description;
      
        var errorParagraph = document.createElement('p');
        errorParagraph.textContent = 'Error: ' + data.message;
        resultDiv.appendChild(errorParagraph);
      }

      console.log('Generierung erfolgreich');
    })
    .catch(error => {
      console.error('Fehler beim Generieren:', error);
    })
    .finally(() => {
      hideLoadingSpinner(); 
    });
});

/*------------------------------------------Copy to Clipboard-----------------------------------------------*/
function copyToClipboard(text) {
  var textArea = document.createElement('textarea');
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand('copy');
  document.body.removeChild(textArea);

  // Anzeigen eines Popups zur Bestätigung der Kopie
  window.alert('The text has been copied to the clipboard!');
}

/*------------------------------------------Shutdown Button-----------------------------------------------*/
document.getElementById('shutdownButton').addEventListener('click', function() {
  //zurücksetzen von status und description
  document.getElementById('description').innerText = '';
  document.getElementById('status').innerText = '';
  //textfelder zurücksetzen
  document.getElementById('quantity').value = '';
  document.getElementById('bits').value = '';
  //result div zurücksetzen
  document.getElementById('result').innerText = '';

  showLoadingSpinner('Shutting down the system.'); // Zeigt den Lade-Spinner

  fetch('https://172.16.78.57:5000/trng/randomNum/shutdown')
    .then(response => {
      document.getElementById('status').innerText = 'Status: ' + response.status;
      return response.json();
    })
    .then(data => {
      document.getElementById('description').innerText = data.description;
      console.log('Herunterfahren erfolgreich');
      
      // Deaktiviere Generate und Shutdown Buttons
      document.getElementById('generateButton').disabled = true;
      document.getElementById('shutdownButton').disabled = true;
      // Aktiviere Initialize Button
      document.getElementById('initButton').disabled = false;
      
      // Deaktivieren der Eingabefelder
    quantityInput.disabled = true;
    bitsInput.disabled = true;
    })
    .catch(error => {
      console.error('Fehler beim Herunterfahren:', error);
    })
    .finally(() => {
      hideLoadingSpinner(); // Blende den Lade-Spinner aus
    });
});

// Überprüfungsfunktion für die Eingabefelder
function checkInputFields() {
  var quantity = document.getElementById('quantity').value;
  var bits = document.getElementById('bits').value;
  var generateButton = document.getElementById('generateButton');

  if (quantity && bits) {
    generateButton.disabled = false; // Aktiviere den Button, wenn beide Eingabefelder einen Wert enthalten
  } else {
    generateButton.disabled = true; // Deaktiviere den Button, wenn mindestens eines der Eingabefelder leer ist
  }
}

// Eventlistener für die Eingabefelder, der die Überprüfungsfunktion aufruft
document.getElementById('quantity').addEventListener('input', checkInputFields);
document.getElementById('bits').addEventListener('input', checkInputFields);

/*-----------------------------Initiale Deaktivierung von Generate und Shutdown Buttons-----------------------------*/ 
document.getElementById('generateButton').disabled = true;
document.getElementById('shutdownButton').disabled = true;

/*------------------------------------------Loading Spinner-----------------------------------------------*/
// Zeige den Lade-Spinner an und blockiere den Inhalt
function showLoadingSpinner(loadingText) {
  document.getElementById('overlay').classList.remove('hidden');
  document.getElementById('loadingSpinner').classList.remove('hidden');
  document.getElementById('loadingText').innerText = loadingText;
}

// Blende den Lade-Spinner aus und entsperre den Inhalt
function hideLoadingSpinner() {
  document.getElementById('overlay').classList.add('hidden');
  document.getElementById('loadingSpinner').classList.add('hidden');
  document.getElementById('loadingText').innerText = '';
}