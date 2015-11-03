!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'web'

import ansible.playbook
from ansible import callbacks
from ansible import utils


def playbook(playbook_yml, extra_vars):
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    return ansible.playbook.PlayBook(
        playbook=playbook_yml,
        host_list='inventory.py',  # set a dynamic inventory executable script
        extra_vars=extra_vars,
        stats=stats,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        # if check=True,will run test
        check=False)


def run():
    # extra_vars define in playbook_yml
    extra_vars = {"key1": "value1", "key2": "value2" ...}
    return playbook("path-to-your-playbook.yml", extra_vars).run()


if __name__ == '__main__':
    print(run())
