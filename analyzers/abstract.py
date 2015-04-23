import abc
import subprocess
import datetime
import container
import models


class Analyzer(object):
    def __init__(self, project):
        projects = models.projects.Projects()
        self.project = projects.select(name=project)[0]

        # figure out last imported commit in this project (if any)
        try:
            commits = models.commits.Commits()
            self.commit = commits.select(project=project, option=["ORDER BY commit_date DESC", "LIMIT 1"])[0]
        except Exception:
            self.commit = None

        config = container.load_config()
        self.path = "{path}/{name}".format(path=config['analyzers']['repo_path'], name=project)

    def execute(self):
        try:
            self.cleanup()
            self.clone(self.project['git'], self.path)
            commits = self.list_commits(self.path, self.commit['hash'] if self.commit else None)

            # analyze already-imported last revision: this makes it possible to calculate
            # differences between commits. We could rely on the data from when we
            # previously analyzed that commit, but it analyzer software changes, that would
            # be unreliable
            previous = self.analyze(self.commit) if self.commit else {}
            for commit in commits:
                self.checkout(self.path, commit)
                data = self.analyze()
                self.listeners(self.project, commit, data, previous)

                # moving on to next commit soon, mark this one as previous
                previous = data
        except Exception:
            # nothing, just want to make sure cleanup() is also run after failure
            pass

        self.cleanup()

    def cleanup(self):
        # AWS doesn't charge for inbound data; however storage comes at a price.
        # Instead of storing repos, we'll delete them after analyzing them and
        # re-clone of we want to analyze new commits.
        # https://aws.amazon.com/blogs/aws/aws-lowers-its-pricing-again-free-inbound-data-transfer-and-lower-outbound-data-transfer-for-all-ser/
        subprocess.call("rm -rf {path}".format(path=self.path), shell=True)

    def clone(self, repo, path):
        cmd = "git clone {repo} {path}".format(repo=repo, path=path)
        subprocess.call(cmd, shell=True)

    def list_commits(self, path, since=None):
        cmd = "git log --pretty=format:'%H\t%ae\t%ad\t%ce\t%cd' --reverse --date=local"
        if since is not None:
            cmd = cmd + " {hash}..".format(hash=since)

        output = subprocess.check_output(
            "cd {path} ".format(path=path) +  # cd into repo
            "&& git checkout master -q " +  # make sure we're on master (without output)
            "&& git pull -q " +  # make sure we're up-to-date (without output)
            "&& " + cmd, shell=True).decode("utf-8")

        commits = [line.split("\t") for line in output.split("\n")]
        return [{
            'hash': commit[0],
            'author': commit[1],
            'author_date': datetime.datetime.strptime(commit[2], "%a %b %d %H:%M:%S %Y"),
            'committer': commit[3],
            'commit_date': datetime.datetime.strptime(commit[4], "%a %b %d %H:%M:%S %Y"),
        } for commit in commits]

    def checkout(self, path, commit):
        cmd = "git checkout {hash}".format(hash=commit['hash'])  # checkout this specific commit
        subprocess.call(
            "cd {path} ".format(path=path) +  # cd into repo
            "&& " + cmd, shell=True)

    def listeners(self, project, commit, data, previous):
        import listeners
        listeners.process(project, commit, data, previous)

    @abc.abstractmethod
    def analyze(self):
        return
