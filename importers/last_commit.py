import subprocess
import datetime
import container
import models


class Importer(object):
    list_commits_command = "git log --pretty=format:'%H\t%ae\t%ad\t%ce\t%cd' --reverse --date=local -2"
    includes_skip = True  # skips first item returned by list_commits_command, because it's "previous" to compare with

    def __init__(self, project):
        projects = models.projects.Projects()
        self.project = projects.select(name=project)[0]

        # figure out last imported commit in this project (if any)
        try:
            commits = models.commits.Commits()
            self.commit = commits.select(project=project, options=["ORDER BY commit_date DESC", "LIMIT 1"])[0]
        except Exception:
            self.commit = None

        config = container.load_config()
        self.path = "{path}/{name}".format(path=config['analyzers']['repo_path'], name=project)

    def execute(self):
        try:
            self.cleanup()
            self.clone(self.project['git'], self.path)
            commits = self.list_commits(self.path)

            # analyze previous revision: this makes it possible to calculate
            # differences between commits. We could rely on the data from when we
            # previously analyzed that commit, but it analyzer software changes,
            # that would be unreliable
            previous = {}
            if self.includes_skip:
                self.checkout(self.path, commits.pop(0))
                previous = self.analyze(self.project, self.path)

            # analyze the commits we really want to analyze, sending the results to listeners
            for commit in commits:
                self.checkout(self.path, commit)
                data = self.analyze(self.project, self.path)
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

    def list_commits(self, path):
        # parse hash of most recent commit into command
        cmd = self.list_commits_command.format(hash=self.commit['hash'] if self.commit else '')

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

    def analyze(self, project, path):
        import analyzers
        # @todo: should return the result, but what about multiple languages?
        return analyzers.execute(project, path)

    def listeners(self, project, commit, data, previous):
        import listeners
        listeners.execute(project, commit, data, previous)
