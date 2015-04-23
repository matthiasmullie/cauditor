def process(project, commit, data, previous):
    avg = averages(data)
    old_avg = averages(previous) if previous else {metric: 0 for metric, value in avg.items()}  # previous can be empty

    # calculate difference between both commits
    # averages between commits can be negative, when overall value of a metric was reduced
    diff = {metric: value - old_avg[metric] for metric, value in avg.items()}

    store(project, commit, diff)

def store(project, commit, metrics):
    import json
    import models

    commit.update({'project': project['name']})
    commit.update({'metrics': json.dumps(metrics)})

    commits = models.commits.Commits()
    commits.store(commit)

def averages(data):
    class_metrics = ['dit', 'ca', 'ce', 'i']
    method_metrics = ['ccn', 'npath', 'mi', 'he', 'hi']

    # calculate averages: sum metrics over all classes/methods & divide by amount of classes/methods
    class_avg = {metric: class_total(data, metric) / (data['noc'] or 1) for metric in class_metrics}
    method_avg = {metric: method_total(data, metric) / (data['nom'] or 1) for metric in method_metrics}

    # combine class & method metrics
    avg = class_avg.copy()
    avg.update(method_avg)

    return avg

def class_total(data, metric):
    try:
        return sum([
            class_data[metric]
            for package_data in data['children']
            for class_data in package_data['children']
        ])
    except Exception:
        # children likely didn't exist; there are no classes (yet)
        return 0

def method_total(data, metric):
    try:
        return sum([
            method_data[metric]
            for package_data in data['children']
            for class_data in package_data['children']
            for method_data in class_data['children']
        ])
    except Exception:
        # children likely didn't exist; there are no classes (yet)
        return 0
