# test_fan2019_data
import logging
from numbers import Number
from fan2019 import Fan2019Dataset


logger = logging.getLogger(__name__)
logger.debug('Logger is ' + __name__)


def test_list_projects():
    project_list = Fan2019Dataset.list_projects()
    logger.debug(f'project_list is {list(project_list)}')
    assert project_list == ['activemq', 'camel', 'derby', 'geronimo', 'hbase', 'hcommon', 'mahout', 'openjpa', 'pig', 'tuscany']


def test_list_attributes():
    attribute_list = Fan2019Dataset.list_attributes()
    logger.debug(f'attribute_list is {attribute_list}')
    assert set(attribute_list) == set(['buggy_B2',
                                        'buggy_AG',
                                        'buggy_MA',
                                        'buggy_RA',
                                        'ns',
                                        'nd',
                                        'nf',
                                        'entropy',
                                        'la',
                                        'ld',
                                        'lt',
                                        'fix',
                                        'ndev',
                                        'age',
                                        'nuc',
                                        'exp',
                                        'rexp',
                                        'sexp'])


def test_list_features():
    feature_list = Fan2019Dataset.list_features(type='as_is')
    logger.debug(f'feature_list is {list(feature_list)}')
    assert set(feature_list) == set(['buggy_B2',
                                    'buggy_AG',
                                    'buggy_MA',
                                    'buggy_RA',
                                    'ns',
                                    'nd',
                                    'nf',
                                    'entropy',
                                    'la',
                                    'ld',
                                    'lt',
                                    'fix',
                                    'ndev',
                                    'age',
                                    'nuc',
                                    'exp',
                                    'rexp',
                                    'sexp'])

def test_get_label_attribute():
    label = Fan2019Dataset.get_label_attribute()
    assert label == 'buggy_RA'


def test_get_as_is_data():
    dataset = Fan2019Dataset('download/data/fan2019')
    for project in dataset.list_projects():
        df = dataset.get_as_is_data(project)
        assert df is not None

def test_get_raw_data():
    dataset = Fan2019Dataset('download/data/fan2019')
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
    dataset = Fan2019Dataset('download/data/fan2019')
    for project in dataset.list_projects():
        df = dataset.get_extended_data(project)
        assert df is not None

        for attr in dataset.get_extended_feature_list():
            column = df[attr]
            assert isinstance(column.min(), Number)
            assert isinstance(column.max(), Number)
            assert isinstance(column.mean(), Number)
