import collections

import pytest

from cfme.utils import log
from cfme.utils.appliance import get_or_create_current_appliance

def pytest_sessionfinish(session, exitstatus):
    c = collections.Counter()
    results = ['total: {}'.format(sum(c.values()))] + map(
        lambda n: '{}: {}'.format(n[0], n[1]), c.items())
