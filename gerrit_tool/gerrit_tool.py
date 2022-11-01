import json
import os
import requests

HEADERS = {'Content-Type': 'application/json'}


class GerritTool:
    """This class is used to interact with the Gerrit API.

    Create an instance with the desired gerrit instance. For example:
        my_gerrit = GerritTool()

    Use the structured class methods to interact with the API. For example:
        get a list of all projects:
            my_gerrit.project.list()

        see if a branch is mergeable into master:
            my_gerrit.project.branch.mergeable('dcp_tests', 'my_branch')
    
        assign a topic to a change:
            my_gerrit.change.topic.set('<change_id>', '<my_topic>')

        remove a reviewer from a change:
            my_gerrit.change.reviewer.delete('<change_id>', '<reviewer_email|id|name>')
    """
    def __init__(self):
        self._url = 'gerrit_url_here'
        self.username = os.environ['gerrit_script_user']
        self.password = os.environ['gerrit_script_token']
        self.auth = (self.username, self.password)
        self.server = self.Server(self)
        self.group = self.Group(self)
        self.account = self.Account(self)
        self.project = self.Project(self)
        self.change = self.Change(self)
        self.documentation = self.Documentation(self)

    def get_and_clean(self, endpoint):
        print("GET request to: " + self._url + endpoint)
        try:
            return json.loads(requests.get(self._url + endpoint, auth=self.auth).text[5:])
        except Exception as e:
            print("Error with returned JSON:")
            print(f"Exception text: " + str(e))
            print(f"Request reply" + str(e))
            return None

    def post(self, endpoint, data=None):
        if data is None:
            data = {}
        try:
            return requests.post(self._url + endpoint, auth=self.auth, data=data, headers=HEADERS)
        except Exception as e:
            print("Error with POSTING JSON: " + str(e))

    def put(self, endpoint, data):
        try:
            return requests.put(self._url + endpoint, auth=self.auth, data=data, headers=HEADERS)
        except Exception as e:
            print("Error with PUTTING JSON: " + str(e))

    def delete(self, endpoint):
        try:
            return requests.delete(self._url + endpoint, auth=self.auth)
        except Exception as e:
            print("Error with DELETING JSON: " + str(e))

    class Server:
        def __init__(self, gerrit_instance):
            self.gerrit_instance = gerrit_instance
            self.cache = self.Cache(self.gerrit_instance)
            self.tasks = self.Tasks(self.gerrit_instance)
            self.plugins = self.Plugins(self.gerrit_instance)

        def version(self):
            return self.gerrit_instance.get_and_clean("/a/config/server/version")

        def info(self):
            return self.gerrit_instance.get_and_clean("/a/config/server/info")

        def state_summary(self):
            return self.gerrit_instance.get_and_clean("/a/config/server/summary")

        def capabilities(self):
            return self.gerrit_instance.get_and_clean("/a/config/server/capabilities")

        def top_menus(self):
            return self.gerrit_instance.get_and_clean("/a/config/server/top-menus")

        def default_user_preferences(self):
            return self.gerrit_instance.get_and_clean("/a/config/server/preferences")

        class Cache:
            """
            The caller must be a member of a group that is granted one of the following capabilities:
                View Caches
                Maintain Server
                Administrate Server
            """
            def __init__(self, gerrit_instance):
                self.gerrit_instance = gerrit_instance

            def list(self):
                return self.gerrit_instance.get_and_clean("/a/config/server/caches")

            def get(self, cache_name):
                return self.gerrit_instance.get_and_clean(f"/a/config/server/caches/{cache_name}")

            def flush_all(self):
                return self.gerrit_instance.post("/a/config/server/caches/", data={"operation": "FLUSH_ALL"})

            def flush(self, cache_name):
                return self.gerrit_instance.post(f"/a/config/server/caches/{cache_name}/flush")

        class Tasks:
            """
            The caller must be a member of a group that is granted one of the following capabilities:
                View Queue
                Maintain Server
                Administrate Server
            """
            def __init__(self, gerrit_instance):
                self.gerrit_instance = gerrit_instance

            def list(self):
                return self.gerrit_instance.get_and_clean("/a/config/server/tasks")

            def get(self, task_name):
                return self.gerrit_instance.get_and_clean(f"/a/config/server/tasks/{task_name}")

            def delete(self, task_name):
                return self.gerrit_instance.delete(f"/a/config/server/tasks/{task_name}")

        class Plugins:
            def __init__(self, gerrit_instance):
                self.gerrit_instance = gerrit_instance

            def list(self):
                return self.gerrit_instance.get_and_clean("/a/plugins")

            def status(self, plugin_name):
                return self.gerrit_instance.get_and_clean(f"/a/plugins/{plugin_name}/gerrit~status")

    class Group:
        def __init__(self, gerrit_instance):
            self.gerrit_instance = gerrit_instance

        def list(self):
            return self.gerrit_instance.get_and_clean("/a/groups")

        def get(self, group_name, detailed=False):
            details = "/" if detailed is False else "/detail"
            return self.gerrit_instance.get_and_clean(f"/a/groups/{group_name}{details}")

        def description(self, group_name):
            return self.gerrit_instance.get_and_clean(f"/a/groups/{group_name}/description")

        def options(self, group_name):
            return self.gerrit_instance.get_and_clean(f"/a/groups/{group_name}/options")

        def owner(self, group_name):
            return self.gerrit_instance.get_and_clean(f"/a/groups/{group_name}/owner")

        def audit_log(self, group_name):
            return self.gerrit_instance.get_and_clean(f"/a/groups/{group_name}/log.audit")

        def members(self, group_name):
            return self.gerrit_instance.get_and_clean(f"/a/groups/{group_name}/members")

    class Account:
        def __init__(self, gerrit_instance):
            self.gerrit = gerrit_instance

        def get(self, user, detailed=False):
            details = '/' if not detailed else '/detail'
            return self.gerrit.get_and_clean(f'/a/accounts/{user}{details}')

        def groups(self, user):
            return self.gerrit.get_and_clean(f'/a/accounts/{user}/groups')

        def projects(self, user):
            return self.gerrit.get_and_clean(f'/a/accounts/{user}/projects')

        def self_ssh_keys(self):
            return self.gerrit.get_and_clean(f'/a/accounts/self/sshkeys')

        def capabilities(self, user):
            return self.gerrit.get_and_clean(f'/a/accounts/{user}/capabilities')

        def self_capabilities(self):
            return self.gerrit.get_and_clean(f'/a/accounts/self/capabilities')

    class Project:
        def __init__(self, gerrit_instance):
            self.gerrit = gerrit_instance
            self.branch = self.Branch(self.gerrit)
            self.tag = self.Tag(self.gerrit)
            self.dashboard = self.DashBoard(self.gerrit)

        def list(self):
            return self.gerrit.get_and_clean('/a/projects')

        def get(self, project_name):
            return self.gerrit.get_and_clean(f'/a/projects/{project_name}')

        def description(self, project_name):
            return self.gerrit.get_and_clean(f'/a/projects/{project_name}/description')

        def parent(self, project_name):
            return self.gerrit.get_and_clean(f'/a/projects/{project_name}/parent')

        def head(self, project_name):
            return self.gerrit.get_and_clean(f'/a/projects/{project_name}/HEAD')

        def statistics(self, project_name):
            """'Capability runGC is required to access this resource'"""
            return self.gerrit.get_and_clean(f'/a/projects/{project_name}/statistics.git')

        def config(self, project_name):
            return self.gerrit.get_and_clean(f'/a/projects/{project_name}/config')

        def access_rights(self, project_name):
            return self.gerrit.get_and_clean(f'/a/projects/{project_name}/access')

        class Branch:
            def __init__(self, gerrit_instance):
                self.gerrit = gerrit_instance

            def list(self, project_name):
                return self.gerrit.get_and_clean(f'/a/projects/{project_name}/branches')

            def get(self, project_name, branch_name):
                return self.gerrit.get_and_clean(f'/a/projects/{project_name}/branches/{branch_name}')

            def create(self, project_name, branch_name):
                return self.gerrit.put(f'/a/projects/{project_name}/branches/{branch_name}')

            def delete(self, project_name, branch_name):
                return self.gerrit.delete(f'/a/projects/{project_name}/branches/{branch_name}')

            def mergeable(self, project_name, branch_name):
                return self.gerrit.get_and_clean(f'/a/projects/{project_name}/branches/{branch_name}/mergeable')

            def reflog(self, project_name, branch_name):
                return self.gerrit.get_and_clean(f'/a/projects/{project_name}/branches/{branch_name}/reflog')

        class Tag:
            def __init__(self, gerrit_instance):
                self.gerrit = gerrit_instance

            def list(self, project_name):
                return self.gerrit.get_and_clean(f'/a/projects/{project_name}/tags')

            def get(self, project_name, tag_name):
                return self.gerrit.get_and_clean(f'/a/projects/{project_name}/tags/{tag_name}')

            def delete(self, project_name, tag_name):
                return self.gerrit.delete(f'/a/projects/{project_name}/tags/{tag_name}')

        class DashBoard:
            def __init__(self, gerrit_instance):
                self.gerrit = gerrit_instance

            def list(self, project_name):
                return self.gerrit.get_and_clean(f'/a/projects/{project_name}/dashboards')

            def get(self, project_name, dashboard_name):
                return self.gerrit.get_and_clean(f'/a/projects/{project_name}/dashboards/{dashboard_name}')

            def create(self, project_name, dashboard_name):
                return self.gerrit.put(f'/a/projects/{project_name}/dashboards/{dashboard_name}')

            def delete(self, project_name, dashboard_name):
                return self.gerrit.delete(f'/a/projects/{project_name}/dashboards/{dashboard_name}')

    class Change:
        def __init__(self, gerrit_instance):
            self.gerrit = gerrit_instance
            self.topic = self.Topic(self.gerrit)
            self.assignee = self.Assignee(self.gerrit)
            self.comment = self.Comment(self.gerrit)
            self.reviewer = self.Reviewer(self.gerrit)
            self.file = self.File(self.gerrit)

        def get_by_query(self, query):
            return self.gerrit.get_and_clean(f'/a/changes/?q={query}')

        def get_by_id(self, change_id, detailed=False):
            details = '/' if not detailed else '/detail'
            return self.gerrit.get_and_clean(f'/a/changes/{change_id}{details}')

        def get_by_change_num(self, change_num, detailed=False):
            details = '/' if not detailed else '/detail'
            return self.gerrit.get_and_clean(f'/a/changes/{change_num}{details}')

        def get_edit_details(self, change_id):
            return self.gerrit.get_and_clean(f'/a/changes/{change_id}/edit')

        # def abandon(self, change_id):
        #     return self.gerrit.POST_request(f'/a/changes/{change_id}/abandon')
        #
        # def publish_draft(self, change_id):
        #     return self.gerrit.POST_request(f'/a/changes/{change_id}/publish')

        class Assignee:
            def __init__(self, gerrit_instance):
                self.gerrit = gerrit_instance

            def get(self, change_id):
                return self.gerrit.get_and_clean(f'/a/changes/{change_id}/assignee')

            def set(self, change_id, assignee):
                return self.gerrit.put(f'/a/changes/{change_id}/assignee', json.dumps(assignee))

        class Topic:
            def __init__(self, gerrit_instance):
                self.gerrit = gerrit_instance

            def get(self, change_id):
                return self.gerrit.get_and_clean(f'/a/changes/{change_id}/topic')

            def set(self, change_id, topic):
                return self.gerrit.put(f'/a/changes/{change_id}/topic', json.dumps(topic))

            def delete(self, change_id):
                return self.gerrit.delete(f'/a/changes/{change_id}/topic')

        class Comment:
            def __init__(self, gerrit_instance):
                self.gerrit = gerrit_instance

            def get(self, change_id):
                return self.gerrit.get_and_clean(f'/a/changes/{change_id}/comments')

            def get_by_id(self, change_id, comment_id):
                return self.gerrit.get_and_clean(f'/a/changes/{change_id}/comments/{comment_id}')

        class Reviewer:
            def __init__(self, gerrit_instance):
                self.gerrit = gerrit_instance

            def get(self, change_id):
                return self.gerrit.get_and_clean(f'/a/changes/{change_id}/reviewers')

            def suggest(self, change_id):
                return self.gerrit.get_and_clean(f'/a/changes/{change_id}/suggest_reviewers?')

            def add(self, change_id, reviewer):
                return self.gerrit.post(f'/a/changes/{change_id}/reviewers', json.dumps(reviewer))

            def delete(self, change_id, reviewer):
                return self.gerrit.post(f'/a/changes/{change_id}/reviewers/{reviewer}/delete')

        class File:
            def __init__(self, gerrit_instance):
                self.gerrit = gerrit_instance

            def get(self, change_id, revision_id):
                return self.gerrit.get_and_clean(f'/a/changes/{change_id}/revisions/{revision_id}/files')

    class Documentation:
        def __init__(self, gerrit_instance):
            self.gerrit = gerrit_instance

        def query(self, keyword):
            return self.gerrit.get_and_clean(f'/a/Documentation/?q={keyword}')
