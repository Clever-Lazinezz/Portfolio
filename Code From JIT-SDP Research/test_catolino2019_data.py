import logging
from numbers import Number
from catolino2019 import Catolino2019Dataset


logger = logging.getLogger(__name__)
logger.debug('Logger is ' + __name__)


def test_list_projects():
    project_list = Catolino2019Dataset.list_projects()
    logger.debug(f'project_list is {list(project_list)}')
    assert project_list == ['aFall', 'Alfresco', 'androidSync', 'androidWalpaper', 'anySoftKeyboard', 'Apg', 'Applozic', 'atmosphere', 'chatSecure', 'delta_chat', 'facebook', 'image', 'kiwis', 'lottie', 'ObservableScrollView', 'owncloudandroid', 'Pageturner', 'reddit', 'telegram']


def test_list_attributes():
    attribute_list = Catolino2019Dataset.list_attributes()
    logger.debug(f'attribute_list is {attribute_list}')
    assert set(attribute_list) == set(['contains_bug',
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
    feature_list = Catolino2019Dataset.list_features(type='as_is')
    logger.debug(f'feature_list is {list(feature_list)}')
    assert set(feature_list) == set(['contains_bug',
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
    label = Catolino2019Dataset.get_label_attribute()
    assert label == 'contains_bug'


def test_get_as_is_data():
    dataset = Catolino2019Dataset('download/data/catolino2019')
    for project in dataset.list_projects():
        df = dataset.get_as_is_data(project)
        assert df is not None

# 03/05/2023 - issue with _denormalize in dataset file
def test_get_raw_data():
    dataset = Catolino2019Dataset('download/data/catolino2019')
    for project in dataset.list_projects():
        df = dataset.get_raw_data(project) # issue location
        assert df is not None

        for attr in dataset.list_features(type='raw'):
            column = df[attr]
            assert isinstance(column.min(), Number)
            assert isinstance(column.max(), Number)
            assert isinstance(column.mean(), Number)
        column = df[dataset.get_label_attribute()]
        assert column.min() == 0
        assert column.max() == 1

# 03/05/2023 - issue with casting values
def test_get_extended_data():
    dataset = Catolino2019Dataset('download/data/catolino2019')
    for project in dataset.list_projects():
        df = dataset.get_extended_data(project) # issue location
        assert df is not None

        for attr in dataset.get_extended_feature_list():
            column = df[attr]
            assert isinstance(column.min(), Number)
            assert isinstance(column.max(), Number)
            assert isinstance(column.mean(), Number)
