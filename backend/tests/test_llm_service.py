import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.llm_service import LLMService

MOVE_DATA = {
    "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
    "played_move": "e7e6",
    "best_move": "e7e5",
    "evaluation_before": 30,
    "evaluation_after": 25,
    "centipawn_loss": 55,
    "classification": "Inaccuracy",
}


def test_returns_stripped_response_text():
    fake_response = Mock()
    fake_response.raise_for_status = Mock()
    fake_response.json.return_value = {"response": "  Good developing move.  "}

    with patch("app.services.llm_service.requests.post", return_value=fake_response) as post:
        result = LLMService().explain_move(MOVE_DATA)

    assert result == "Good developing move."
    _, kwargs = post.call_args
    assert kwargs["json"]["stream"] is False
    assert MOVE_DATA["played_move"] in kwargs["json"]["prompt"]


def test_returns_none_when_ollama_unreachable():
    import requests

    with patch("app.services.llm_service.requests.post", side_effect=requests.ConnectionError()):
        result = LLMService().explain_move(MOVE_DATA)

    assert result is None


if __name__ == "__main__":
    test_returns_stripped_response_text()
    test_returns_none_when_ollama_unreachable()
    print("OK")
