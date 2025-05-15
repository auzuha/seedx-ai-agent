from langchain_core.tools import tool
from utils.mock_apis import get_campaign_analytics
from prompt_config import PROMPTS

@tool(name_or_callable='AnalyticsAgent', description=PROMPTS['v1']['AnalyticsAgent'])
def analytics_agent():
    """
    Provides marketing analytics based for recent campaigns.
    """
    return get_campaign_analytics()
    