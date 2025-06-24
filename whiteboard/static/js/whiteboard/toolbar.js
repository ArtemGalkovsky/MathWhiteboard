class Toolbar {
    constructor(board, detailsMenu) {
        this._board = board
        this._detailsMenu = detailsMenu

        this._shapesMenu = new ShapesMenu(board)
    }

    setup() {
        this.#setupMenus()

        this._shapesMenu.setup()
    }

    #setupMenus() {
        const menus = document.querySelectorAll(".toolbar_menu")

        let menuButtons = []
        menus.forEach((menu) => {
            const menuButton = menu.parentElement.querySelector(".toolbar_action_menu_button")
            menuButtons.push(menuButton)

            this.#setupMenu(menu, menuButton)
        })

        // document.addEventListener("mousedown", e => {
        //     menuButtons.forEach((menuButton) => {
        //         if (menuButton === e.target) return
        //
        //         menuButton.classList.remove("open")
        //     })
        //
        //     menus.forEach((menu) => {
        //         if (menu === e.target) return
        //
        //         menu.classList.add("hidden")
        //     })
        // })
    }

    #setupMenu(menu, menuButton) {
        if (!menuButton) {
            console.warn(`No menu button [.toolbar_action_menu_button] found for ${menu} in ${menu.parentElement}`)
            return
        }

        menuButton.addEventListener("click", (e) => {
            const isMenuOpened = e.target.classList.contains("open")

            menu.classList.toggle("hidden", isMenuOpened)
            e.target.classList.toggle("open", !isMenuOpened);
        })
    }
}