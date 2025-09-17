from typing import Any

from app.agent import agent_manager


async def get_initialized_agent() -> Any:
    """Dependency to ensure agent is initialized before endpoint execution"""
    if not agent_manager.is_initialized():
        await agent_manager.initialize()
    return agent_manager
