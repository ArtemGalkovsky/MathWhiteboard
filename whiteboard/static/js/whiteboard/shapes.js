class ShapesMenu {
    constructor(board) {
        this._board = board

        this._currentUserShapeChoice = null
        this._currentWorkingShape = null

        this._boardPointerDownHandler = this.#pointerDownHandler.bind(this)
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
        shape.stroke("black")
        shape.fill("yellow")
        shape.strokeScaleEnabled(false)

        if (["star", "ellipse", "rectangle", "arc"].includes(shapeType)) {
            shape.x(x)
            shape.y(y)
        } else if (["line", "arrow"].includes(shapeType)) {
            shape.points([x, y, x + 30, y])
        }

        if (["rectangle"].includes(shapeType)) {
            shape.width(30)
            shape.height(30)
        }

        return shape
    }

    #getDefaultShape(shapeType) {
        switch (shapeType) {
            case "ellipse":
                return new Konva.Ellipse({
                    radiusX: 10,
                    radiusY: 10,
                })
            case "line":
                return new Konva.Line({
                    width: 1,
                })
            case "star":
                return new Konva.Star({
                    innerRadius: 5,
                    outerRadius: 10,
                    numPoints: 5,
                })
            case "rectangle":
                return new Konva.Rect({})
            case "arc":
                return new Konva.Arc({
                    angle: 30,
                    clockwise: false,
                    innerRadius: 5,
                    outerRadius: 10,
                })
            case "arrow":
                return new Konva.Arrow({})
        }
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