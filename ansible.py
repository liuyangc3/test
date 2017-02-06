# -*- coding:utf-8 -*-
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


Options = namedtuple('Options',
                     ['connection', 'forks', 'become', 'check', 'verbosity'])


class PlayBook(object):
    def __init__(self, playbook, inventory):
        # initialize needed objects
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.options = Options(connection='smart', forks=10, become=None, check=False, verbosity=0)

        # # Instantiate our ResultCallback for handling results as they come in
        # self.results_callback = ResultCallback()

        # create inventory and pass to var manager
        self.inventory = Inventory(loader=self.loader,
                                   variable_manager=self.variable_manager, host_list=inventory)
        self.variable_manager.set_inventory(inventory)

        self.pbex = PlaybookExecutor(playbooks=[playbook],
                                     inventory=self.inventory,
                                     loader=self.loader,
                                     variable_manager=self.variable_manager,
                                     options=self.options,
                                     passwords=None)
        self.pbex._tqm._stdout_callback = ResultCallback()
        
    def run(self):
        results = self.pbex.run()
        return results


