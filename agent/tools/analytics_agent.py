from langchain_core.tools import tool



@tool
def analytics_agent(query: str) -> str:
    """
    Function to get analytical details/ business metrics for the company.
    """
    pass
    return f"The summary is 50% ROI, 30% more engagement"