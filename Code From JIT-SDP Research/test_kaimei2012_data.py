import logging
from numbers import Number
from kamei2012 import Kamei2012Dataset


logger = logging.getLogger(__name__)
logger.debug('Logger is ' + __name__)


def test_list_projects():
    project_list = Kamei2012Dataset.list_projects()
    logger.debug(f'project_list is {list(project_list)}')
    assert project_list == ['bugzilla',  'columba', 'jdt', 'mozilla', 'platform', 'postgres']


def test_list_attributes():
    attribute_list = Kamei2012Dataset.list_attributes()
    logger.debug(f'attribute_list is {attribute_list}')
    assert set(attribute_list) == set(['transactionid',
                                       'commitdate',
                                       'ns',
                                       'nm',
                                       'nf',
                                       'entropy',
                                       'la',
                                       'ld',
                                       'lt',
                                       'fix',
                                       'ndev',
                                       'pd',
                                       'npt',
                                       'exp',
                                       'rexp',
                                       'sexp',
                                       'bug'])


def test_list_features():
    feature_list = Kamei2012Dataset.list_features(type='as_is')
    logger.debug(f'feature_list is {list(feature_list)}')
    assert set(feature_list) == set(['ns',
                                     'nm',
                                     'nf',
                                     'entropy',
                                     'la',
                                     'ld',
                                     'lt',
                                     'fix',
                                     'ndev',
                                     'pd',
                                     'npt',
                                     'exp',
                                     'rexp',
                                     'sexp'])

def test_get_label_attribute():
    label = Kamei2012Dataset.get_label_attribute()
    assert label == 'bug'


def test_get_as_is_data():
    dataset = Kamei2012Dataset('download/data/kamei2012')
    for project in dataset.list_projects():
        df = dataset.get_as_is_data(project)
        assert df is not None

def test_get_raw_data():
    dataset = Kamei2012Dataset('download/data/kamei2012')
    for project in dataset.list_projects():
        df = dataset.get_raw_data(project)
        assert df is not None

        for attr in dataset.list_features(type='raw'):
            column = df[attr]
            assert isinstance(column.min(), Number)
            assert isinstance(column.max(), Number)
            assert isinstance(column.mean(), Number)
        column = df[dataset.get_label_attribute()]
        assert column.min() == 0
        assert column.max() == 1


def test_get_extended_data():
    dataset = Kamei2012Dataset('download/data/kamei2012')
    for project in dataset.list_projects():
        df = dataset.get_extended_data(project)
        assert df is not None

        for attr in dataset.get_extended_feature_list():
            column = df[attr]
            assert isinstance(column.min(), Number)
            assert isinstance(column.max(), Number)
            assert isinstance(column.mean(), Number)
