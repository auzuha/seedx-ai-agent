import json


def get_campaign_analytics():
    with open('data/analytics_mock.json', 'r') as f:
        data = json.load(f)
    return data


def get_projects():
    with open('data/project_mock.json', 'r') as f:
        data = json.load(f)
    return data