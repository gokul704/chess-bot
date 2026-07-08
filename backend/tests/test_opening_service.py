import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.opening_service import OpeningService


def test_detects_known_opening():
    service = OpeningService()
    fen = "rn1qkbnr/ppp2ppp/8/3pp3/5P2/6Pb/PPPPP2P/RNBQKB1R w KQkq - 0 4"

    result = service.detect_opening(fen)

    assert result is not None
    assert result["name"] == "Amar Opening: Paris Gambit"


def test_detects_via_transposed_move_counters():
    service = OpeningService()
    fen = "rn1qkbnr/ppp2ppp/8/3pp3/5P2/6Pb/PPPPP2P/RNBQKB1R w KQkq - 5 12"

    result = service.detect_opening(fen)

    assert result is not None
    assert result["name"] == "Amar Opening: Paris Gambit"


def test_unknown_position_returns_none():
    service = OpeningService()
    fen = "8/8/8/8/8/8/8/k1K5 w - - 0 1"

    assert service.detect_opening(fen) is None


if __name__ == "__main__":
    test_detects_known_opening()
    test_detects_via_transposed_move_counters()
    test_unknown_position_returns_none()
    print("OK")
