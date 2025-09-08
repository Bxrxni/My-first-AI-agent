from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import google, noise_cancellation

load_dotenv()

class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a helpful assistant. "
                "If anyone asks 'who created you', 'who made you', or similar, "
                "you must always answer exactly: 'I was created by Baranidharan.'"
            )
        )

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            model="gemini-2.0-flash-exp",
            voice="Puck",
            temperature=0.8,
            instructions="You are a helpful voice AI assistant."
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),  # agent now has instructions
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="Hello! How can I help you today?"
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
