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

let legalMoves = [];  // New global variable to store legal moves

async function handleCellClick(event) {
    const row = parseInt(event.target.dataset.row_count, 10);
    const col = parseInt(event.target.dataset.col_count, 10);

    if (!selectedPiece) {
        // Handle the click on a piece
        const pieceResponse = await fetch(`http://localhost:5000/get_legal_moves/${row}/${col}`);

        if (pieceResponse.status === 400) {
            // Inform the player that it's not the correct turn for the chosen piece
            alert('Wrong turn! Please choose a valid piece.');
            return;
        }

        if (pieceResponse.ok) {
            const pieceData = await pieceResponse.json();

            if (pieceData.legal_moves && pieceData.legal_moves.length > 0) {
                // Highlight legal moves
                pieceData.legal_moves.forEach(move => {
                    const cell = document.querySelector(`[data-row_count='${move[0]}'][data-col_count='${move[1]}']`);
                    cell.classList.add('legal-move');
                });

                // Store the legal moves
                legalMoves = pieceData.legal_moves;

                // Store the selected piece for future reference
                selectedPiece = { row, col };
            }
        }
    } else {
        // Check if the move is legal
        const isLegalMove = legalMoves.some(move => move[0] === row && move[1] === col);

        if (!isLegalMove) {
            // If not a legal move, remove highlight from legal moves and reset
            document.querySelectorAll('.legal-move').forEach(cell => cell.classList.remove('legal-move'));
            selectedPiece = null;
            legalMoves = [];
            return;
        }

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
            const moveData = await moveResponse.json();

            // Clear previous pink color for checks
            document.querySelectorAll('.in-check').forEach(cell => {
                cell.style.backgroundColor = '';
                cell.classList.remove('in-check');
            });

            // Handle in check scenario
            if (moveData.in_check) {
                const kingCell = document.querySelector(`[data-row_count='${moveData.king_position[0]}'][data-col_count='${moveData.king_position[1]}']`);
                kingCell.style.backgroundColor = 'pink';
                kingCell.classList.add('in-check');
            }

            // Update the visual appearance of the pieces
            const oldPieceCell = document.querySelector(
                `[data-row_count='${selectedPiece.row}'][data-col_count='${selectedPiece.col}']`
            );
            const newPieceCell = event.target;

            const oldPieceClass = Array.from(oldPieceCell.classList).find(
                (cls) => cls.endsWith("-b") || cls.endsWith("-w")
            );
            oldPieceCell.classList.remove(oldPieceClass);

            const existingPieceClass = Array.from(newPieceCell.classList).find(
                (cls) => cls.endsWith("-b") || cls.endsWith("-w")
            );
            if (existingPieceClass) {
                newPieceCell.classList.remove(existingPieceClass);
            }

            newPieceCell.classList.add(oldPieceClass);
            newPieceCell.style.backgroundSize = 'contain';

            document.querySelectorAll('.legal-move').forEach(cell => cell.classList.remove('legal-move'));

            if (moveData.game_over) {
                const kingCell = document.querySelector(`[data-row_count='${moveData.king_position[0]}'][data-col_count='${moveData.king_position[1]}']`);
                kingCell.style.backgroundColor = 'red';

                setTimeout(() => {
                    alert(moveData.message);
                }, 50);
            }

            // Reset selectedPiece and legalMoves for the next turn
            selectedPiece = null;
            legalMoves = [];
        }
    }
}




