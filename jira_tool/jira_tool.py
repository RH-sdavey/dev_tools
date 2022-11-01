import requests
import os


class JiraTool:
    def __init__(self):
        self.url = 'jira_url_here'
        self.session = self.Session(self)
        self.project = self.Project(self.session, "project_here")
        self.issue = self.Issue(self.session)

    class Session:
        def __init__(self, jira):
            self.jira = jira
            self.url = jira.url
            self.api_url = f"{self.url}/rest/api/2"
            self.session = requests.Session()
            self.session.auth = (os.environ['jira_script_user'], os.environ['jira_script_token'])
            self.session.headers = {'Content-Type': 'application/json'}
            self.session.verify = False
            self.session.timeout = 60
            self.session.stream = False

    class Project:
        def __init__(self, session, project):
            self.session = session
            self.url = f"{self.session.api_url}/project"
            self.project = project

        def get(self, project_key):
            url = self.url + '/' + project_key
            response = self.session.session.get(url)
            return response.json()

        def get_all(self):
            url = self.url
            response = self.session.session.get(url)
            return response.json()

        def create_meta(self):
            url = self.url + 'createmeta'
            response = self.session.session.get(url)
            return response.json()

        def get_all_issue_types(self):
            for proj in self.create_meta()['projects']:
                if proj['key'] == self.project:
                    for issue_type in proj['issuetypes']:
                        print(f"{issue_type['name']} - {issue_type['id']} - {issue_type['description']}")

    class Issue:
        def __init__(self, session):
            self.session = session
            self.url = f"{self.session.api_url}/issue/"
            self.comment = self.Comment(self.session)
            self.attachment = self.Attachment(self.session)
            self.worklog = self.Worklog(self.session)
            self.project = self.session.jira.project.project

        def get(self, issue_id):
            url = self.url + issue_id
            response = self.session.session.get(url)
            return response.json()

        def get_type(self, issue_id):
            url = self.url + issue_id
            response = self.session.session.get(url)
            return response.json()['fields']['issuetype']['name']

        def get_all_issue_types(self):
            for proj in self.create_meta()['projects']:
                if proj['key'] == self.project:
                    for issue_type in proj['issuetypes']:
                        print(f"{issue_type['name']} - {issue_type['id']} - {issue_type['description']}")

        def create_meta(self):
            url = self.url + 'createmeta'
            response = self.session.session.get(url)
            return response.json()

        def create(self, data):
            url = self.url
            response = self.session.session.post(url, json=data)
            if response.ok:
                return response.json()
            return Exception(response.text)

        def update(self, issue_id, data):
            url = self.url + issue_id
            response = self.session.session.put(url, json=data)
            return response.status_code

        class Comment:
            def __init__(self, session):
                self.session = session
                self.url = f"{self.session.api_url}/issue/"

            def comment_url_factory(self, issue_id, comment_id=None):
                assert issue_id
                if comment_id:
                    return f"{self.url}/{issue_id}/comment/{comment_id}"
                return f"{self.url}/{issue_id}/comment"

            def get_all(self, issue_id):
                return self.session.session.get(self.comment_url_factory(issue_id)).json()

            def post(self, issue_id, comment):
                return self.session.session.post(self.comment_url_factory(issue_id), json=comment).json()

            def delete(self, issue_id, comment_id):
                return self.session.session.delete(self.comment_url_factory(issue_id, comment_id)).status_code

            def edit(self, issue_id, comment_id, comment):
                return self.session.session.put(self.comment_url_factory(issue_id, comment_id), json=comment).json()

            def get_by_id(self, issue_id, comment_id):
                return self.session.session.get(self.comment_url_factory(issue_id, comment_id)).json()

        class Attachment:
            def __init__(self, session):
                self.session = session
                self.url = session.url + 'rest/api/2/issue/'

            def get_all(self, issue_id):
                url = self.url + issue_id + '/attachment'
                response = self.session.session.get(url)
                return response.json()

            def post(self, issue_id, file_path):
                url = self.url + issue_id + '/attachments'
                headers = {
                    "Content-Type": "multipart/form-data",
                    "X-Atlassian-Token": "nocheck"
                }
                files = {
                    'file': open(file_path, 'rb'),
                }
                response = self.session.session.post(url, headers=headers, files=files)
                return response.status_code

        class Worklog:
            def __init__(self, session):
                self.session = session
                self.url = session.url + 'rest/api/2/issue/'

            def add_worklog(self, issue_id, worklog):
                url = self.url + issue_id + '/worklog'
                response = self.session.session.post(url, data=worklog)
                return response.json()
