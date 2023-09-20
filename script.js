const board = document.querySelector(".board");
let selectedPiece = null;

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

async function handleCellClick(event) {
  const row = event.target.dataset.row_count;
  const col = event.target.dataset.col_count;

  if (!selectedPiece) {
    // Handle the click on a piece
    const pieceResponse = await fetch(`http://localhost:5000/get_legal_moves/${row}/${col}`);
    if (pieceResponse.ok) {
      const pieceData = await pieceResponse.json();
      if (pieceData.legal_moves.length > 0) {
        // Highlight legal moves
        pieceData.legal_moves.forEach(move => {
          const cell = document.querySelector(`[data-row_count='${move[0]}'][data-col_count='${move[1]}']`);
          cell.classList.add('legal-move');
        });

        // Store the selected piece for future reference
        selectedPiece = { row, col };
      }
    }
  } else {
    // Handle the click on a legal move
    const moveResponse = await fetch(`http://localhost:5000/move`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        old_coor: selectedPiece,
        new_coor: { row, col },
      }),
    });

    if (moveResponse.ok) {
      // Update the visual appearance of the pieces
      const oldPieceCell = document.querySelector(
        `[data-row_count='${selectedPiece.row}'][data-col_count='${selectedPiece.col}']`
      );
      const newPieceCell = event.target;

      // Remove the class representing the piece from the old cell
      const oldPieceClass = Array.from(oldPieceCell.classList).find(
        (cls) => cls.endsWith("-b") || cls.endsWith("-w")
      );
      oldPieceCell.classList.remove(oldPieceClass);

      // Add the class representing the piece to the new cell
      const newPieceClass = Array.from(newPieceCell.classList).find(
        (cls) => cls.endsWith("-b") || cls.endsWith("-w")
      );
      newPieceCell.classList.remove(newPieceClass);
      newPieceCell.classList.add(oldPieceClass);

      // Update the data attributes for the new cell
      newPieceCell.dataset.row_count = selectedPiece.row;
      newPieceCell.dataset.col_count = selectedPiece.col;

      // Adjust the size of the piece to prevent it from becoming too large
      newPieceCell.style.backgroundSize = 'contain';

      // Remove glow from legal moves
      document.querySelectorAll('.legal-move').forEach(cell => cell.classList.remove('legal-move'));
    }

    // Reset selectedPiece
    selectedPiece = null;
  }
}
