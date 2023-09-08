import logging
import numpy as np
import os
from typing import Iterable
import pandas as pd


logger = logging.getLogger(__name__)
logger.debug('Logger is ' + __name__)
logger.debug('CWD is ' + os.getcwd())


class Kamei2012Dataset(object):
    __PROJECT_LIST = ['bugzilla',  'columba', 'jdt', 'mozilla', 'platform', 'postgres']
    __PROJECT_DATA_DIR = os.path.join('input')
    __ATTRIBUTE_INFO = {
        'transactionid': 'CVS or Subservsion changeset id, where a changeset is a group of commits called a logical transaction', 
        'commitdate': 'Commit date of the changeset',
        'ns': 'NS, number of modified subsystems (e.g., a subsystem is a package root in some software systems, i.e., '
              'org.eclipse.jdt.core is the system if org.eclipse.jdt.core/jdom/org/eclipse/jdt/core/dom/Node.java is '
              'being modified)',
        'nm': 'formally ND, number of modified directories (e.g., org.eclipse.jdt.core/jdom/org/eclipse/jdt/core/dom/ is the '
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
        'fix': 'Is this a defect-fixing changeset? (FIX)',
        'ndev': 'NDEV, the number of developers that previously changed the touched files. For example, if a change has files '
                'A, B, and C, file A thus far has been modified by developer x, and files B and C have been modified by '
                'developers x and y, then NDEV would be 2 (x and y).',
        'pd': 'formally AGE, the average time interval between the current and the last time these files were modified. For '
              'example, if file A was last modified 3 days ago, file B was modified 5 days ago, and file C was modified 4 '
              'days ago, then AGE is calculated as 4 = (3+5+4)/3.',
        'npt': 'formally NUC, the number of unique last changes of the modified files. For example, if file A was previously '
               'modified in change $\alpha$ and files B and C were modified in change $\beta$, then NUC is 2 (i.e., changes '
               '$\alpha$ and $\beta$). In the as-is data, npt is normalized by NF, i.e., NPT/NF',
        'exp': 'EXP, developer experience (EXP) is measured as the number of changes made by the developer before the current '
               'change.',
        'rexp': 'REXP, recent experience (REXP) is measured as the total experience of the developer in terms of changes, '
                'weighted by their age. It gives a higher weight to changes that are more recent. ',
        'sexp': 'SEXP, Subsystem experience (SEXP) measures the number of changes the developer made in the past to the '
                'subsystems that are modified by the current change.',
        'bug': 'Is this a defect-introducing changeset?'
    }
    __LABEL = 'bug'
    __AUX_ATTRIBUTE_LIST = ['transactionid', 'commitdate']
    __AS_IS_FEATURE_LIST = [
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
    __EXTENDED_FEAURE_LIST = ['churn']
    __ATTRIBUTE_MAPPER = {
        'nm': 'nd', 
        'pd': 'age',
        'npt': 'nuc'
    }
    
    def __init__(self, data_dir:str):
        if not os.path.exists(data_dir):
            raise FileNotFoundError('Kamei-2012 Dataset not found at {}'.format(data_dir))
        
        input_dir = os.path.join(data_dir, self.__PROJECT_DATA_DIR)            
        if not os.path.exists(input_dir):
            raise FileNotFoundError('Complete Kamei-2012 Dataset not found at {}'.format(data_dir))
        
        for project in self.__PROJECT_LIST:
            project_data_file = os.path.join(input_dir, project + '.csv')
            if not os.path.exists(project_data_file):
                raise FileNotFoundError('Complete Kamei-2012 Dataset not found at {}'.format(data_dir))

        self.__data_dir = data_dir
        self.__data_files = dict()
        for project in self.__PROJECT_LIST:
            self.__data_files[project] = os.path.join(self.__data_dir, self.__PROJECT_DATA_DIR, project + '.csv')


    @classmethod
    def list_projects(self) -> Iterable:
        return list(self.__PROJECT_LIST)

    # @classmethod
    # def list_attributes(self, project: str) -> Iterable:
    #     if not project in self.__PROJECT_LIST:
    #         raise ValueError('Project {} not found in Kamei-2012 Dataset'.format(project))
        
    #     df = pd.read_csv(self.__data_files[project])
    #     return df.columns
    
    @classmethod
    def list_attributes(self) -> Iterable:
        return self.__ATTRIBUTE_INFO.keys()

    @classmethod
    def explain_attribute(self, attribute:str) -> str:
        if attribute not in self.__ATTRIBUTE_INFO.keys():
            raise ValueError('Attribute {} not found in Kamei-2012 Dataset'.format(attribute))
        
        return self.__ATTRIBUTE_INFO[attribute]
    
    
    @classmethod
    def list_features(self, type:str='as_is') -> Iterable:
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

    def __denormalize(self, df:pd.DataFrame):
        lt = df.apply(lambda row: row['lt']*row['nf'] if row['nf']>=1 else row['lt'], axis=1).round().astype('int')
        df['lt'] = lt

        la = df.apply(lambda row: row['la']*row['lt'] if row['lt']>=1 else row['la'], axis=1).round().astype('int')
        df['la'] = la

        ld = df.apply(lambda row: row['ld']*row['lt'] if row['lt']>=1 else row['ld'], axis=1).round().astype('int')
        df['ld'] = ld

        nuc = df.apply(lambda row: row['nuc']*row['nf'] if row['nf']>=1 else row['nuc'], axis=1).round().astype('int')
        df['nuc'] = nuc

        entropy = df.apply(lambda row: row['entropy']*np.log2(row['nf']) if row['nf']>=2 else row['entropy'], axis=1)
        df['entropy'] = entropy


    def __normalize(self, df:pd.DataFrame) -> None:
        pass
        #   idx.la <- charmatch(c("la"), colnames(data))
        #   tmp.la <- data["la"]/data["lt"]
        #   data[(data["lt"] >= 1), idx.la] <- tmp.la[(data["lt"] >= 1)]

        #   idx.ld <- charmatch(c("ld"), colnames(data))
        #   tmp.ld <- data["ld"]/data["lt"]
        #   data[(data["lt"] >= 1), idx.ld] <- tmp.ld[(data["lt"] >= 1)]

        #   idx.lt <- charmatch(c("lt"), colnames(data))
        #   tmp.lt <- data["lt"]/data["nf"]
        #   data[(data["nf"] >= 1), idx.lt] <- tmp.lt[(data["nf"] >= 1)]

        #   idx.npt <- charmatch(c("npt"), colnames(data))
        #   tmp.npt <- data["npt"]/data["nf"]
        #   data[(data["nf"] >= 1), idx.npt] <- tmp.npt[(data["nf"] >= 1)]

        #   # if the num of files is less than 2, entropy is not normalized
        #   idx.ent <- charmatch(c("entropy"), colnames(data))
        #   tmp.ent <- data["entropy"]/log(data["nf"],2)
        #   data[(data["nf"] >= 2), idx.ent] <- tmp.ent[(data["nf"] >= 2)]


    def get_raw_data(self, project:str) -> pd.DataFrame:
        df = self.get_as_is_data(project)
        df.rename(mapper=self.__ATTRIBUTE_MAPPER, axis=1, inplace=True)
        self.__denormalize(df)
        return df

    def get_extended_data(self, project:str) -> pd.DataFrame:
        df = self.get_raw_data(project)
        churn = df.apply(lambda row: row['la'] + row['ld'], axis=1)
        df.insert(0, 'churn', churn, allow_duplicates=False)
        return df

