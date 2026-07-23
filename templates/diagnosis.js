const questions = [
  { q: "Do you have enough space？", A: "Not so much", B: "Yes", C: "much space", D: "it's not matter, i like retro vibes." },
  { q: "About volume？", A: "I usually play at night", B: "I guess neighbors want me to stay quiet.", C: "Nobody cares", D: "I would like to have old sound" },
  { q: "What is th purpose？", A: "I just want to practice at home", B: "I want to have fun as one of me hobbies", C: "I would like to play real classic", D: "I would like to enjoy traditional or special features." },
  { q: "Price?", A: "cheap", B: "normal", C: "expensive", D: "no matter, vibe is more important" },
  { q: "What kind of design？", A: "simple and small", B: "for a house and normal design", C: "gorgeous and professional", D: "retro and wooden disign" },
  { q: "The conditions of the keyboard？", A: "Light", B: "Average", C: "Heavy", D: "Old and unique touch" },
  { q: "How often do you want to play？", A: "When I feel I want to.", B: "For a few times in a week", C: "Everyday", D: "For a vibe, not for playing" },
  { q: "Size？", A: "It must be small", B: "A little small", C: "Never mind", D: "Bigger" },
  { q: "Sound？", A: "soft and quiet", B: "Bright and for home use.", C: "Strong and various.", D: "Unique sound" },
  { q: "Do you need specific features？", A: "No need.", B: "Something common", C: "Authentic features", D: "Auto-performing or retro effects" }
];

let current = 0;
let answers = [];

function showQuestion() {
  const q = questions[current];
  const container = document.getElementById("question-container");

  container.innerHTML = `
    <h2>${q.q}</h2>
    <button onclick="selectAnswer('A')">A: ${q.A}</button>
    <button onclick="selectAnswer('B')">B: ${q.B}</button>
    <button onclick="selectAnswer('C')">C: ${q.C}</button>
    <button onclick="selectAnswer('D')">D: ${q.D}</button>
  `;
}

function selectAnswer(letter) {
  answers.push(letter);
  current++;

  if (current < questions.length) {
    showQuestion();
  } else {
    sendToPython();
  }
}

function sendToPython() {
  fetch("/diagnosis", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers })
  })
  .then(res => res.json())
  .then(data => showResult(data));
}

function showResult(data) {
  const container = document.getElementById("result-container");
  container.style.display = "block";

  let html = "<h2>診断結果</h2>";

  data.forEach((item, index) => {
    html += `<h3>第${index + 1}希望（タイプ ${item.type}）</h3>`;
    item.pianos.forEach(p => {
      html += `<p>・${p}</p>`;
    });
  });

  document.getElementById("question-container").innerHTML = "";
  container.innerHTML = html;
}

showQuestion();
