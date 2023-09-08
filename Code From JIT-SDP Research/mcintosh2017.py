import os
import pandas as pd
from typing import Iterable

class Mcintosh2017Dataset(object):
    __PROJECT_DATA_DIR = os.path.join('data')
    __PROJECT_LIST = ['openstack', 'qt']
    __ATTRIBUTE_INFO = {
        'commit_id': 'Commit SHA or git commit id, a changeset is a commit',
        'author_date': 'in Git, the author date is when someone first creates a commit with git commit',
        'bugcount': 'the number bugs/defects introduced by the changeset. buggy if bug count > 0; else clean',
        'fixcount': 'the number bugs/defects fixed by the changeset. fix = 1 if fixcount > 0',
        # size
        'la': 'LA, lines added, in the as-is data, la is normalized by LT, i.e., LA/LT',
        'ld': 'LD, lines deleted, in the as-is data, ld is normalized by LT, i.e. LD/LT',
        # diffusion
        'nf': 'NF, number of modified files (e.g., Node.java is file being modified)',
        'nd': 'number of modified directories/components (e.g., org.eclipse.jdt.core/jdom/org/eclipse/jdt/core/dom/ is the '
              'directory if org.eclipse.jdt.core/jdom/org/eclipse/jdt/core/dom/Node.java is being modified)',
        'ns': 'NS, number of modified subsystems (e.g., a subsystem is a package root in some software systems, i.e., '
              'org.eclipse.jdt.core is the system if org.eclipse.jdt.core/jdom/org/eclipse/jdt/core/dom/Node.java is '
              'being modified)',
        'ent': 'entropy, distribution of modified code across each file, defined as $H(P) = -\\sum_{k=1}^n p_k * \\log_2 p_k. '
                   'where probabilities $1 \\ge p_k > 0$, $k = 1, 2, \\ldots, n$, $n$ is the number of files in the change, P is '
                   'a set of $p_k$, where $p_k$ is the proportion that $file_k$ is modified in a change and \\sum_{k=1}^n p_k = 1 '
                   'If, for example, a change modifies three different files, A, B, and C and the number of modified lines in '
                   'files A, B, and C is 30, 20, and 10 lines, respectively, then the Entropy is measured as approximlately '
                   '$1.46 = - 30/60 \\log_2 30/60 - 20/60 \\log_2 20/60 - 10/60 \\log_2 10/60$. In the as-is data, entropy is '
                   'is normalized by NF if $NF \\ge 2$, i.e., entropy = ENTROPY/log_2(NF)',
        # Set review metrics for non-reviewed changes to NA
        # "nrev", "rtime", "hcmt", "self", "app", "rexp", "rrexp", "rsexp", "oexp", "orexp", "osexp"
        'revd': 'whether the changeset is reviewed, boolean, true or false',
        'nrev': 'review revisions, number of reviewers who have voted on whether a change should be integrated or abandoned',
        'rtime': 'review timespan/review window, the length of time between the creation of a review request and its final approval for integration.',
        'tcmt': 'not used, unclear what it is',
        'hcmt': 'Review comments, The number of non-automated, non-owner comments posted during the review of a change.',
        'self': 'self approval? true or false',
        'app':'reviewers, the number of reviewers',
        # History
        'ndev': 'NDEV, the number of developers that previously changed the touched files. For example, if a change has files '
                'A, B, and C, file A thus far has been modified by developer x, and files B and C have been modified by '
                'developers x and y, then NDEV would be 2 (x and y).',
        'age': 'time since last modification, the average time interval between the current and the last time these files were modified. For '
              'example, if file A was last modified 3 days ago, file B was modified 5 days ago, and file C was modified 4 '
              'days ago, then AGE is calculated as 4 = (3+5+4)/3.',
        'nuc': 'number of past changes, the number of unique last changes of the modified files. For example, if file A was previously '
               'modified in change $\alpha$ and files B and C were modified in change $\beta$, then NUC is 2 (i.e., changes '
               '$\alpha$ and $\beta$). In the as-is data, npt is normalized by NF, i.e., NPT/NF',
        # Experience
        'aexp': '*CALLED REXP IN KAMEI* et al. (2012), author experience, recent experience (REXP) is measured as the total experience '
                'of the author in terms of changes',
        'arexp': 'relative author experience, the number of prior changes that an author has participated in weighted by the age '
                 ' (in years) of the changes (older changes are given less weight than recent ones).',
        'asexp': 'subsystem author experience, is the number of past changes that an author has made to the subsystems that are being '
                 'modified by the change in question',
        'rexp': 'reviewer experience, author experience, reviewer experience (REXP) is measured as the total experience '
                'of the reviewers in terms of changes',
        'rrexp': 'Relative reviewer experience, the number of prior changes that a reviewer has participated in weighted by the age '
                 ' (in years) of the changes (older changes are given less weight than recent ones).',
        'rsexp': 'Subsystem reviewer experience, is the number of past changes that an reviewer has made to the subsystems that are being '
                 'modified by the change in question',
        'oexp': 'overall experience, recent experience (REXP) is measured as the total experience of an actor(author/reviwer) in '
                'terms of changes',
        'orexp': 'relative overall experience',
        'osexp': 'Subsystem overall experience, is the number of past changes that an actor (author/reviewer) has made to the '
                 'subsystems that are being modified by the change in question',
        # Awareness
        'asawr': 'author awareness, the proportion of past changes that were made to a subsystem that the author has authored or reviewed',
        'rsawr': 'reviewer awareness, the proportion of past changes that were made to a subsystem that the reviewer has authored or reviewed',
        'osawr': 'overall awareness, The proportion of the prior changes to the modified subsystem(s) that an actor (reviwer & author) has participated in. it should aways hold: osawr <= asawr + rsawr',
        'fix': 'Is this a defect-fixing changeset? (FIX)',
        'exp': 'EXP, developer experience (EXP) is measured as the number of changes made by the developer before the current change.',
        'sexp': 'SEXP, Subsystem experience (SEXP) measures the number of changes the developer made in the past to the subsystems that are modified by the current change.',
    }

    __LABEL = 'bugcount'
    __AUX_ATTRIBUTE_LIST = ['commit_id', 'author_date']
    __AS_IS_FEATURE_LIST = [
        'commit_id',
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
        'fix',
        'exp',
        'sexp'
    ]
    __RAW_FEATURE_LIST = [
        'commit_id',
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
        'fix',
        'exp',
        'sexp'
    ]
    __EXTENDED_FEAURE_LIST = ['churn'] # needs checking
    # __LABEL_MAPPER = {'clean': 0, 'buggy': 1} ----- already 0/1 needs checking
    __LABEL_LIST = ['bugcount, fixcount']

    def __init__(self, data_dir:str):
        if not os.path.exists(data_dir):
            raise FileNotFoundError('Mcintosh-2017 Dataset not found at {}'.format(data_dir))
        
        input_dir = os.path.join(data_dir, self.__PROJECT_DATA_DIR)            
        if not os.path.exists(input_dir):
            raise FileNotFoundError('Complete Mcintosh-2017 Dataset not found at {}'.format(data_dir))
        
        for project in self.__PROJECT_LIST:
            project_data_file = os.path.join(input_dir, project + '.csv')
            if not os.path.exists(project_data_file):
                raise FileNotFoundError('Complete Mcintosh-2017 Dataset not found at {}'.format(data_dir))

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


    """
    def __denormalize(self, df): 
        df['buggy_B2'] = df['buggy_B2'].apply(lambda x: 1 if x == 'buggy' else 'clean')
        df['buggy_AG'] = df['buggy_AG'].apply(lambda x: 1 if x == 'buggy' else 'clean')
        df['buggy_MA'] = df['buggy_MA'].apply(lambda x: 1 if x == 'buggy' else 'clean')
        df['buggy_RA'] = df['buggy_RA'].apply(lambda x: 1 if x == 'buggy' else 'clean')
    """

    def get_raw_data(self, project) -> pd.DataFrame:
        df = self.get_as_is_data(project)
        #self.__denormalize(df) # 03/05/2023 - issue with this function when called in text file
        return df


    def get_extended_data(self, project) -> pd.DataFrame:
        df = self.get_raw_data(project)
        # total_churn <- sum(test_data$real_la+test_data$real_ld)
        churn = df.apply(lambda row: row['la'] + row['ld'], axis=1)
        df.insert(0, 'churn', churn, allow_duplicates=False)
        return df