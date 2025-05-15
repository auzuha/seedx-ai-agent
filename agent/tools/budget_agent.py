from langchain_core.tools import tool
from utils.mock_apis import get_campaign_analytics
from prompt_config import PROMPTS


@tool(name_or_callable='BudgetAgent', description=PROMPTS['v1']['BudgetAgent'])
def budget_agent(campaign_name: str) -> str:
    """
    Calculates key campaign metrics—CTR, conversion rate, cost per click (CPC), cost per acquisition (CPA), total spend, and ROI—for each advertising channel within the campaign. Present these metrics clearly to the user, compare performance across ad spaces, identify the most cost-effective and profitable channel, and recommend where to prioritize budget allocation for the next campaign phase.
    """
    return get_campaign_analytics()