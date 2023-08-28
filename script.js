const board = document.querySelector(".board");

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

let selectedCell = null;

async function handleCellClick(event) {
  const row = event.target.dataset.row_count;
  const col = event.target.dataset.col_count;
  console.log("Event target:", event.target);
  console.log("Classes:", event.target.classList);

  if (!selectedCell) {
    selectedCell = { row, col };
  } else {
    // Send request to Flask API
    const response = await fetch("http://localhost:5000/move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        old_coor: selectedCell,
        new_coor: { row, col },
      }),
    });

    if (response.ok) {
      // Remove classes from the old cell
      const oldCell = document.querySelector(
        `[data-row_count='${selectedCell.row}'][data-col_count='${selectedCell.col}']`
      );
      const newCell = document.querySelector(`[data-row_count='${row}'][data-col_count='${col}']`);

      const pieceClass = Array.from(oldCell.classList).find(
        (cls) => cls.endsWith("-b") || cls.endsWith("-w")
      );

      if (pieceClass) {
        // Remove the class representing the piece from the old cell
        oldCell.classList.remove(pieceClass);

        // Add the class to the new cell
        event.target.classList.add(pieceClass);
      }
      oldCell.classList.remove("chess-piece");
      newCell.classList.remove("chess-piece");
      newCell.classList.add("chess-piece");
    }

    selectedCell = null;
  }
}
