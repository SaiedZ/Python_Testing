"""Testing data_utils."""

import pytest
from data.data_utils import update_purchases


def test_update_purchases():
    """
    Testing the update_purchases method
    """
    purchases_dict = {"club_0": {"competition_0": 10}}
    update_purchases(purchases_dict, "club_1", "competition_1", 1)
    update_purchases(purchases_dict, "club_0", "competition_0", 12)
    update_purchases(purchases_dict, "club_0", "competition_1", 3)
    expected_dict = {"club_0": {"competition_0": 12, "competition_1":3},
                     "club_1": {"competition_1": 1}
                     }
    assert purchases_dict == expected_dict
    