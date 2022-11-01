import json
import pathlib
import webbrowser
from datetime import date
from time import sleep

import urllib3

from .StrategyExecutor import Strategy
from signal import signal, SIGINT

__all__ = [
    'Test', 'ViewHealthReport', 'AllJobsInView', 'CloneJob', 'BuildJob',
    'JobInfo', 'JobHealthReport',
    'LastBuildConsoleOutput', 'PullBuildArtifactsAndRobotReports', 'PullACCxDEVANYTESTBuildArtifacts'
 ]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Test(Strategy):
    """Get info for user executing the script, used as a convenience method for testing"""

    def __init__(self):
        super().__init__()

    def execute(self):
        return self.jenkins_tool.user.get_user_details()


class ViewHealthReport(Strategy):
    """Get view_name health report"""

    def __init__(self, view_name):
        super().__init__()
        self.view_name = view_name

    def execute(self):
        return [
            self.jenkins_tool.server.jobs.health_report(job['name'])
            for job in self.jenkins_tool.server.jobs.all_by_view_name(self.view_name)
            if 'healthReport' in self.jenkins_tool.server.jobs.info_by_name(job['name'])
        ]


class AllJobsInView(Strategy):
    """Get all jobs in view_name"""

    def __init__(self, view_name):
        super().__init__()
        self.view_name = view_name

    def execute(self):
        return self.jenkins_tool.server.jobs.all_by_view_name(self.view_name)


class CloneJob(Strategy):
    """Clone job_name to cloned_name"""

    def __init__(self, job_name, cloned_name):
        super().__init__()
        self.job_name = job_name
        self.cloned_name = cloned_name

    def execute(self):
        self.jenkins_tool.server.jobs.copy(self.job_name, self.cloned_name)


class BuildJob(Strategy):
    """Build job_name"""

    def __init__(self, job_name):
        super().__init__()
        self.job_name = job_name

    def execute(self):
        self.jenkins_tool.server.jobs.trigger_build_by_name(self.job_name)


class JobInfo(Strategy):
    """Get job_name info"""

    def __init__(self, job_name):
        super().__init__()
        self.job_name = job_name

    def execute(self):
        return self.jenkins_tool.server.jobs.info_by_name(self.job_name)


class JobHealthReport(Strategy):
    """Get job_name health report"""

    def __init__(self, job_name):
        super().__init__()
        self.job_name = job_name

    def execute(self):
        return self.jenkins_tool.server.jobs.health_report(self.job_name)


class LastBuildConsoleOutput(Strategy):
    """Get job_name console output"""

    def __init__(self, job_name):
        super().__init__()
        self.job_name = job_name

    def execute(self):
        last_build_number = self.jenkins_tool.server.jobs.last_build_number_by_name(self.job_name)
        return self.jenkins_tool.server.builds.console_output(self.job_name, last_build_number)


class PullBuildArtifactsAndRobotReports(Strategy):
    """
         pull consoles from upstream build
         parse the correct accx_build job
         pull consoles from accx_build
         download all_artifacts zip file
         download robot logs and reports"""
    description = f'Pull Build Artifacts and Robot Reports to ./output folder'

    def __init__(self, job_name: str, build_number: int):
        super().__init__()
        self.job_name = job_name
        self.accx_job_name = "ACCx_RTA-DWH_NIGHTLY"
        self.build_number = int(build_number)

    def pull_consoles(self, job_name, build_number) -> str:
        return self.jenkins_tool.server.builds.console_output(job_name, build_number)

    def execute(self):
        us_console = self.pull_consoles(self.job_name, self.build_number)
        accx_build_num = self.console_parser.find_accx_build(us_console)

        self.jenkins_tool.server.builds.download_build_artifact(self.accx_job_name, accx_build_num, full_archive=True)
        self.jenkins_tool.server.builds.robot.download_robot_log(self.job_name, self.build_number)
        self.jenkins_tool.server.builds.robot.download_robot_report(self.job_name, self.build_number)
        webbrowser.open_new(self.script_dir / self.output_dir / self.robot_log_name)
        webbrowser.open_new_tab(self.script_dir / self.output_dir / self.robot_report_name)


