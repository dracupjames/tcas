from dataclasses import dataclass


@dataclass
class State:
    current_vertical_sep: int
    high_confidence: int
    two_of_three_reports_valid: int
    own_tracked_altitude: int
    own_tracked_alt_rate: int
    other_tracked_altitude: int
    altitude_layer_value: int
    up_separation: int
    down_separation: int
    other_rac: int
    other_capability: int
    climb_inhibit: int

    positive_ra_alt_thresh_0: int = 16434
    positive_ra_alt_thresh_1: int = 0
    positive_ra_alt_thresh_2: int = 0
    positive_ra_alt_thresh_3: int = 0
