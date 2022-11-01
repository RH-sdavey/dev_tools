import os
from jenkins import Jenkins as J_LIB
import requests

from robot.api import ExecutionResult, ResultVisitor


class JenkinsTool:

    def __init__(self):
        self.username = os.environ['jenkins_script_user']
        # Login to jenkins > Click username > Configure > Show Legacy API token
        self.token = os.environ['jenkins_script_token']
        self.user = self.User(self.username, self.token).login_to_jenkins()
        self.server = self.Server(self.user.get_server_instance())

    class User:
        def __init__(self, username, token):
            self.jenkins_url = "jenkins build master url here"
            self.username = username
            self.token = token
            self.server = None

        def login_to_jenkins(self):
            self.server = J_LIB(self.jenkins_url, username=self.username, password=self.token)
            return self

        def get_server_instance(self):
            return self.server

        def get_user_details(self):
            user_details = self.server.get_whoami()
            return {
                "fullname": user_details['fullName'],
                "id": user_details['id'],
                "email": [value['address'] for value in user_details['property'] if 'address' in value][0]
            }

    class Server:
        def __init__(self, server):
            self.server = server
            self.plugins = self.Plugins(self.server)
            self.nodes = self.Nodes(self.server)
            self.views = self.Views(self.server)
            self.jobs = self.Jobs(self.server)
            self.builds = self.Builds(self.server)

        def info(self):
            return self.server.get_info()

        def version(self):
            return self.server.get_version()

        class Plugins:
            def __init__(self, server):
                self.server = server

            def all(self):
                return self.server.get_plugins()

            def info_by_name(self, name):
                return self.server.get_plugin_info(name)

        class Nodes:
            def __init__(self, server):
                self.server = server

            def all(self):
                """Get a list of nodes connected to the Master
                   Each node is a dict with keys ‘name’ and ‘offline’
                   :return:	[ { str: str, str: bool} ]
                   :rtype: list(dict)
                """
                return self.server.get_nodes()

            def info_by_name(self, name):
                return self.server.get_node_info(name)

            def config_by_name(self, name):
                return self.server.get_node_config(name)

        class Views:
            def __init__(self, server):
                self.server = server

            def all(self):
                return self.server.get_views()

            def exists(self, name):
                return self.server.view_exists(name)

            def create(self, name, config_xml):
                self.server.create_view(name, config_xml)

            def delete_USE_WITH_EXTREME_CAUTION(self, name):
                self.server.delete_view(name)

            def config_by_name(self, name):
                return self.server.get_view_config(name)

        class Jobs:
            def __init__(self, server):
                self.server = server

            def all(self):
                return self.server.get_all_jobs()

            def count(self):
                return self.server.jobs_count()

            def health_report(self, name):
                if len(self.server.get_job_info(name)['healthReport']) > 0:
                    return {
                        "Name": name,
                        "Description": self.server.get_job_info(name)['healthReport'][0]['description'],
                        "Score": self.server.get_job_info(name)['healthReport'][0]['score']
                    }

            def all_by_view_name(self, view_name):
                return self.server.get_jobs(view_name=view_name)

            def info_by_name(self, name):
                return self.server.get_job_info(name)

            def debug_info_by_name(self, name):
                return self.server.debug_job_info(name)

            def last_build_number_by_name(self, name):
                return self.server.get_job_info(name)['lastBuild']['number']

            def config_by_name(self, name):
                return self.server.get_job_config(name)

            def trigger_build_by_name(self, name):
                """
                This method returns a queue item number that you can pass to Builds.get_build_info(name, <HERE>).
                Note that this queue number is only valid for about five minutes after the job completes,
                so you should get/poll the queue information as soon as possible to determine the job’s URL.
                :param name:
                :return:
                """
                return self.server.build_job(name)

            def create(self, name, config_xml):
                self.server.create_job(name, config_xml)

            def copy(self, from_name, to_name):
                self.server.copy_job(from_name, to_name)

            def rename(self, from_name, to_name):
                self.server.rename_job(from_name, to_name)

            def _delete_job_USE_WITH_EXTREME_CAUTION(self, name):
                self.server.delete_job(name)

            def enable(self, name):
                self.server.enable_job(name)

            def disable(self, name):
                self.server.disable_job(name)

            def exists(self, name) -> bool:
                return self.server.job_exists(name)

            def reconfigure(self, name, config_xml):
                self.server.reconfig_job(name, config_xml)

        class Builds:
            def __init__(self, server):
                self.server = server
                self.robot = self.Robot(self)

            def console_output(self, job_name, number):
                return self.server.get_build_console_output(job_name, number)

            def get_last_build_number(self, job_name):
                return self.server.get_last_build_number(job_name)

            def all_running(self):
                return self.server.get_running_builds()

            def get_build_url_by_name(self, name, parameters=None, token=None):
                return self.server.build_job_url(name, parameters, token)

            def info_by_name(self, job_name, number):
                return self.server.get_build_info(job_name, number)

            def env_vars_by_name(self, job_name, number):
                return self.server.get_build_env_vars(job_name, number)

            def test_report(self, job_name, number):
                """Will most likely return None as we have robot test reports"""
                return self.server.get_build_test_report(job_name, number)

            def stop(self, job_name, number):
                self.server.stop_build(job_name, number)

            def delete(self, job_name, number):
                self.server.delete_build(job_name, number)

            def download_build_artifact(self, job_name, number, file_name=None, full_archive=False):
                if (not file_name and not full_archive) or (file_name and full_archive):
                    raise Exception("Cannot have both or neither file_name and full_archive")
                if full_archive:
                    self.download_full_archive(job_name, number)
                else:
                    self.download_one_file_from_artifact(file_name, job_name, number)

            def download_one_file_from_artifact(self, file_name, job_name, number):
                print(f"--(( Downloading {file_name} from {self.server.server}{job_name}/{number}")
                url = f"{self.server.server}/job/{job_name}/{number}/artifact/output/{file_name}"
                with open(file_name, "wb") as out:
                    out.write(requests.get(url).content)

            def download_full_archive(self, job_name, number):
                output_file = 'archive.zip'
                output_path = f'output/{output_file}'
                url = f"{self.server.server}/job/{job_name}/{number}/artifact/*zip*/{output_file}"
                print(f"--(( Downloading robot report from {url} --> {output_path}))")
                with open(output_path, "wb") as out:
                    out.write(requests.get(url).content)

            class Robot:
                def __init__(self, server):
                    self.server = server

                class AllTestResults(ResultVisitor):
                    def visit_test(self, test):
                        print(f'{test.longname} | {test.status}')

                class FailedTests(ResultVisitor):
                    def visit_test(self, test, result='FAIL'):
                        if test.status == 'FAIL':
                            print(f'{test.longname} | {test.status}')

                class PassedTests(ResultVisitor):
                    def visit_test(self, test):
                        result = []
                        if test.status == 'PASS':
                            result.append(f'{test.longname} | {test.status}')
                        return result

                class TestBodies(ResultVisitor):
                    def visit_test(self, test):
                        print(f'{test.longname} | {test.status} | {[line for line in test.body]}')

                def download_robot_log(self, job_name, number, custom_output_file=None):
                    output_file = 'log_all.html' if not custom_output_file else custom_output_file
                    output_path = f'output/{output_file}'
                    url = f"{self.server.server}/job/{job_name}/{number}/robot/report/{output_file}"
                    print(f"--(( Downloading robot report from {url} --> {output_path}))")
                    with open(output_path, "wb") as out:
                        out.write(requests.get(url).content)

                def download_robot_report(self, job_name, number, custom_output_file=None):
                    output_file = 'report_all.html' if not custom_output_file else custom_output_file
                    output_path = f'output/{output_file}'
                    url = f"{self.server.server}/job/{job_name}/{number}/robot/report/{output_file}"
                    print(f"--(( Downloading robot report from {url} --> {output_path}))")
                    with open(output_path, "wb") as out:
                        out.write(requests.get(url).content)

                def get_passed_tests(self, file_name):
                    result = ExecutionResult(file_name)
                    yield result.visit(self.PassedTests())
