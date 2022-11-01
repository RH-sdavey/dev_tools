import os
from pathlib import Path


class KarafTool:
    def __init__(self):
        self.karaf_client = Path(os.environ['KARAF_CLIENT'])
        self.bundle = self.Bundle(self)

    def run_command(self, command):
        command = command.split()
        command.insert(0, self.karaf_client.as_posix())
        command.insert(1, '--')
        return os.system(' '.join(command))

    class Bundle:
        def __init__(self, karaf_tool):
            self.karaf_tool = karaf_tool
            self.action = self.Action(self.karaf_tool)
            self.info = self.Info(self.karaf_tool)

        class Action:
            def __init__(self, karaf_tool):
                self.karaf_tool = karaf_tool

            def install(self, bundle_name):
                return self.karaf_tool.run_command('bundle:install ' + bundle_name)

            def diagnose(self):
                return self.karaf_tool.run_command(f'bundle:diag')

            def refresh(self):
                return self.karaf_tool.run_command('bundle:refresh')

            def resolve(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:resolve {bundle_id}')

            def start(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:start {bundle_id}')

            def stop(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:stop {bundle_id}')

            def uninstall(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:uninstall {bundle_id}')

            def update(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:update {bundle_id}')

            def watch(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:watch {bundle_id}')

        class Info:
            def __init__(self, karaf_tool):
                self.karaf_tool = karaf_tool

            def info(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:info {bundle_id}')

            def list(self):
                return self.karaf_tool.run_command('bundle:list')

            def capabilities(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:capabilities {bundle_id}')

            def classes(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:classes {bundle_id}')

            def find_class_in_bundles(self, class_name):
                return self.karaf_tool.run_command(f'bundle:find-class {class_name}')

            def headers(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:headers {bundle_id}')

            def get_id_by_name(self, bundle_full_name):
                return self.karaf_tool.run_command(f'bundle:id {bundle_full_name}')

            def services(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:services {bundle_id}')

            def start_level(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:start-level {bundle_id}')

            def status(self, bundle_id=""):
                return self.karaf_tool.run_command(f'bundle:status {bundle_id}')

            def tree(self, bundle_id, show_bundle_versions=False):
                versions = "-v" if show_bundle_versions else ""
                return self.karaf_tool.run_command(f'bundle:tree-show {versions} {bundle_id}')

