import pytest
from app.services.motivation_service import MotivationService


def test_motivation_messages():
    msg_zero = MotivationService.get_encouragement_message(0.0, 0)
    assert "Ready to learn?" in msg_zero

    msg_part = MotivationService.get_encouragement_message(25.0, 2)
    assert "25.0%" in msg_part

    msg_half = MotivationService.get_encouragement_message(50.0, 5)
    assert "halfway" in msg_half.lower()

    msg_full = MotivationService.get_encouragement_message(100.0, 10)
    assert "100%" in msg_full

