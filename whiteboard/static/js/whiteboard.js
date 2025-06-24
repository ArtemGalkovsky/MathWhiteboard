import {DetailsMenu} from "/static/js/whiteboard/details_menu.js";

document.addEventListener("DOMContentLoaded", () => {
    const boardContainer = document.querySelector("#canvas_container");

    const board = new Board(boardContainer)
    board.setup()

    const detailsMenu = new DetailsMenu(board)

    const toolbar = new Toolbar(board, detailsMenu)
    toolbar.setup()
})
