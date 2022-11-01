import os

import openshift
from openshift import OpenShiftPythonException


class SelectorsObjectsActions:
    def __init__(self):
        self.username = os.environ["OC_USER"]
        self.password = os.environ["OC_PASSWORD"]
        self.oc = openshift
        self.selector = None

        self.name = self.Name(self)
        self.label = self.Label(self)

    def get_selector_by_kind(self, selector_name: str):
        try:
            self.selector = self.oc.selector(selector_name)
            return self.selector
        except OpenShiftPythonException as e:
            print(e)

    def get_selector_by_list(self, names: list):
        """sa_selector = oc.selector(["serviceaccount/deployer", "serviceaccount/builder"])"""
        try:
            self.selector = self.oc.selector(names)
            return self.selector
        except OpenShiftPythonException as e:
            print(e)

    def get_selector_by_kind_and_label(self, kind: str,  label: dict):
        """sa_label_selector = oc.selector("sa", labels={"mylabel":"myvalue"})"""
        try:
            self.selector = self.oc.selector(kind, labels=label)
            return self.selector
        except OpenShiftPythonException as e:
            print(e)

    class Name:
        def __init__(self, parent):
            self.parent = parent
            self.selector = self.parent.selector
            self.oc = self.parent.oc

        def get_all_qualified_names(self):
            return self.selector.qnames()

        def get_all_names(self):
            return self.selector.names()

    class Label:
        def __init__(self, parent):
            self.parent = parent
            self.selector = self.parent.selector
            self.oc = self.parent.oc

        def get_all(self):
            return self.selector.labels()

        def apply(self, label: dict):
            """selector.label({"mylabel" : "myvalue"})"""
            self.selector.label(label)

        def get_by_label(self, component: str, label: dict):
            """sa_label_selector = oc.selector("sa", labels={"mylabel":"myvalue"})"""
            return self.selector(component, labels=label).names()

    class Describe:
        def __init__(self, parent):
            self.parent = parent
            self.selector = self.parent.selector
            self.oc = self.parent.oc

        def __call__(self, *args, **kwargs):
            return self.selector.describe(*args, **kwargs)


class Openshift(SelectorsObjectsActions):
    def __init__(self):
        super().__init__()
        self.user = self.User(self)
        self.projects = self.Projects(self)
        self.service_accounts = self.ServiceAccounts(self)
        self.build_configs = self.BuildConfigs(self)
        try:
            self.user.whoami()
        except OpenShiftPythonException:
            self.user.login()

    class User:
        def __init__(self, openshift):
            self.oc = openshift.oc

        def login(self):
            try:
                self.oc.login(self.oc.username, self.oc.password)
            except OpenShiftPythonException as e:
                print("[+] Exception raised when trying to log you in to Openshift using this client.\n"
                      "You will need to login to the OpenShift cluster using the command line before using this"
                      " object instance: 'oc login'")
                raise e

        def whoami(self):
            return self.oc.whoami()

    class Nodes:
        def __init__(self, openshift):
            self.openshift = openshift
            self.oc = openshift.oc
            self.selector = self.openshift.get_selector_by_kind("nodes")

        # def get_all(self):

    class Projects:
        def __init__(self, openshift):
            self.openshift = openshift
            self.oc = self.openshift.oc
            self.selector = self.openshift.get_selector_by_kind("projects")

        def get_all(self):
            return self.selector

        def get_one(self, name: str):
            return self.openshift.get_selector_by_list([name])

        def objects(self):
            return self.selector.objects()

        def count(self):
            return self.selector.count_existing()

        def describe(self):
            return self.selector.describe()

        def create(self, name: str):
            return self.oc.new_project(name, adm=False)

        def delete(self, name: str):
            return self.oc.delete_project(name, ignore_not_found=True, grace_period=1)

    class ServiceAccounts:
        def __init__(self, openshift):
            self.openshift = openshift
            self.oc = self.openshift.oc
            self.selector = self.openshift.get_selector_by_kind("serviceaccounts")

        def get_all(self):
            return self.selector

        def objects(self):
            return self.selector.objects()

    class BuildConfigs:
        def __init__(self, openshift):
            self.openshift = openshift
            self.oc = openshift.oc
            self.selector = openshift.get_selector_by_kind("buildconfigs")

        def describe(self):
            print("Please be patient, this may take a while...")
            return self.selector.describe()


sean = Openshift()
print(sean.service_accounts.objects()[0].as_dict()['secrets'])
