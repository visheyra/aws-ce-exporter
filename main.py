from argparse import ArgumentParser
import multiprocessing
import json
import time 
import schedule
import sys

from config import load_config
from scheduler import run_scheduler
from prometheus import Exporter

import signal

def signal_handler(sig, frame):
        schedule.clear()
        sys.exit(0)

def _parse():
    parser = ArgumentParser()
    parser.add_argument('--config', '-c', help='path to config file', default='config.yaml')
    return parser.parse_args()


def main():
    #signal.signal(signal.SIGINT, signal_handler)
    #signal.signal(signal.SIGTERM, signal_handler)
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
        except Exception as e:
            pass
        else:
            print(json.dumps(d, indent=4))
            prom.hand_out(d)
        time.sleep(5)


if __name__ == '__main__':
    main()