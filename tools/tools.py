from langchain_core.tools import tool



@tool
def analytics_agent(query: str) -> str:
    """
    Function to get analytical details/ business metrics for the company.
    """
    pass
    return f"The summary is 50% ROI, 30% more engagement"

@tool
def project_agent(name: str) -> str:
    """
    Function to get details about the projects.
    Args: name[str] -> the name of the project
    """

    return f"for {name}, 3 tasks remaining, project 80% complete"