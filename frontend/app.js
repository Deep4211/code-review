async function run() {
  const model = document.getElementById("model").value;

  await fetch(`/run?model_name=${model}`, {
    method: "POST"
  });

  loadLeaderboard();
}

async function loadLeaderboard() {
  const res = await fetch("/leaderboard");
  const data = await res.json();

  const board = document.getElementById("board");
  board.innerHTML = "";

  data.forEach(item => {
    const li = document.createElement("li");
    li.innerText = `${item.model} → ${item.score.toFixed(2)}`;
    board.appendChild(li);
  });
}

loadLeaderboard();
