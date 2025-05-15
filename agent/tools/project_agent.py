from langchain_core.tools import tool
from utils.mock_apis import get_projects
from config import PROMPTS

@tool(name_or_callable="ProjectAgent", description=PROMPTS['v1']['ProjectAgent'])
def project_agent():
    """
    Provides project or task status updates for a project.
    Accepts a project_name to find details on the tasks,
    completed work, upcoming deadlines.
    Useful for project tracking and answering status-related questions.
    """
    return get_projects()