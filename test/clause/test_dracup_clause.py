from tcas.state import State 
from tcas.main import altitude_separation_test, non_crossing_biased_climb, non_crossing_biased_descend, positive_ra_alt_thresh

def test_positive_ra_alt_thresh():
    # Setup a configuration for threshold validation
    config_state = State(
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
    # Valid Case: layer index is within the supported range (0-4)
    assert positive_ra_alt_thresh(config_state, 0) == config_state.positive_ra_alt_thresh_0
    
    # Invalid Case: layer index is outside the recognized range
    assert positive_ra_alt_thresh(config_state, 8) == 0


def test_non_crossing_biased_climb():
    # Setup state for biased climb evaluation
    climb_state = State(
        current_vertical_sep=15,
        high_confidence=1,
        two_of_three_reports_valid=1,
        own_tracked_altitude=250,
        own_tracked_alt_rate=0,
        other_tracked_altitude=500,
        altitude_layer_value=1,
        up_separation=450,
        down_separation=50,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0, 
    ) 
    # True Case: biased climb inhibition check passes against down_separation
    assert non_crossing_biased_climb(climb_state) == True
    
    # Reset for False Case: Adjusting down_separation to exceed the biased threshold
    climb_state.down_separation = 1000
    assert non_crossing_biased_climb(climb_state) == False

def test_non_crossing_biased_descend():
    # Setup state for biased descent evaluation
    descend_state = State(
        current_vertical_sep=10,
        high_confidence=1,
        two_of_three_reports_valid=1,
        own_tracked_altitude=800,
        own_tracked_alt_rate=0,
        other_tracked_altitude=300,
        altitude_layer_value=1,
        up_separation=2000,
        down_separation=100,
        other_rac=0,
        other_capability=0,
        climb_inhibit=0, 
    ) 
    # True Case: biased descent logic holds against up_separation
    assert non_crossing_biased_descend(descend_state) == True
    
    # False Case: up_separation is now the dominant factor
    descend_state.up_separation = 50 
    assert non_crossing_biased_descend(descend_state) == False

def test_altitude_separation():
    # Initialize state for final separation logic
    separation_env = State(
        current_vertical_sep=750,
        high_confidence=1,
        two_of_three_reports_valid=1,
        own_tracked_altitude=1000,
        own_tracked_alt_rate=600,
        other_tracked_altitude=1200,
        altitude_layer_value=1,
        up_separation=300,
        down_separation=300,
        other_rac=0,
        other_capability=1,
        climb_inhibit=0, 
    ) 
    # Result 0: Criteria met for default separation status
    assert altitude_separation_test(separation_env) == 0
    
    # Result 2: Conditions trigger a downward Resolution Advisory (RA)
    # (Achieved here by modifying state to make downward the safer path)
    separation_env.down_separation = 800
    assert altitude_separation_test(separation_env) == 2 
    
    # Result 1: Conditions trigger an upward Resolution Advisory (RA)
    separation_env.up_separation = 900
    assert altitude_separation_test(separation_env) == 1