class PullACCxDEVANYTESTBuildArtifacts(Strategy):
    """Pull build artifacts and robot reports from any ACCx_DEV_ANYTEST build"""

    def __init__(self, build_number):
        super().__init__()
        self.job_name = "DEV_ACCx-ANYTEST"
        self.build_number = build_number
        self.robot_log_name = f"log-{self.build_number}.html"
        self.robot_report_name = f"report-{self.build_number}.html"

    def execute(self):
        self.jenkins_tool.server.builds.download_build_artifact(self.job_name, self.build_number, full_archive=True)
        self.jenkins_tool.server.builds.download_robot_log(
            self.job_name,
            self.build_number,
            custom_output_file=self.robot_log_name
        )
        self.jenkins_tool.server.builds.download_robot_report(
            self.job_name,
            self.build_number,
            custom_output_file=self.robot_report_name
        )
        log_full_path = str(pathlib.Path(f"{self.output_dir.name}/{self.robot_log_name}").absolute())
        report_full_path = str(pathlib.Path(f"{self.output_dir.name}/{self.robot_report_name}").absolute())
        webbrowser.open_new(log_full_path)
        webbrowser.open_new_tab(report_full_path)


class CreateJiraFromLastJobsExecution(Strategy):
    """Create Jira ticket from job failure"""

    def __init__(self, view_name):
        super().__init__()
        self.view_name = view_name

    def execute(self):
        view_health = str(ViewHealthReport(self.view_name).execute())
        created_jira = self.jira_tool.issue.create(
            {
                "fields": {
                    "project": {
                            "key": "IOTA"
                    },
                    "summary": f"{date.today().strftime('%d/%m')} Fix {self.view_name} TC results",
                    "description": f"{self.view_name}: Fix the failed tests",

                    "issuetype": {
                            "name": "Story"
                    },
                    "labels": ["Leprechauns", "RobotTests", "JobFailure", "Analytics"],
                    'customfield_25310': [{'active': True,
                                           'avatarUrls': {
                                               '16x16': 'https://eteamproject.internal.ericsson.com/secure/useravatar?size=xsmall&avatarId=10122',
                                               '24x24': 'https://eteamproject.internal.ericsson.com/secure/useravatar?size=small&avatarId=10122',
                                               '32x32': 'https://eteamproject.internal.ericsson.com/secure/useravatar?size=medium&avatarId=10122',
                                               '48x48': 'https://eteamproject.internal.ericsson.com/secure/useravatar?avatarId=10122'},
                                           'displayName': 'Leprechauns',
                                           'emailAddress': 'PDLPTEAMSL@ericsson.com',
                                           'key': 'JIRAUSER101325',
                                           'name': 'leprechauns',
                                           'self': 'https://eteamproject.internal.ericsson.com/rest/api/2/user?username=leprechauns',
                                           'timeZone': 'Europe/Stockholm'}],
                    "assignee": {
                        "name": "esvdeaa"
                    }
                }
            }
        )
        # print(created_jira)
        self.jira_tool.issue.comment.post(created_jira['key'], {'body': f"{json.dumps(view_health)}"})

        for job_name in ['ACC3_RTA_DWH_NIGHTLY', 'ACC4_RTA_DWH_NIGHTLY', 'ACC5CDCS_RTA_DWH_NIGHTLY']:
            last_build_number = self.jenkins_tool.server.jobs.last_build_number_by_name(job_name)

            self.jira_tool.issue.comment.post(
                created_jira['key'],
                {'body': f'====================\n{job_name} build {last_build_number}\n\n'
                         f'TEST RESULTS: http://10.44.62.37:8080/jenkins/view/Leprechauns/view/Leprechauns_Nightly/job/{job_name}/{last_build_number}/robot/\n'
                         f'REPORT: http://10.44.62.37:8080/jenkins/view/Leprechauns/view/Leprechauns_Nightly/job/{job_name}/{last_build_number}/robot/report/report_all.html\n'
                         f'LOG: http://10.44.62.37:8080/jenkins/view/Leprechauns/view/Leprechauns_Nightly/job/{job_name}/{last_build_number}/robot/report/log_all.html\n'
                         f'CONSOLE: http://10.44.62.37:8080/jenkins/view/Leprechauns/view/Leprechauns_Nightly/job/{job_name}/{last_build_number}/console'
                 }
            )
        return created_jira


