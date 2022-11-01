import os


class GitTool:
    def __init__(self, path):
        self.path = path
        self.git_path = path + "/.git"
        self.commit = self.Commit(self)

    def is_git_repo(self):
        return os.path.exists(self.git_path)

    class Commit:
        def __init__(self, git_instance):
            self.git_instance = git_instance

        def get_commit_details(self):
            """
            Returns a list of Commit objects
            """
            print(self.git_instance.path)
            if self.git_instance.is_git_repo():
                commits = []
                for line in os.popen(f"git  --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --git-dir {self.git_instance.path}  log").readlines():
                    commits.append(line)
                return commits

    def get_git_repo_name(self):
        """
        Returns the name of the git repo
        """
        if self.is_git_repo():
            return self.path.split("/")[-1]
        else:
            return None

    def get_git_repo_path(self):
        """
        Returns the path to the git repo
        """
        if self.is_git_repo():
            return self.git_path
        else:
            return None

    def get_git_repo_url(self):
        """
        Returns the url to the git repo
        """
        if self.is_git_repo():
            return self.get_git_repo_path().split("/")[-2]
        else:
            return None

    def get_git_repo_branch(self):
        """
        Returns the current branch
        """
        if self.is_git_repo():
            return self.get_git_repo_path().split("/")[-1]
        else:
            return None

    def get_git_repo_commit_id(self):
        """
        Returns the commit id
        """
        if self.is_git_repo():
            return self.get_git_repo_path().split("/")[-1]
        else:
            return None

    def get_git_repo_commit_id_short(self):
        """
        Returns the commit id, short version
        """
        if self.is_git_repo():
            return self.get_git_repo_commit_id()[:7]
        else:
            return None

    def get_git_repo_commit_id_long(self):
        """

        """
        if self.is_git_repo():
            return self.get_git_repo_commit_id()
        else:
            return None
