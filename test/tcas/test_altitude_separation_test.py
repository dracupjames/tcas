from tcas.main import altitude_separation_test
from tcas.state import State


def test():
    state = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=0,
        own_tracked_alt_rate=0,
        other_tracked_altitude=0,
        altitude_layer_value=0,
        up_separation=0,
        down_separation=0,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0,
    )

    expected = 0

    actual = altitude_separation_test(state)

    assert actual == expected
