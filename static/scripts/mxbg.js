let generatedObjects = 0;
const maxObjects = 300;
const objectsList = [];

function generateDollarSign() {
  if (generatedObjects < maxObjects) {
    const dollar = document.createElement("span");
    const numBars = Math.floor(Math.random() * 8) + 3;
    const barHeight = 20;
    const barSpacing = 5;
    dollar.classList.add("dollar");
    dollar.textContent = "$";
    var left = Math.random() * window.innerWidth;
    dollar.style.left = left + "px";
    dollar.style.animationDuration = Math.random() * 9 + 1 + "s";
    dollar.style.top = "120";
    document.body.appendChild(dollar);

    for (let i = 0; i < numBars; i++) {
      const bar = document.createElement("span");
      bar.classList.add("bar");
      bar.textContent = "|";
      bar.style.left = left + 3 + "px";
      bar.style.top = dollar.style.top - 10 * i + "px";
      bar.style.animationDuration = dollar.style.animationDuration;

      if (i == 0) {
        true;
      } else {
        document.body.appendChild(bar);
      }


      bar.addEventListener("animationend", function() {
        removeBarSign(bar);
      });

      dollar.addEventListener("animationend", function() {
        removeDollarSign(dollar);
      });
    }

    objectsList.push(dollar);
    generatedObjects++;

    // Aktualizacja liczby wygenerowanych obiektów
    document.querySelector("#generated-objects").textContent = generatedObjects;
  }
}

setInterval(generateDollarSign, 1000 * 0.01);

function removeDollarSign(dollar) {
  setTimeout(function() {
    dollar.remove();
    objectsList.splice(objectsList.indexOf(dollar), 1);

    // Aktualizacja liczby wygenerowanych obiektów
    if (generatedObjects > 150) {
      generatedObjects--;
    }
    document.querySelector("#generated-objects").textContent = generatedObjects;
  }, parseFloat(dollar.style.animationDuration) * 1);
}

function removeBarSign(bar) {
  setTimeout(function() {
    bar.remove();
    objectsList.splice(objectsList.indexOf(bar), 1);
  }, parseFloat(bar.style.animationDuration) * 1);
}


setInterval(function() {
  objectsList.forEach(function(object) {
    object.remove();
  });
  objectsList.length = 0;
  generatedObjects = 0;

  // Aktualizacja liczby wygenerowanych obiektów
  document.querySelector("#generated-objects").textContent = generatedObjects;
}, 5000 );
