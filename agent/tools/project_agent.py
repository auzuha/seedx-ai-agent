from langchain_core.tools import tool


@tool
def project_agent(name: str) -> str:
    """
    Function to get analytical details/ business metrics for the company.
    """
    pass
    return f"For project {name}, 8 tasks remaining, 70% overall complete."