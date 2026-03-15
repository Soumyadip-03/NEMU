from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import google, noise_cancellation

from prompts import BEHAVIOUR_PROMPT, REPLY_PROMPT
from NEMU_SearchEngine import get_search_tool, get_current_time
from logger import logger, log_user, log_nemu, nemu_thinking

load_dotenv(".env.local")

logger.info("Environment loaded")


# ==============================
# ASSISTANT
# ==============================

class Assistant(Agent):

    def __init__(self) -> None:

        logger.info("Initializing NEMU Assistant")

        super().__init__(
            instructions=BEHAVIOUR_PROMPT,
            tools=[
                get_search_tool(),
                get_current_time
            ]
        )


# ==============================
# SERVER
# ==============================

server = AgentServer()


# ==============================
# RTC SESSION
# ==============================

@server.rtc_session(agent_name="nemu-agent")
async def my_agent(ctx: agents.JobContext):

    logger.info(f"RTC session started | Room: {ctx.room.name}")

    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice="Charon"
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params:
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC(),
            ),
        ),
    )

    logger.info("Agent session started")

    # ==============================
    # USER SPEECH EVENT
    # ==============================

    @session.on("user_speech")
    def on_user_speech(speech):
        log_user(speech.text)
        nemu_thinking()


    # ==============================
    # AGENT SPEECH EVENT
    # ==============================

    @session.on("agent_speech")
    def on_agent_speech(speech):
        log_nemu(speech.text)


    # ==============================
    # START CONVERSATION
    # ==============================

    await session.generate_reply(
        instructions=REPLY_PROMPT
    )


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    logger.info("Starting NEMU Agent Server")

    agents.cli.run_app(server)