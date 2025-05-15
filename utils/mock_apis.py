from rapidfuzz import process
import json


def get_campaign_analytics(campaign_name: str):
    with open('data/analytics_mock.json', 'r') as f:
        data = json.load(f)
    choices = [campaign['campaign_name'] for campaign in data]
    best_match = process.extractOne(campaign_name, choices)[0]

    return [campaign for campaign in data if campaign['campaign_name'] == best_match]


def get_projects(project_name: str):
    with open('data/project_mock.json', 'r') as f:
        data = json.load(f)
    choices = [project['project_name'] for project in data]
    best_match = process.extractOne(project_name, choices)[0]

    return [project for project in data if project['project_name'] == best_match]