import {DetailsMenuElement} from "/static/js/whiteboard/details_menu/details_menu_element_creator_class.js";

export class SectionNameElement extends DetailsMenuElement {
    /**
     * Constructs specific DetailsMenuElement [SectionNameElement]
     * @param data - object, which contains headingText
     */
    constructor(data) {
        super(data);
    }

    create() {
        const sectionNameElement = document.createElement("div");
        sectionNameElement.classList.add("details_section_name");

        const headingElement = document.createElement("h3");
        headingElement.classList.add("details_section_name_heading");
        headingElement.textContent = this._data.headingText

        sectionNameElement.append(headingElement);

        return sectionNameElement;
    }
}