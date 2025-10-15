from src.scenarios import get_scenario

def test_car_following_scene():
    v1, v2, env = get_scenario("car_following")

    print("V1 Pos:", v1.g, "Speed:", v1.v)
    print("V2 Pos:", v2.g, "Speed:", v2.v)
    print("Enviorment Information:", env)

if __name__ == "__main__":
    test_car_following_scene()