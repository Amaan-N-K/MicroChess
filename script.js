const board = document.querySelector(".board");

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
    row.appendChild(cell);
  }
  board.appendChild(row);
}
