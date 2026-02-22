import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from unittest.mock import AsyncMock, patch
import asyncio
import pytest
from bot import TOKEN, CHAT_ID, enviar_mensagem


@pytest.mark.asyncio
async def test_enviar_mensagem():
    msg = 'Olá mundo!'
    with patch('bot.Application') as mock_app_class:
        mock_app = AsyncMock()
        mock_app.bot.send_message = AsyncMock()
        mock_app.shutdown = AsyncMock()

        mock_app_class.builder.return_value.token.return_value.build.return_value = mock_app

        await enviar_mensagem(msg)

        mock_app.bot.send_message.assert_called_once_with(
            chat_id = CHAT_ID,
            text = msg,
            parse_mode = 'HTML'
        )

        mock_app.shutdown.assert_awaited_once()