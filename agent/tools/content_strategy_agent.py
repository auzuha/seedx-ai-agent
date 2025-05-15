from langchain_core.tools import tool
from utils.mock_apis import get_projects

@tool
def project_agent(project_name: str) -> str:
    """
    Provides project or task status updates for marketing campaigns.
    Accepts a campaign name or task keyword and returns outstanding tasks, 
    completed work, upcoming deadlines, and responsible team members.
    Useful for project tracking and answering status-related questions.
    """
    data = get_projects(project_name)
    return data