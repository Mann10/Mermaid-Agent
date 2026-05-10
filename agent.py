import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from langchain.messages import SystemMessage
from typing import Callable

from skills import SKILLS, Skill
from mermaid_tool import generate_mermaid_diagram


load_dotenv(override=True)


llm = ChatOpenAI(
    base_url=os.getenv("LITELLM_API_BASE"),
    api_key=os.getenv("LITELLM_API_KEY"),
    model="ministral-3:latest",
    temperature=0.2,
)


@tool
def load_skill(skill_name: str) -> str:
    """
    Load the full content of a skill into the agent's context.

    Use this when you need detailed syntax rules for a specific task.

    Args:
        skill_name: The name of the skill to load (e.g., "mermaid-diagrams")
    """
    for skill in SKILLS:
        if skill["name"] == skill_name:
            return f"Loaded skill: {skill_name}\n\n{skill['content']}"

    available = ", ".join(s["name"] for s in SKILLS)
    return f"Skill '{skill_name}' not found. Available skills: {available}"


class SkillMiddleware(AgentMiddleware):
    """Middleware that injects skill descriptions into the system prompt."""

    tools = [load_skill]

    def __init__(self):
        skills_list = [
            f"- **{skill['name']}**: {skill['description']}"
            for skill in SKILLS
        ]
        self.skills_prompt = "\n".join(skills_list)

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        skills_addendum = (
            f"\n\n## Available Skills\n\n{self.skills_prompt}\n\n"
            "Use the load_skill tool when you need detailed information "
            "about handling a specific type of request."
        )

        new_content = list(request.system_message.content_blocks) + [
            {"type": "text", "text": skills_addendum}
        ]
        new_system_message = SystemMessage(content=new_content)
        modified_request = request.override(system_message=new_system_message)
        return handler(modified_request)


SYSTEM_PROMPT = """You are a diagram assistant that creates Mermaid diagrams from user descriptions.

You have access to a tool that validates and formats Mermaid diagram code.
Before writing any Mermaid code, you MUST load the mermaid-diagrams skill
so you know the correct syntax for the requested diagram type.

Rules:
- Load the skill first, then generate the code, then call the tool.
- If validation fails, reload the skill and fix the errors.
- Present the final diagram code to the user in a format they can copy into any Mermaid viewer.
- Do not explain the syntax unless the user asks.
"""


agent = create_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    middleware=[SkillMiddleware()],
    tools=[generate_mermaid_diagram],
)


if __name__ == "__main__":
    print("=" * 50)
    print("Welcome to the Mermaid Diagram Agent!")
    print("I am the mermaid diagram agent.")
    print("I create beautiful Mermaid diagrams from your descriptions.")
    print("I provide you mermaid code that you can use in any mermaid viewer online.")
    print("=" * 50)
    print("\nCommands:")
    print("  - Enter your diagram description to generate a diagram")
    print("  - Type 'q' to quit")
    print("  - Press Ctrl+C to exit\n")

    try:
        while True:
            user_input = input("You: ").strip()

            if not user_input or user_input.lower() == "q":
                print("Goodbye!")
                break

            input_message = {
                "role": "user",
                "content": user_input,
            }

            for step in agent.stream(
                {"messages": [input_message]},
                stream_mode="values",
            ):
                step["messages"][-1].pretty_print()

    except KeyboardInterrupt:
        print("\n\nAgent interrupted. Goodbye!")