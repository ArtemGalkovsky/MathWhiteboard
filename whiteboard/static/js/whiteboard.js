document.addEventListener("DOMContentLoaded", () => {
    const boardContainer = document.querySelector("#whiteboard_container");

    const board = new Board(boardContainer)
    board.setup()
})