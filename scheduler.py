import signal
import sys
import schedule
import ce_job
import datetime
import credentials

def run_scheduler(config, data_queue):
    jobs = [_create_target(job) for job in config['jobs']]
    for j in jobs:
        schedule.every(int(j.refresh)).seconds.do(j.execute, data_queue)

def _create_target(target_config):
    now = datetime.datetime.utcnow()
    delta = int(target_config['delta'])
    creds = credentials.Credentials(target_config['credentials'])
    return ce_job.CostExplorerJob(
        name=target_config['name'],
        labels=target_config['metric_labels'],
        credentials=creds,
        metrics=target_config['metric'],
        granularity=target_config['granularity'].upper(),
        start=(now - datetime.timedelta(days=delta)).strftime('%Y-%m-%d'),
        end=now.strftime('%Y-%m-%d'),
        refresh=target_config['refresh']
    )
