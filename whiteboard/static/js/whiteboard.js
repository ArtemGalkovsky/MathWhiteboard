document.addEventListener("DOMContentLoaded", () => {
    const boardContainer = document.querySelector("#canvas_container");

    const board = new Board(boardContainer)
    board.setup()

    const toolbar = new Toolbar(board)
    toolbar.setup()
})
