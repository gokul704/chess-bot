import requests

from app.core.logging import logger
from app.core.settings import settings


class LLMService:
    def explain_move(self, move_data: dict) -> str | None:
        prompt = (
            "You are a chess coach. Explain this move in 2-3 short sentences, "
            "plain language, no move list.\n"
            f"Position (FEN): {move_data['fen']}\n"
            f"Move played: {move_data['played_move']} "
            f"(classification: {move_data['classification']}, "
            f"centipawn loss: {move_data['centipawn_loss']})\n"
            f"Engine's best move: {move_data['best_move']}\n"
            f"Evaluation before: {move_data['evaluation_before']}, "
            f"after: {move_data['evaluation_after']}"
        )

        try:
            response = requests.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=30,
            )
            response.raise_for_status()
        except requests.RequestException:
            logger.warning("Ollama unavailable, skipping move explanation")
            return None

        return response.json()["response"].strip()
