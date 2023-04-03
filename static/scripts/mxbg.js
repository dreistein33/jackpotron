const MAX_OBJECTS = 300;
const OBJECTS_LIST = [];

function generateDollarSign() {
  if (OBJECTS_LIST.length < MAX_OBJECTS) {
    const dollarSign = document.createElement("span");
    const numBars = Math.floor(Math.random() * 8) + 3;
    dollarSign.classList.add("dollar");
    dollarSign.textContent = "$";
    const leftPosition = Math.random() * window.innerWidth;
    dollarSign.style.left = leftPosition + "px";
    dollarSign.style.animationDuration = Math.random() * 9 + 1 + "s";
    dollarSign.style.top = "120";
    document.body.appendChild(dollarSign);

    for (let i = 0; i < numBars; i++) {
      const verticalBar = document.createElement("span");
      verticalBar.classList.add("bar");
      verticalBar.textContent = "|";
      verticalBar.style.left = leftPosition + 3 + "px";
      verticalBar.style.top = dollarSign.style.top - 18 * i + "px";
      verticalBar.style.animationDuration = dollarSign.style.animationDuration;

      if (i > 0) {
        document.body.appendChild(verticalBar);
      }
      verticalBar.addEventListener("animationend", removeBarSign);
    }
    dollarSign.addEventListener("animationend", removeDollarSign);
    OBJECTS_LIST.push(dollarSign);

  }
}
setInterval(generateDollarSign, 100);

function removeDollarSign() {
  const dollarSign = this;
  dollarSign.remove();
  OBJECTS_LIST.splice(OBJECTS_LIST.indexOf(dollarSign), 1);
}
function removeBarSign() {
  const verticalBar = this;
  verticalBar.remove();
  OBJECTS_LIST.splice(OBJECTS_LIST.indexOf(verticalBar.parentNode), 1);
}

setInterval(() => {
  OBJECTS_LIST.forEach((object) => object.remove());
  OBJECTS_LIST.length = 0;
}, 6000);
