from importers import last_commit


class Importer(last_commit.Importer):
    list_commits_command = "git log --pretty=format:'%H\t%ae\t%ad\t%ce\t%cd' --reverse --date=local {hash}~1.."
    includes_skip = True  # skips first item returned by list_commits_command, because it's "previous" to compare with
