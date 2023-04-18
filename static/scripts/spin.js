function placeLinesOnCircle(diameter, numLines) {
    const radius = diameter / 2;
    var lineContainer = $("#spin");
    const centerX = 40;
    const centerY = 93;
    const angleStep = 2 * Math.PI / numLines;
    console.log(window.innerWidth)
    for (let i = 0; i < numLines; i++) {
      const angle = angleStep * i;
      const lineX = centerX + radius * Math.cos(angle);
      const lineY = centerY + radius * Math.sin(angle);
      const lineAngle = angle + Math.PI; // obróć linię o 90 stopni, aby była skierowana do środka okręgu
  
      const line = document.createElement("div");
      line.classList.add("line");
      line.style.left = `${lineX}px`;
      line.style.top = `${lineY}px`;
      line.style.transform = `rotate(${lineAngle}rad)`;
      line.style.position = "absolute";
      line.setAttribute('data-index', i);
      $("#spin").append(line);
    }
  }
  