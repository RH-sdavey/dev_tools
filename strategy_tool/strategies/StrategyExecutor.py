from __future__ import annotations
import os
import types
from abc import ABC, abstractmethod
from importlib.machinery import SourceFileLoader
from pathlib import Path
from sys import exit


from ..console_parser import ConsoleParser


def load_module_from_file(name, path):
    try:
        loaded = SourceFileLoader(name, str(path))
        if isinstance(loaded, types.ModuleType):
            return loaded, None
        return loaded.load_module(), None
    except Exception as error:
        print("EXCEPTION: " + str(error))
        return None, error


class Executor:

    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def execute_strategy(self):
        return self._strategy.execute()


class Strategy(ABC):

    def __init__(self):

        self.console_parser = ConsoleParser()
        self.script_dir = Path(os.path.dirname(__file__))
        self.output_dir = Path("../../jenkins_tool/output")
        self.robot_log_name = Path("log_all.html")
        self.robot_report_name = Path("report_all.html")
        self.jenkins = load_module_from_file("jenkins_tool", self.script_dir.parent.parent / "jenkins_tool/jenkins_tool.py")[0]
        self.jira = load_module_from_file("jira_tool",  self.script_dir.parent.parent / "jira_tool/jira_tool.py")[0]
        self.gerrit = load_module_from_file("gerrit_tool",  self.script_dir.parent.parent / "gerrit_tool/gerrit_tool.py")[0]
        self.elastic = load_module_from_file("elastic_tool",  self.script_dir.parent.parent / "elastic_tool/elastic_tool.py")[0]
        self.karaf = load_module_from_file("karaf_tool",  self.script_dir.parent.parent / "karaf_tool/karaf_tool.py")[0]

        self.jenkins_tool = self.jenkins.JenkinsTool()
        self.jira_tool = self.jira.JiraTool()
        self.gerrit_tool = self.gerrit.GerritTool()

        self.elastic_tool = self.elastic.EsTool()
        self.karaf_tool = self.karaf.KarafTool()

    @classmethod
    def handler(cls, signal_received, frame):
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        exit(0)


class StrategyExecutor(Executor):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def precondition(self, *args, **kwargs):
        pass
