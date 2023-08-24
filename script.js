const board = document.querySelector(".board");

function handleCellClick(event) {
  alert(
    `You clicked on row ${event.target.dataset.row_count}, column ${event.target.dataset.col_count}`
  );
}

const initialSetup = [
  ["king-b", "knight-b", "bishop-b", "rook-b"],
  ["pawn-b"],
  [],
  [null, null, null, "pawn-w"],
  ["rook-w", "bishop-w", "knight-w", "king-w"],
];

for (let i = 0; i < 5; i++) {
  const row = document.createElement("div");
  row.style.display = "flex";

  for (let j = 0; j < 4; j++) {
    const cell = document.createElement("div");
    cell.dataset.row_count = i;
    cell.dataset.col_count = j;

    cell.classList.add("cell");
    const color = (i + j) % 2 == 0 ? "light" : "dark";
    cell.classList.add(color);

    if (initialSetup[i] && initialSetup[i][j]) {
      cell.classList.add("chess-piece", initialSetup[i][j]);
    }

    cell.addEventListener("click", handleCellClick);
    row.appendChild(cell);
  }
  board.appendChild(row);
}
