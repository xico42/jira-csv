import csv
from datetime import datetime


def create_date(datestr):
    return datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S.%f%z')


def get_status_changelog(issue, to_status='DEVELOPMENT'):
    changes = (
        (create_date(hist.created), item)
        for hist in issue.changelog.histories for item in hist.items
        if item.field == 'status' and item.toString == to_status
    )
    return sorted(changes, key=lambda c: c[0])


def get_start_date(issue):
    changelog = get_status_changelog(issue)
    if len(changelog) > 0:
        return format_date(changelog[0][0])


def format_date(date):
    return date.strftime('%Y-%m-%d')


def generate_row(issue):
    class_of_service = 'Normal'
    if issue.fields.priority.name == 'Hotfix':
        class_of_service = 'Hot-fix'
    if issue.key.startswith('SD'):
        class_of_service = 'Expedite'

    issue_type = issue.fields.issuetype.name
    if issue_type == 'Story':
        issue_type = 'Value'

    start_date = get_start_date(issue)
    resolution_date = format_date(create_date(issue.fields.resolutiondate))
    components = ','.join([c.name for c in issue.fields.components])

    return [components, issue.key, issue.fields.summary, issue_type, class_of_service, start_date, resolution_date]


def export_to_csv(issues, file):
    rows = [generate_row(issue) for issue in sorted(issues, key=lambda issue: create_date(issue.fields.resolutiondate))]

    csv.register_dialect('myDialect',
                         quoting=csv.QUOTE_ALL,
                         skipinitialspace=True)

    # with open(file, 'w+') as csv_file:
    writer = csv.writer(file, dialect='myDialect', lineterminator='\n')
    writer.writerows(rows)
    file.flush()
