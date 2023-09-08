import os
import pandas as pd
from typing import Iterable


class Catolino2019Dataset(object):
    __PROJECT_DATA_DIR = os.path.join('data')
    __PROJECT_LIST = ['aFall', 'Alfresco', 'androidSync', 'androidWalpaper', 'anySoftKeyboard', 'Apg', 'Applozic', 'atmosphere', 'chatSecure', 'delta_chat', 'facebook', 'image', 'kiwis', 'lottie', 'ObservableScrollView', 'owncloudandroid', 'Pageturner', 'reddit', 'telegram']
    __ATTRIBUTE_INFO = {
        'contains_bug': 'Is this a defect-inducing changeset?',
        'fix': 'Is this a defect-fixing changeset? (FIX)',
        'ns': 'NS, number of modified subsystems (e.g., a subsystem is a package root in some software systems, i.e., '
              'org.eclipse.jdt.core is the system if org.eclipse.jdt.core/jdom/org/eclipse/jdt/core/dom/Node.java is '
              'being modified)',
        'nd': 'ND, number of modified directories (e.g., org.eclipse.jdt.core/jdom/org/eclipse/jdt/core/dom/ is the '
              'directory if org.eclipse.jdt.core/jdom/org/eclipse/jdt/core/dom/Node.java is being modified)',
        'nf': 'NF, number of modified files (e.g., Node.java is file being modified)', 
        'entropy': 'entropy, distribution of modified code across each file, defined as $H(P) = -\\sum_{k=1}^n p_k * \\log_2 p_k. '
                   'where probabilities $1 \\ge p_k > 0$, $k = 1, 2, \\ldots, n$, $n$ is the number of files in the change, P is '
                   'a set of $p_k$, where $p_k$ is the proportion that $file_k$ is modified in a change and \\sum_{k=1}^n p_k = 1 '
                   'If, for example, a change modifies three different files, A, B, and C and the number of modified lines in '
                   'files A, B, and C is 30, 20, and 10 lines, respectively, then the Entropy is measured as approximlately '
                   '$1.46 = - 30/60 \\log_2 30/60 - 20/60 \\log_2 20/60 - 10/60 \\log_2 10/60$. In the as-is data, entropy is '
                   'is normalized by NF if $NF \\ge 2$, i.e., entropy = ENTROPY/log_2(NF)',
        'la': 'LA, lines added, in the as-is data, la is normalized by LT, i.e., LA/LT',
        'ld': 'LD, lines deleted, in the as-is data, ld is normalized by LT, i.e. LD/LT',
        'lt': 'LT, lines of code in a file before the change, in the as-is data, lt is normalized by NF, i.e., LT/NF',
        'ndev': 'NDEV, the number of developers that previously changed the touched files. For example, if a change has files '
                'A, B, and C, file A thus far has been modified by developer x, and files B and C have been modified by '
                'developers x and y, then NDEV would be 2 (x and y).',
        'age': 'AGE, the average time interval between the current and the last time these files were modified. For '
              'example, if file A was last modified 3 days ago, file B was modified 5 days ago, and file C was modified 4 '
              'days ago, then AGE is calculated as 4 = (3+5+4)/3.',
        'nuc': 'NUC, the number of unique last changes of the modified files. For example, if file A was previously '
               'modified in change $\alpha$ and files B and C were modified in change $\beta$, then NUC is 2 (i.e., changes '
               '$\alpha$ and $\beta$). In the as-is data, npt is normalized by NF, i.e., NPT/NF',
        'exp': 'EXP, developer experience (EXP) is measured as the number of changes made by the developer before the current '
               'change.',
        'rexp': 'REXP, recent experience (REXP) is measured as the total experience of the developer in terms of changes, '
                'weighted by their age. It gives a higher weight to changes that are more recent. ',
        'sexp': 'SEXP, Subsystem experience (SEXP) measures the number of changes the developer made in the past to the '
                'subsystems that are modified by the current change.'
    }
    __LABEL = 'contains_bug'
    __AS_IS_FEATURE_LIST = [
        'contains_bug',
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
        'sexp'
    ]
    __RAW_FEATURE_LIST = [
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
        'sexp'       
    ]
    __EXTENDED_FEAURE_LIST = ['churn'] # needs checking
    # __LABEL_MAPPER = {'clean': 0, 'buggy': 1} ----- already 0/1 needs checking
    __LABEL_LIST = ['contains_bug']

    def __init__(self, data_dir:str):
        if not os.path.exists(data_dir):
            raise FileNotFoundError('Catolino-2019 Dataset not found at {}'.format(data_dir))
        
        input_dir = os.path.join(data_dir, self.__PROJECT_DATA_DIR)            
        if not os.path.exists(input_dir):
            raise FileNotFoundError('Complete Catolino-2019 Dataset not found at {}'.format(data_dir))
        
        for project in self.__PROJECT_LIST:
            project_data_file = os.path.join(input_dir, project + '.csv')
            if not os.path.exists(project_data_file):
                raise FileNotFoundError('Complete Catolino-2019 Dataset not found at {}'.format(data_dir))

        self.__data_dir = data_dir
        self.__data_files = dict()
        for project in self.__PROJECT_LIST:
            self.__data_files[project] = os.path.join(self.__data_dir, self.__PROJECT_DATA_DIR, project + '.csv')

    @classmethod
    def list_projects(self) -> Iterable:
        return list(self.__PROJECT_LIST)

    @classmethod
    def list_attributes(self) -> Iterable:
        return self.__ATTRIBUTE_INFO.keys()

    @classmethod
    def list_features(self, type='as_is') -> Iterable: #check method
        if type == 'as_is':
            return self.__AS_IS_FEATURE_LIST
        elif type == 'raw':
            return self.__RAW_FEATURE_LIST
        elif type == 'extended':
            return self.__RAW_FEATURE_LIST + self.__EXTENDED_FEAURE_LIST
        else:
            raise ValueError('Argments type must be in {}'.format(['as_is', 'raw', 'extended']))

    @classmethod
    def get_label_attribute(self) -> str:
        return self.__LABEL


    @classmethod
    def get_extended_feature_list(self) -> Iterable:
        return self.__EXTENDED_FEAURE_LIST


    def get_as_is_data(self, project:str) -> pd.DataFrame:
        df = pd.read_csv(self.__data_files[project])
        return df   
    
    # NaN causing errors during casting 
    # why these particular transformations - how did you decide to process these specific columns
    def __denormalize(self, df): 
		# raw_data$lt <- raw_data$lt * raw_data$nf
        lt = df.apply(lambda row: row['lt']*row['nf'] if row['nf']>=1 else row['lt'], axis=1).round().astype('int')
        df.loc[:, 'lt'] = lt   
		# raw_data$nuc <- raw_data$nuc * raw_data$nf        
        nuc = df.apply(lambda row: row['nuc']*row['nf'] if row['nf']>=1 else row['nuc'], axis=1).round().astype('int')
        df.loc[:, 'nuc'] = nuc
    
    def get_raw_data(self, project) -> pd.DataFrame:
        df = self.get_as_is_data(project)
        self.__denormalize(df) # 03/05/2023 - issue with this function when called in text file
        return df


    def get_extended_data(self, project) -> pd.DataFrame:
        df = self.get_raw_data(project)
        # total_churn <- sum(test_data$real_la+test_data$real_ld)
        churn = df.apply(lambda row: row['la'] + row['ld'], axis=1)
        df.insert(0, 'churn', churn, allow_duplicates=False)
        return df