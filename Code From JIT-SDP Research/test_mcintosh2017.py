import logging
from numbers import Number
from mcintosh2017 import Mcintosh2017Dataset


logger = logging.getLogger(__name__)
logger.debug('Logger is ' + __name__)


def test_list_projects():
    project_list = Mcintosh2017Dataset.list_projects()
    logger.debug(f'project_list is {list(project_list)}')
    assert project_list == ['openstack', 'qt']


def test_list_attributes():
    attribute_list = Mcintosh2017Dataset.list_attributes()
    logger.debug(f'attribute_list is {attribute_list}')
    assert set(attribute_list) == set(['commit_id',
                                        'author_date',
                                        'bugcount',
                                        'fixcount',
                                        'la',
                                        'ld',
                                        'nf',
                                        'nd',
                                        'ns',
                                        'ent',
                                        'revd',
                                        'nrev',
                                        'rtime',
                                        'tcmt',
                                        'hcmt',
                                        'self',
                                        'app',
                                        'ndev',
                                        'age',
                                        'nuc',
                                        'aexp',
                                        'arexp',
                                        'asexp',
                                        'rexp',
                                        'rrexp',
                                        'rsexp',
                                        'oexp',
                                        'orexp',
                                        'osexp',
                                        'asawr',
                                        'rsawr',
                                        'osawr',
                                        'lt',
                                        'fix',
                                        'exp',
                                        'sexp'])


def test_list_features():
    feature_list = Mcintosh2017Dataset.list_features(type='as_is')
    logger.debug(f'feature_list is {list(feature_list)}')
    assert set(feature_list) == set(['commit_id',
                                        'author_date',
                                        'bugcount',
                                        'fixcount',
                                        'la',
                                        'ld',
                                        'nf',
                                        'nd',
                                        'ns',
                                        'ent',
                                        'revd',
                                        'nrev',
                                        'rtime',
                                        'tcmt',
                                        'hcmt',
                                        'self',
                                        'app',
                                        'ndev',
                                        'age',
                                        'nuc',
                                        'aexp',
                                        'arexp',
                                        'asexp',
                                        'rexp',
                                        'rrexp',
                                        'rsexp',
                                        'oexp',
                                        'orexp',
                                        'osexp',
                                        'asawr',
                                        'rsawr',
                                        'osawr',
                                        'lt',
                                        'fix',
                                        'exp',
                                        'sexp'])

def test_get_label_attribute():
    label = Mcintosh2017Dataset.get_label_attribute()
    assert label == 'bugcount'


def test_get_as_is_data():
    dataset = Mcintosh2017Dataset('download/data/mcintosh2017')
    for project in dataset.list_projects():
        df = dataset.get_as_is_data(project)
        assert df is not None

# probable error - issue with _denormalize in dataset file
# currently does the same thing as test_get_as_is_data
def test_get_raw_data():
    dataset = Mcintosh2017Dataset('download/data/mcintosh2017')
    for project in dataset.list_projects():
        df = dataset.get_raw_data(project) # probable issue location
        assert df is not None
    """
        for attr in dataset.list_features(type='raw'):
            column = df[attr]
            assert isinstance(column.min(), Number)
            assert isinstance(column.max(), Number)
            assert isinstance(column.mean(), Number)
        column = df[dataset.get_label_attribute()]
        assert column.min() == 0
        assert column.max() == 1
    """

# not yet tested but probable - issue with casting values
def test_get_extended_data():
    dataset = Mcintosh2017Dataset('download/data/mcintosh2017')
    for project in dataset.list_projects():
        df = dataset.get_extended_data(project) # issue location
        assert df is not None

        for attr in dataset.get_extended_feature_list():
            column = df[attr]
            assert isinstance(column.min(), Number)
            assert isinstance(column.max(), Number)
            assert isinstance(column.mean(), Number)
