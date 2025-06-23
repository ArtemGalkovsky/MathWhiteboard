class Board {
    constructor(boardContainer) {
        this._boardContainer = boardContainer

        this._currentWorkingShape = null
        this._currentUserShapeChoice = null

        this._stage = new Konva.Stage(
            {
                container: this._boardContainer,
            }
        )
        this._boardElement = boardContainer.querySelector(".konvajs-content")

        this._currentLayer = new Konva.Layer()
        this._stage.add(this._currentLayer)

        this._transformer = new Konva.Transformer()
        this._currentLayer.add(this._transformer)
    }

    get transformer() {
        return this._transformer
    }

    setup() {
        this.#setWindowResizeHandler()
        this.#resize()

        this.#setDragAndDropToStage()
    }

    setBoardEvent(eventType, func) {
        this._boardElement.addEventListener(eventType, func)
    }

    removeBoardEvent(eventType, func) {
        this._boardElement.removeEventListener(eventType, func)
    }

    addShapeToStage(shape) {
        this._currentLayer.add(shape)
    }

    #setDragAndDropToStage() {
        this._boardContainer.addEventListener("dragenter", e => e.preventDefault())
        this._boardContainer.addEventListener("dragover", e => e.preventDefault())

        this._boardContainer.addEventListener("drop", e => {
            e.preventDefault()
        })
    }

    #resize() {
        const boundingRect = this._boardContainer.getBoundingClientRect()

        this._stage.width(boundingRect.width)
        this._stage.height(boundingRect.height)
    }

    #setWindowResizeHandler() {
        window.addEventListener('resize', this.#resize.bind(this))
    }
}