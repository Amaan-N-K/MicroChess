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

window.onload = function() {
    fetch('http://localhost:5000/reset_game', {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.message) {
            console.log(data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};

let legalMoves = [];  // New global variable to store legal moves

async function handleCellClick(event) {
  const row = parseInt(event.target.dataset.row_count, 10);
  const col = parseInt(event.target.dataset.col_count, 10);

  // Clear previous legal move indicators
  document.querySelectorAll('.legal-move-circle').forEach(circle => circle.remove());

  if (!selectedPiece) {
    // Handle the click on a piece
    const pieceResponse = await fetch(`http://localhost:5000/get_legal_moves/${row}/${col}`);

    if (pieceResponse.status === 400) {
      alert('Wrong turn! Please choose a valid piece.');
      return;
    }

    if (pieceResponse.ok) {
      const pieceData = await pieceResponse.json();

      if (pieceData.legal_moves && pieceData.legal_moves.length > 0) {
        pieceData.legal_moves.forEach(move => {
          const cell = document.querySelector(`[data-row_count='${move[0]}'][data-col_count='${move[1]}']`);
          const circle = document.createElement('div');
          circle.classList.add('legal-move-circle');
          cell.appendChild(circle);
        });

        legalMoves = pieceData.legal_moves;
        selectedPiece = { row, col };
      }
    }
  } else {
    const isLegalMove = legalMoves.some(move => move[0] === row && move[1] === col);
    if (!isLegalMove) {
      selectedPiece = null;
      legalMoves = [];
      return;
    }

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

      // Handle in_check logic
      if (moveData.in_check) {
        const kingCell = document.querySelector(`[data-row_count='${moveData.king_position[0]}'][data-col_count='${moveData.king_position[1]}']`);
        kingCell.style.backgroundColor = 'pink';
        kingCell.classList.add('in-check');
      } else {
        // If the king is not in check, reset any square marked 'in-check' to its default color
        const previouslyCheckedKing = document.querySelector('.in-check');
        if (previouslyCheckedKing) {
          const isWhiteSquare = (parseInt(previouslyCheckedKing.dataset.row_count, 10) + parseInt(previouslyCheckedKing.dataset.col_count, 10)) % 2 === 0;
          previouslyCheckedKing.style.backgroundColor = isWhiteSquare ? 'var(--white-cell)' : 'var(--black-cell)';
          previouslyCheckedKing.classList.remove('in-check');
        }
      }

      // Update the visual appearance of the pieces
      const oldPieceCell = document.querySelector(`[data-row_count='${selectedPiece.row}'][data-col_count='${selectedPiece.col}']`);
      const newPieceCell = event.target;

      const oldPieceClass = Array.from(oldPieceCell.classList).find((cls) => cls.endsWith("-b") || cls.endsWith("-w"));
      oldPieceCell.classList.remove(oldPieceClass);

      const existingPieceClass = Array.from(newPieceCell.classList).find((cls) => cls.endsWith("-b") || cls.endsWith("-w"));
      if (existingPieceClass) {
        newPieceCell.classList.remove(existingPieceClass);
      }

      newPieceCell.classList.add(oldPieceClass);
      newPieceCell.style.backgroundSize = 'contain';

      if (moveData.game_over) {
        const kingCell = document.querySelector(`[data-row_count='${moveData.king_position[0]}'][data-col_count='${moveData.king_position[1]}']`);
        kingCell.style.backgroundColor = 'red';

        setTimeout(() => {
          alert(moveData.message);
          location.reload();
        }, 50);
        return;
      }

      selectedPiece = null;
      legalMoves = [];
      if (moveData.ai_move) {
      console.log("157");
        // If AI's king is in check, make it glow pink for half a second
        if (moveData.ai_in_check) {
        const kingCell = document.querySelector(`[data-row_count='${moveData.ai_king_position[0]}'][data-col_count='${moveData.ai_king_position[1]}']`);
        kingCell.style.backgroundColor = 'pink';
        kingCell.classList.add('in-check');
        console.log("This line is being executed");
        await new Promise(resolve => setTimeout(resolve, 500));  // Wait for half a second
        }

        // Make the AI's move after highlighting in_check (if applicable)
        const aiOldCoor = moveData.ai_move.old_coor;
        const aiNewCoor = moveData.ai_move.new_coor;

        const aiOldPieceCell = document.querySelector(`[data-row_count='${aiOldCoor.row}'][data-col_count='${aiOldCoor.col}']`);
        const aiNewPieceCell = document.querySelector(`[data-row_count='${aiNewCoor.row}'][data-col_count='${aiNewCoor.col}']`);

        const aiOldPieceClass = Array.from(aiOldPieceCell.classList).find((cls) => cls.endsWith("-b") || cls.endsWith("-w"));
        aiOldPieceCell.classList.remove(aiOldPieceClass);

        const aiExistingPieceClass = Array.from(aiNewPieceCell.classList).find((cls) => cls.endsWith("-b") || cls.endsWith("-w"));
        if (aiExistingPieceClass) {
        aiNewPieceCell.classList.remove(aiExistingPieceClass);
        }

        aiNewPieceCell.classList.add(aiOldPieceClass);
        aiNewPieceCell.style.backgroundSize = 'contain';

        // Reset the 'in-check' status after the move is done
        const previouslyCheckedKing = document.querySelector('.in-check');
        if (previouslyCheckedKing) {
        const isWhiteSquare = (parseInt(previouslyCheckedKing.dataset.row_count, 10) + parseInt(previouslyCheckedKing.dataset.col_count, 10)) % 2 === 0;
        previouslyCheckedKing.style.backgroundColor = isWhiteSquare ? 'var(--white-cell)' : 'var(--black-cell)';
        previouslyCheckedKing.classList.remove('in-check');
        }

        // Handle game_over logic for AI's move
        if (moveData.ai_game_over) {
        const kingCell = document.querySelector(`[data-row_count='${moveData.white_king_position[0]}'][data-col_count='${moveData.white_king_position[1]}']`);
        kingCell.style.backgroundColor = 'red';

        setTimeout(() => {
          alert(moveData.result_message);
          location.reload();
        }, 50);
        return;
        }
      }
    }
  }
}
const modeText = document.getElementById('modeText');
const modeToggle = document.getElementById('modeToggle');

// Function to set mode text based on toggle state
function updateModeText() {
    if (modeToggle.checked) {
        modeText.textContent = "Player vs Computer";
    } else {
        modeText.textContent = "Player vs Player";
    }
}

// Set the toggle state and mode text based on sessionStorage
const savedToggleState = sessionStorage.getItem('modeToggleState');
if (savedToggleState !== null) {
    modeToggle.checked = savedToggleState === 'true';
}
updateModeText();  // Update mode text based on initial toggle state

modeToggle.addEventListener('change', function() {
    // Save the current state of the toggle to sessionStorage
    sessionStorage.setItem('modeToggleState', modeToggle.checked);

    updateModeText();  // Update mode text based on changed toggle state

    // Change the game mode on the server when the toggle is clicked
    fetch('http://localhost:5000/change_mode')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.message) {
            console.log(data.message);

            // Refresh the page to reset the frontend board
            window.location.reload();
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});





