from langchain_core.tools import tool
from utils.mock_apis import get_campaign_analytics

@tool
def budget_agent(campaign_name: str) -> str:
    """
    When given a campaign name, Analyze the metrics, draw conclusions and suggest where to invest in the next phase/ which ad space is most profitable.
    """
    return get_campaign_analytics(campaign_name)