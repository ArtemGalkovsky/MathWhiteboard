class Board {
    constructor(boardContainer) {
        this._boardContainer = boardContainer

        this._stage = null
    }

    setup() {
        this._stage = new Konva.Stage(
            {
                container: this._boardContainer,
            }
        )

        this.#__set_window_resize_handler()
        this.#__resize()
    }

    #__resize() {
        if (!this._stage) throw new Error("Board is not initialized! Use 'setup' method before calling this method!")

        const boundingRect = this._boardContainer.getBoundingClientRect()

        this._stage.width(boundingRect.width)
        this._stage.height(boundingRect.height)
    }

    #__set_window_resize_handler() {
        window.addEventListener('resize', this.#__resize.bind(this))
    }
}