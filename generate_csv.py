from itertools import chain

from jira import JIRA
from helper import export_to_csv
import sys
import os
from dotenv import load_dotenv


def load_issues(jira, query):
    page_number = 0
    page_size = 50
    issues_list = []

    while True:
        start_at = page_number * page_size
        issues = jira.search_issues(query, expand='changelog', fields='summary,components,resolutiondate,type,priority', startAt=start_at, maxResults=page_size)
        issues_list.append(issues)

        if len(issues) == 0:
            break

        page_number += 1

    return chain(*issues_list)


def main():
    auth = (os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_KEY'))
    query = open(os.getenv('JIRA_QUERY_FILE')).read()
    jira = JIRA(os.getenv('JIRA_URL'), basic_auth=auth)

    issues = load_issues(jira, query)

    output = 'output.csv'
    if len(sys.argv) > 1:
        output = sys.argv[1]

    export_to_csv(issues, open(output, mode="w+"))


if __name__ == '__main__':
    load_dotenv()
    main()
