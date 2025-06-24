import {SectionNameElement} from "/static/js/whiteboard/details_menu/section_name_element_creator.js";

const detailsElementsClasses = Object.freeze({
    sectionName: SectionNameElement
})

export class DetailsMenu {
    constructor(board) {
        this._board = board

        this._detailsMenuContainer = document.querySelector("#element_details_menu")
    }

    buildMenu(structureWithCallbacksArray) {
        structureWithCallbacksArray.forEach(data => {
            const detailsElement = this.#createDetailsElement(data)

            structureWithCallbacksArray.callbacks.forEach((callbackData) => {
                detailsElement.addEventListener(callbackData.eventType, callbackData.callback)
            })

            this._detailsMenuContainer.append(detailsElement)
        })
    }

    #createDetailsElement(elementData) {
        if (!detailsElementsClasses.has(elementData.elementName)) {
            throw new Error("Can't find element class to create new element!")
        }

        return detailsElementsClasses[elementData.elementName](elementData).create()
    }
}