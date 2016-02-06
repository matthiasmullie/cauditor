from cauditor.models import model
import abc
import pickle


class Jobs(model.DbManager):
    def __init__(self):
        super(Jobs, self).__init__()
        self.table = 'jobs'

    def add(self, job):
        """ Add a job to the queue
        :param job: Job
        """
        self.store(
            type=job.__class__.__name__,
            job=pickle.dumps(job),
        )

    def run(self, type=None):
        if type is None:
            data = self.select(options=["ORDER BY id ASC", "LIMIT 1"])
        else:
            data = self.select(type=type, options=["ORDER BY id ASC", "LIMIT 1"])

        try:
            job = next(data)
        except Exception:
            # there is no job...
            return

        # delete job from queue
        self.select(id=job['id']).delete()

        # reconstruct job & execute
        job = pickle.loads(job['job'])
        try:
            job.execute()
        except Exception:
            # failed to run, reinsert
            self.add(job)


class Job(object):
    @abc.abstractmethod
    def execute(self):
        pass
