const shapesClasses = Object.freeze({
    rectangle: Konva.Rect,
    arc: Konva.Arc,
    ellipse: Konva.Ellipse,
    circle: Konva.Circle,
    line: Konva.Line,
    polygon: Konva.RegularPolygon,
    star: Konva.Star,
    arrow: Konva.Arrow,
})

class ShapesMenu {
    constructor(board) {
        this._board = board

        this._currentUserShapeChoice = null
        this._currentWorkingShape = null

        this._boardPointerDownHandler = this.#pointerDownHandler.bind(this)

        this.#setShapesDefaultParametersField()
    }

    #setShapesDefaultParametersField() {
        const parametersScriptJson = document.querySelector("#default_shapes_json")

        if (!parametersScriptJson) {
            throw new Error(`Unable to set shapesDefault parameters`)
        }

        this._shapesDefaultParameters = JSON.parse(parametersScriptJson.textContent)
    }

    setup() {
        const shapeMenuButtons = document.querySelectorAll(".toolbar_shape_button")

        shapeMenuButtons.forEach((button) => {
            button.addEventListener("click", (e) => {
                this._currentUserShapeChoice = e.target.dataset.shape

                this._board.setBoardEvent("pointerdown", this._boardPointerDownHandler)
            })
        })
    }

    #getDefaultModifiedShape(shapeType, x, y) {
        const shape = this.#getDefaultShape(shapeType)

        shape.draggable(true)

        if (["star", "ellipse", "rectangle", "arc"].includes(shapeType)) {
            shape.x(x)
            shape.y(y)
        } else if (["line", "arrow"].includes(shapeType)) {
            shape.points([x, y, x + 30, y])
        }

        return shape
    }

    #getDefaultShape(shapeType) {
       return new shapesClasses[shapeType](this._shapesDefaultParameters[shapeType])
    }

    #configureShape(shapeObject) {
        shapeObject.on("pointerdown", (e) => {
            this._board.transformer.nodes([e.target])
        })
    }

    #pointerDownHandler(e) {
        console.log(e)

        this._currentWorkingShape = this.#getDefaultModifiedShape(this._currentUserShapeChoice, e.layerX, e.layerY)
        console.log(this._currentWorkingShape)
        if (!this._currentWorkingShape) {
            this._board.setBoardEvent("pointerdown", this._boardPointerDownHandler)
            return
        }

        this.#configureShape(this._currentWorkingShape)

        this._board.addShapeToStage(this._currentWorkingShape)
        this._board.transformer.nodes([this._currentWorkingShape])

        this._board.removeBoardEvent("pointerdown", this._boardPointerDownHandler)
    }
}