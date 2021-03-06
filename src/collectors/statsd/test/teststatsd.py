#!/usr/bin/python
# coding=utf-8
###############################################################################
from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from diamond.collector import Collector
from statsd import StatsdCollector, _transform_metric_name, ListenerThread
from mock import patch

###############################################################################


class TestStatsdCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('StatsdCollector', {})
        self.collector = StatsdCollector(config, None)

    def test_import(self):
        self.assertTrue(StatsdCollector)

    def test_clean_key(self):
        self.assertEqual(_transform_metric_name('test/this/key'), 'test-this-key')
        self.assertEqual(_transform_metric_name('test key'), 'test_key')
        self.assertEqual(_transform_metric_name('normal_key'), 'normal_key')
        self.assertEqual(_transform_metric_name('@special-remove@'), 'special-remove')
        self.assertEqual(_transform_metric_name('normal.key'), 'normal.key')

    @patch.object(Collector, 'publish')
    def test_publish_metrics(self, publish_mock):

        self.collector.start_listener()
        self.collector.listener_thread.parse_metrics('gorets:1|c\nglork:320|ms\ngaugor:333|g\ngorets:1|c\nglork:100|ms')
        self.collector.stop_listener()

        metrics = {
        'gaugor': 333.0,
        'glork_mean': 0.210,
        'glork_min': 0.1,
        'glork_max': .320,
        'glork_count': 2.0,
        'glork_90.0pct': 0.1,
        'gorets': 0.00066666667,
        }

        self.assertPublishedMany(publish_mock, metrics)


###############################################################################
if __name__ == "__main__":
    unittest.main()