class GetJiraIssue(Strategy):
    """Get Jira issue"""

    def __init__(self, issue_key):
        super().__init__()
        self.issue_key = issue_key

    def execute(self):
        return self.jira_tool.issue.get(self.issue_key)


class LogWorkInJira(Strategy):
    """Log work in Jira ticket"""

    def __init__(self, issue_key, time_spent_hours, comment):
        super().__init__()
        self.issue_key = issue_key
        self.time_spent_hours = time_spent_hours
        self.comment = comment

    def execute(self):
        payload = json.dumps({
            "timeSpent": self.time_spent_hours,
            "comment": self.comment
        })
        return self.jira_tool.issue.worklog.add_worklog(self.issue_key, payload)


class MonitorElasticClusterHealth(Strategy):
    """Log the current health of the Elastic cluster in a loop, until ctrl_c is pressed"""

    def __init__(self, interval_seconds, optional_verbose_output=False):
        super().__init__()
        self.interval_seconds = int(interval_seconds)
        self.verbose_output = json.loads(str(optional_verbose_output).lower())

    def execute(self):
        signal(SIGINT, Strategy.handler)
        print('Monitoring ElasticSearch Cluster Health. Press CTRL-C to exit.')
        while True:
            try:
                self.elastic_tool.cat.health(verbose=self.verbose_output)
                sleep(self.interval_seconds)
            except Exception as e:
                print(e)
                break


class ElasticClusterState(Strategy):
    """Very verbose output of ElasticSearch cluster state
        Possible values for metric:
            'nodes', 'routing_table', 'routing_nodes', 'metadata', 'master_node', 'blocks', 'version'
            '_all' is the default value
    """

    def __init__(self, metric='_all'):
        super().__init__()
        self.metric = metric

    def execute(self):
        return self.elastic_tool.cluster.state(metric=self.metric)


class ElasticClusterHealth(Strategy):
    """ElasticSearch cluster health"""

    def __init__(self):
        super().__init__()

    def execute(self):
        return self.elastic_tool.cluster.health()


class ElasticClusterStats(Strategy):
    """ElasticSearch cluster stats"""

    def __init__(self):
        super().__init__()

    def execute(self):
        return self.elastic_tool.cluster.stats()


class AllCurrentElasticTasks(Strategy):
    """Get all current Elastic tasks"""

    def __init__(self):
        super().__init__()

    def execute(self):
        return self.elastic_tool.cat.tasks(verbose=True)


class ElasticIndexInfo(Strategy):
    """Get ElasticSearch index info"""

    def __init__(self, index_name):
        super().__init__()
        self.index_name = index_name

    def execute(self):
        return self.elastic_tool.indices.get(index=self.index_name)


class SuggestAddGerritReviewers(Strategy):
    """Suggest reviewers for a Gerrit review"""

    def __init__(self, project, change_id, auto_add_suggested_reviewers=False):
        super().__init__()
        self.project = project
        self.change_id = change_id
        self.auto_add_reviewers = auto_add_suggested_reviewers

    def execute(self):
        if self.project.lower() == "xdn":
            tool = self.xdn_gerrit_tool
        elif self.project.lower() == "ecn":
            tool = self.xdn_gerrit_tool
        else:
            raise ValueError(f'Invalid project: {self.project}')
        suggested_reviewers = tool.change.reviewer.suggest(self.change_id)
        if self.auto_add_reviewers:
            for reviewer in suggested_reviewers:
                response = tool.change.reviewer.add(self.change_id, reviewer['account']['username'])
                if response.ok:
                    print(f"Added reviewer {reviewer['account']['username']}/{reviewer['account']['name']}/{reviewer['account']['email']}")
        return suggested_reviewers


