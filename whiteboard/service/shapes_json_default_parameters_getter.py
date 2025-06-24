def get_shapes_default_parameters() -> dict:
    parameters = {
        "rectangle": {"strokeScaleEnabled": True},
        "line": {"width": 1},
        "star": {"innerRadius": 5, "outerRadius": 10, "numPoints": 5},
        "arc": {"angle": 30, "clockwise": False, "innerRadius": 5, "outerRadius": 7},
        "arrow": {"width": 1},
        "ellipse": {"radius": {"x": 5, "y": 6}},
    }

    for param in parameters:
        parameters[param]["fill"] = "yellow"
        parameters[param]["stroke"] = "black"

    return parameters