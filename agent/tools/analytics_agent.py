from langchain_core.tools import tool
from utils.mock_apis import get_campaign_analytics


@tool
def analytics_agent(campaign_name: str) -> str:
    """
    Provides marketing analytics based on recent campaign data. 
    Accepts a campaign name or query and returns KPIs such as click-through rate (CTR),
    conversion rate, cost per conversion, and ROI. Useful for analyzing campaign performance 
    or generating summaries of multiple campaigns.
    """
    data = get_campaign_analytics(campaign_name)
    return data