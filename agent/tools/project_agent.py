from langchain_core.tools import tool
from utils.mock_apis import get_projects

@tool
def project_agent(project_name: str) -> str:
    """
    Provides project or task status updates for a project.
    Accepts a project_name to find details on the tasks,
    completed work, upcoming deadlines.
    Useful for project tracking and answering status-related questions.
    """
    data = get_projects(project_name)
    return data