class AddTopicToGerritChange(Strategy):
    """Add a topic to a Gerrit change"""

    def __init__(self, project, change_id, topic):
        super().__init__()
        self.project = project
        self.change_id = change_id
        self.topic = topic

    def execute(self):
        if self.project.lower() == "xdn":
            tool = self.xdn_gerrit_tool
        elif self.project.lower() == "ecn":
            tool = self.ecn_gerrit_tool
        else:
            raise ValueError(f'Invalid project: {self.project}')
        response = tool.change.topic.set(self.change_id, self.topic)
        if response.ok:
            print(f"Added topic {self.topic} to change {self.change_id}")
        return response


class MonitorKarafBundleList(Strategy):
    """Monitor Karaf bundle list
    TODO: currently need to enter password for every loop, need to fix this
    """

    def __init__(self, interval_seconds):
        super().__init__()
        self.interval_seconds = int(interval_seconds)

    def execute(self):
        signal(SIGINT, Strategy.handler)
        print('Monitoring Karaf bundle list. Press CTRL-C to exit.')
        while True:
            try:
                self.karaf_tool.bundle.info.list()
                sleep(self.interval_seconds)
            except Exception as e:
                print(e)
                break


# --------( OBSOLETE or NOT NEEDED )---------- ####
#
# class DebugJobInfo(Strategy):
#     """Get job_name info"""
#
#     def __init__(self, job_name):
#         super().__init__()
#         self.job_name = job_name
#
#     def execute(self):
#         return self.jenkins_tool.server.jobs.debug_info_by_name(self.job_name)
#
# class BuildJobWithParameters(Strategy):
#     """Build job_name with parameters"""
#     description = 'Build Job With Parameters'
#
#     def __init__(self, job_name, parameters):
#         super().__init__()
#         self.job_name = job_name
#         self.parameters = parameters
#
#     def execute(self):
#         self.jenkins_tool.jobs.build(self.job_name, parameters=self.parameters)
#
#
#
#
# class EnableJob(Strategy):
#     """Enable job_name"""
#
#     def __init__(self, job_name):
#         super().__init__()
#         self.job_name = job_name
#
#     def execute(self):
#         self.jenkins_tool.server.jobs.enable(self.job_name)
#
#
# class DisableJob(Strategy):
#     """Disable job_name"""
#
#     def __init__(self, job_name):
#         super().__init__()
#         self.job_name = job_name
#
#     def execute(self):
#         self.jenkins_tool.server.jobs.disable(self.job_name)
#
#
# class JobExists(Strategy):
#     """Check if job_name exists"""
#
#     def __init__(self, job_name):
#         super().__init__()
#         self.job_name = job_name
#
#     def execute(self):
#         return self.jenkins_tool.server.jobs.exists(self.job_name)
#
#
# class DeleteJob(Strategy):
#     """Delete job_name, USE WITH CAUTION"""
#
#     def __init__(self, job_name):
#         super().__init__()
#         self.job_name = job_name
#
#     def execute(self):
#         if self.jenkins_tool.server.jobs.exists(self.job_name):
#             self.jenkins_tool.server.jobs._delete_job_USE_WITH_EXTREME_CAUTION(self.job_name)
#
#
# class CreateJob(Strategy):
#     """Create job_name from job_config_xml (Default: EMPTY_JOB_CONFIG_XML)"""
#     description = 'Create Job'
#
#     def __init__(self, job_name, job_config_xml=EMPTY_CONFIG_XML):
#         super().__init__()
#         self.job_name = job_name
#         self.job_config_xml = job_config_xml
#
#     def execute(self):
#         if not self.jenkins_tool.server.jobs.exists(self.job_name):
#             self.jenkins_tool.server.jobs.create(self.job_name, self.job_config_xml)
#
#
# class ReconfigureJob(Strategy):
#     """Reconfigure job_name from job_config_xml"""
#
#     def __init__(self, job_name, job_config_xml):
#         super().__init__()
#         self.job_name = job_name
#         self.job_config_xml = job_config_xml
#
#     def execute(self):
#         self.jenkins_tool.server.jobs.reconfigure(self.job_name, self.job_config_xml)
#
#
# class AllJobs(Strategy):
#     """Get all jobs info"""
#
#     def __init__(self):
#         super().__init__()
#
#     def execute(self):
#         return self.jenkins_tool.server.jobs.all()
#
#
# class CountJobs(Strategy):
#     """Count of all jobs"""
#
#     def __init__(self):
#         super().__init__()
#
#     def execute(self):
#         return self.jenkins_tool.server.jobs.count()
#
#
#
# class ServerInfo(Strategy):
#     """Get full server info (Jobs/Views/Projects/Labels), and version"""
#
#     def __init__(self):
#         super().__init__()
#
#     def execute(self):
#         return self.jenkins_tool.server.info(), f"Server Version: {self.jenkins_tool.server.version()}"
#
#
# class AllPlugins(Strategy):
#     """Get all plugins info"""
#
#     def __init__(self):
#         super().__init__()
#
#     def execute(self):
#         return self.jenkins_tool.server.plugins.all()
#
#
# class PluginInfo(Strategy):
#     """Get info for plugin plugin_name"""
#
#     def __init__(self, plugin_name):
#         super().__init__()
#         self.plugin_name = plugin_name
#
#     def execute(self):
#         return self.jenkins_tool.server.plugins.info_by_name(self.plugin_name)
#
#
# class AllNodes(Strategy):
#     """Get all nodes info"""
#
#     def __init__(self):
#         super().__init__()
#
#     def execute(self):
#         return self.jenkins_tool.server.nodes.all()
#
#
# class NodeInfo(Strategy):
#     """Get info for node node_name"""
#
#     def __init__(self, node_name):
#         super().__init__()
#         self.node_name = node_name
#
#     def execute(self):
#         return self.jenkins_tool.server.nodes.info_by_name(self.node_name)
#
#
# class NodeConfig(Strategy):
#     """Get node_name xml config"""
#
#     def __init__(self, node_name):
#         super().__init__()
#         self.node_name = node_name
#
#     def execute(self):
#         return self.jenkins_tool.server.nodes.config_by_name(self.node_name)
#
#
# class AllViews(Strategy):
#     """Get all views info"""
#
#     def __init__(self):
#         super().__init__()
#
#     def execute(self):
#         return self.jenkins_tool.server.views.all()
#
#
# class ViewExists(Strategy):
#     """Check if view view_name exists"""
#
#     def __init__(self, view_name):
#         super().__init__()
#         self.view_name = view_name
#
#     def execute(self):
#         return self.jenkins_tool.server.views.exists(self.view_name)
#
#
# class CreateView(Strategy):
#     """Create New Jenkins View view_name"""
#
#     def __init__(self, view_name):
#         super().__init__()
#         self.view_name = view_name
#
#     def execute(self):
#         self.jenkins_tool.server.views.create(self.view_name, EMPTY_VIEW_CONFIG_XML)
#
#
# class DeleteView(Strategy):
#     """Delete view_name, USE WITH CAUTION"""
#
#     def __init__(self, view_name):
#         super().__init__()
#         self.view_name = view_name
#
#     def execute(self):
#         self.jenkins_tool.server.views._delete_view_USE_WITH_EXTREME_CAUTION(self.view_name)
#
#
# class ViewConfig(Strategy):
#     """Get view_name xml config"""
#
#     def __init__(self, view_name):
#         super().__init__()
#         self.view_name = view_name
#
#     def execute(self):
#         return self.jenkins_tool.server.views.config_by_name(self.view_name)


# class JobConfig(Strategy):
#     """Get job_name xml config"""
#
#     def __init__(self, job_name):
#         super().__init__()
#         self.job_name = job_name
#
#     def execute(self):
#         return self.jenkins_tool.server.jobs.config_by_name(self.job_name)


# class RebuildJob(Strategy):
#     """Rebuild job_name"""
#
#     def __init__(self, job_name):
#         super().__init__()
#         self.job_name = job_name
#
#     def execute(self):
#         self.jenkins_tool.server.jobs.rebuild(self.job_name)
# class RenameJob(Strategy):
#     """Rename job_name to new_job_name"""
#
#     def __init__(self, job_name, new_job_name):
#         super().__init__()
#         self.job_name = job_name
#         self.new_job_name = new_job_name
#
#     def execute(self):
#         self.jenkins_tool.server.jobs.rename(self.job_name, self.new_job_name)
