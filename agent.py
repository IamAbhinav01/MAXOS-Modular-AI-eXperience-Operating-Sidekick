from dotenv import load_dotenv
from livekit.plugins import google
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from tools import get_news,get_stock_price,describe_clipboard,search,tell_news
from prompt import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from livekit.plugins import (
    google,
    noise_cancellation,
)

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTION,tools=[get_stock_price,get_news,describe_clipboard,search,tell_news])

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice="Puck",
            temperature=0.8
        ),
    )
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    
    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))