from .car_following import init_scene as car_following

SCENARIOS = {
    "car_following": car_following,
    # "intersection_turn": intersection_turn,
    # "hypothetical": hypothetical,
}


def get_scenario(name: str):
    if name not in SCENARIOS:
        raise ValueError(f"Unkown Scenario: {name}")
    return SCENARIOS[name]()