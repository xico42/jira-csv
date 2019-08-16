from jira import JIRA
from helper import export_to_csv
import sys
import os
from dotenv import load_dotenv


def main():
    auth = (os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_KEY'))
    jira = JIRA(os.getenv('JIRA_URL'), basic_auth=auth)
    query = open(os.getenv('JIRA_QUERY_FILE')).read()

    issues = jira.search_issues(query, expand='changelog', fields='summary,components,resolutiondate,type,priority')

    output = 'output.csv'
    if len(sys.argv) > 1:
        output = sys.argv[1]

    export_to_csv(issues, output)


if __name__ == '__main__':
    load_dotenv()
    main()
