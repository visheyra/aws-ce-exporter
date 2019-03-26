from argparse import ArgumentParser
import multiprocessing
import json
import time
import schedule

from config import load_config
from scheduler import run_scheduler
from prometheus import Exporter


def _parse():
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', help='path to config file',
                        default='config.yaml')
    return parser.parse_args()


def main():
    args = _parse()
    config = load_config(args.config)
    print(json.dumps(config, indent=4))
    time.sleep(4)
    prom = Exporter(config)
    q = multiprocessing.Queue()
    run_scheduler(config, q)
    while True:
        schedule.run_pending()
        try:
            d = q.get(False)
        except multiprocessing.queues.Empty:
            pass
        else:
            print(json.dumps(d, indent=4))
            prom.hand_out(d)
        time.sleep(5)


if __name__ == '__main__':
    main()
