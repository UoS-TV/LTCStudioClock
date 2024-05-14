const socket = io();

socket.on("connect", () => {
  console.log("Connected to server");
});

socket.on("timecode", (timecode) => {
  updateTimecode(timecode);
});

function updateTimecode(timecode) {
  const [hh, mm, ss, ff] = timecode.split(":");
  const timeContainer = document.getElementById("time-container");
  timeContainer.children[0].innerText = hh + ':' + mm;
  timeContainer.children[1].innerText = ss;
  timeContainer.children[2].innerText = ff;

  const seconds = parseInt(ss);
  updateSecondsOpacity(seconds);
}

function updateSecondsOpacity(seconds) {
  const secondsContainer = document.getElementById("seconds-container");
  secondsContainer.innerHTML = "";

  for (let i = 0; i < 60; i++) {
    const dot = document.createElement("div");
    dot.classList.add("dot");
    dot.style.backgroundColor = 'red';
    dot.style.transform = `rotate(${6 * (i+1)}deg) translate(40vh)`;
    secondsContainer.appendChild(dot);

    // Calculate opacity based on seconds
    const opacity = seconds >= (i+1) ? 1 : 0.4;
    dot.style.opacity = opacity;
  }
}

const hoursContainer = document.getElementById("hours-container");
hoursContainer.innerHTML = "";

for (let i = 0; i < 12; i++) {
  const dot = document.createElement("div");
  dot.classList.add("dot");
  dot.style.backgroundColor = 'orange';
  dot.style.transform = `rotate(${30 * i}deg) translate(44vh)`;
  hoursContainer.appendChild(dot);
}
