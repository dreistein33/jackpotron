function placeLinesOnCircle(diameter, numLines) {
    const radius = diameter / 2;
    var lineContainer = $("#line-container");
    const centerX = lineContainer.width() / 2.78;
    const centerY = lineContainer.height() * 0.474;
    const angleStep = 2 * Math.PI / numLines;
  
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
      line.style.display = "inline-block";
      line.setAttribute('data-index', i);
      $("#line-container").append(line);
    }
  }
  
function colorLinesOnCircle(users) {
    let start = 0;
    let end = 0;

    for (let x = 0; x < users.length; x++) {
        var us = users[x];
        end += Math.floor(us.probability * 100);      
        if (end == 99) {
            end++;
        }
        const lines = $("#line-container .line");
        var userDiv = $("#user" + us.sender);

        for (let i = start; i < end; i++) {
            lines.eq(i).animate(
                {"backgroundColor": userDiv.attr("potColor")},
                2000,
                function() {
                    $(this).css({"backgroundColor": userDiv.attr("potColor")});
                }
            );
        }

        start = end;
    }
}
  