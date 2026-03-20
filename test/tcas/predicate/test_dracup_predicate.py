from tcas.state import State 
from tcas.main import altitude_separation_test, non_crossing_biased_climb, non_crossing_biased_descend, positive_ra_alt_thresh

def test_positive_ra_alt_thresh(): 
    # Initialize a baseline scenario object
    scenario = State(
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
    # Verify mapping for index-based thresholds 0 through 3
    assert positive_ra_alt_thresh(scenario, 0) == scenario.positive_ra_alt_thresh_0
    assert positive_ra_alt_thresh(scenario, 1) == scenario.positive_ra_alt_thresh_1
    assert positive_ra_alt_thresh(scenario, 2) == scenario.positive_ra_alt_thresh_2
    assert positive_ra_alt_thresh(scenario, 3) == scenario.positive_ra_alt_thresh_3
    
    # Verify that an invalid index returns the default 0
    assert positive_ra_alt_thresh(scenario, 9) == 0 


def test_non_crossing_biased_climb():
    # Setup for a valid climb bias (upward separation priority)
    climb_priority = State(
        current_vertical_sep=5,
        high_confidence=1,
        two_of_three_reports_valid=1,
        own_tracked_altitude=100,
        own_tracked_alt_rate=0,
        other_tracked_altitude=400,
        altitude_layer_value=1,
        up_separation=350,
        down_separation=0,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0, 
    ) 
    # Setup for an invalid climb bias
    climb_restricted = State(
        current_vertical_sep=5,
        high_confidence=1,
        two_of_three_reports_valid=1,
        own_tracked_altitude=400,
        own_tracked_alt_rate=0,
        other_tracked_altitude=100,
        altitude_layer_value=1,
        up_separation=0,
        down_separation=350,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0, 
    ) 
    # Execute assertions for climb logic
    assert non_crossing_biased_climb(climb_priority) == True
    assert non_crossing_biased_climb(climb_restricted) == False

def test_non_crossing_biased_descend():
    # Setup for a valid descent bias (higher altitude relative to other)
    descend_priority = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=2500,
        own_tracked_alt_rate=0,
        other_tracked_altitude=1000,
        altitude_layer_value=0,
        up_separation=4500,
        down_separation=0,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0, 
    ) 
    # Setup for an invalid descent bias
    descend_restricted = State(
        current_vertical_sep=0,
        high_confidence=0,
        two_of_three_reports_valid=0,
        own_tracked_altitude=1000,
        own_tracked_alt_rate=0,
        other_tracked_altitude=2500,
        altitude_layer_value=0,
        up_separation=0,
        down_separation=1500,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0, 
    ) 
    # Execute assertions for descent logic
    assert non_crossing_biased_descend(descend_priority) == True
    assert non_crossing_biased_descend(descend_restricted) == False

def test_altitude_separation():
    # Case: Upward advisory (Return Code 1)
    rising_intent = State(
        current_vertical_sep=900,
        high_confidence=12,
        two_of_three_reports_valid=1,
        own_tracked_altitude=0,
        own_tracked_alt_rate=0,
        other_tracked_altitude=0,
        altitude_layer_value=0,
        up_separation=120,
        down_separation=240,
        other_rac=0,
        other_capability=1,
        climb_inhibit=0, 
    ) 
    # Case: Neutral/Insignificant (Return Code 0)
    baseline_intent = State(
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
    # Case: Downward advisory (Return Code 2)
    falling_intent = State(
        current_vertical_sep=900,
        high_confidence=12,
        two_of_three_reports_valid=1,
        own_tracked_altitude=0,
        own_tracked_alt_rate=0,
        other_tracked_altitude=0,
        altitude_layer_value=0,
        up_separation=120,
        down_separation=240,
        other_rac=0,
        other_capability=1,
        climb_inhibit=0, 
    ) 
    
    # Validate final decision logic
    assert altitude_separation_test(rising_intent) == 1
    assert altitude_separation_test(baseline_intent) == 0
    assert altitude_separation_test(falling_intent) == 2