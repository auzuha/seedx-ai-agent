PROMPTS = {
    'v1': 
        {
        "ProjectAgent": """
        Provides project or task status updates for a project.
        Accepts a project_name to find details on the tasks,
        completed work, upcoming deadlines.
        Useful for project tracking and answering status-related questions.
        """,


        "BudgetAgent": """
        Calculates key campaign metrics—CTR, conversion rate, cost per click (CPC), cost per acquisition (CPA), total spend, and ROI—for each advertising channel within the campaign. Present these metrics clearly to the user, compare performance across ad spaces, identify the most cost-effective and profitable channel, and recommend where to prioritize budget allocation for the next campaign phase.
        """,


        "AnalyticsAgent": """
        Provides marketing analytics based for recent campaigns.
        """
        }

}


MODEL = 'gpt-4o'