"""
Monitor filesize.

"""
import os
from newrelic_plugin_agent.plugins import base


class Filesize(base.Plugin):
    GUID = 'com.meetme.newrelic_filesize_agent'

    def add_datapoints(self, stats):
        """Extend this method to process the data points retrieved during the
        poll process.

        :param mixed data: The data received during the poll process

        """
        for key in stats:
            self.add_gauge_value(key, 'bytes', stats[key])

    def poll(self):
        """Poll the server returning the results in the expected component
        format.

        """
        self.initialize()
        stats = {}
        for fname in self.config.get('filenames', list()):
            size = 0
            if os.access(fname, os.F_OK):
                size = os.stat(fname).st_size
            stats[fname[fname.rfind('/')+1:]] = size
        self.add_datapoints(stats)
        self.finish()
