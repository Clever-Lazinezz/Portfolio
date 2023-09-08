# %%
import os
import pandas as pd
# import matplotlib.pyplot as plt
# import sys
# sys.path.append("/Users/clever_lazinezz/JITSDPStratified/src/dataset")

# DO NOT CHANGE ORDER OF PATHWAYS - ORDER USED FOR SOME FUNCTIONS
project_directories = ['/Users/clever_lazinezz/JITSDPStratified/download/data/fan2019/data_results/data_csvs2',
                       '/Users/clever_lazinezz/JITSDPStratified/download/data/catolino2019/input_data',
                       '/Users/clever_lazinezz/JITSDPStratified/download/data/kamei2012/input',
                       '/Users/clever_lazinezz/JITSDPStratified/download/data/mcintosh2017/data']

PROJECT_ORDER = ['fan2019', 'catolino2019', 'kamei2012', 'mcintosh2017']

UNIFORM_ATTRIBUTES = [  'ns',
                        'nd',
                        'nf',
                        'entropy',
                        'la',
                        'ld',
                        'ndev',
                        'age',
                        'nuc',
                        'rexp'] # last change here 05/11/23

COLS_ORDER = [  'bug',
                'fix',
                'ns',
                'nd',
                'nf',
                'entropy',
                'la',
                'ld',
                'ndev',
                'age',
                'nuc',
                'rexp']

"""
Description: This function reads in all the files from a given os path as a csv file into a list.
Input: target directory os pathway
Output: list of pd.Dataframes
"""
def get_projects_as_dataframe(directory) -> list:
    dataset_files = []
    dataframe_of_files = []
    for project in os.listdir(directory):
        project_path = os.path.join(directory, project)
        if os.path.isfile(project_path):
            dataset_files.append(project)
            dataframe_of_files.append(pd.read_csv(project_path))
   
    print("The following project csv files were read: ", dataset_files)
    return dataframe_of_files

# %%
"""
Description: Combines all project files from specific projects into a single dataframe. Each
pd.dataframe will be stored in a list. NO TRANSFORMATIONS OF ANY SORT SHOULD BE MADE TO THESE FILES!
Input: none
Output: list of pd.Dataframes
"""
def gather_joined_projects() -> list:
    complete_dataframe_list = []
    for directory in project_directories:
        combined_project_files = get_projects_as_dataframe(directory)
        complete_dataframe_list.append(combined_project_files)
    complete_combined_dataframe_list = []
    for projects in complete_dataframe_list:
        complete_combined_dataframe_list.append(pd.concat(projects, ignore_index=True))
    return complete_combined_dataframe_list


"""
Description: Transforms 'buggy' data to a 1 numerical value and 'clean to a 0 numerical value.
Unexpected cases return None.
Input: A String argument
Output: an integer(1 or 0)
"""
def transform_status_fan(status):
    if status == 'buggy':
        return 1
    elif status == 'clean':
        return 0
    else:
        return None


"""
Description:
Input: A numerical argument
Output: an integer(1 or 0)
"""
def transform_status_mcintosh(status):
    if status > 0:
        return 1
    elif status == 0:
        return 0
    else:
        return 0


"""
Description: DONE W/ INFO NEEDED
Input:
Output:
"""
def fan2019_transformations(df):
    """"
    Project Notes:
    -"Most of our change metrics are highly skewed, and to alleviate the effect of highly skewed values of the metrics, we
    apply a logarithmic transformation fol- lowing prior studies [37], [62]. And we use the standard log- arithmic
    transformation ln$x " 1%. Tantithamthavorn et al. demonstrated that correlated metrics can impact defect pre- diction
    models [70]. If the absolute correlation value between a pair of metrics is larger than 0.8, we keep the one that is
    easier to understand to ease model interpretation fol- lowing prior studies [37], [45]."
    ZERO non-null values
    buggy_B2, buggy_AG, buggy_MA, buggy_RA - all are objects - if 'buggy' then 1 else 0
    """
    
    df['buggy_B2'] = df['buggy_B2'].apply(lambda x: transform_status_fan(x))
    df['buggy_AG'] = df['buggy_AG'].apply(lambda x: transform_status_fan(x))
    df['buggy_MA'] = df['buggy_MA'].apply(lambda x: transform_status_fan(x))
   # article claimed this was the most accurate algorithm
    df['buggy_RA'] = df['buggy_RA'].apply(lambda x: transform_status_fan(x))

    # dropping columns only used in fan2019 + exp + sexp + lt
    df.drop(columns=['buggy_B2', 'buggy_AG', 'buggy_MA', 'exp', 'sexp', 'lt'], inplace=True)
    # changing column names to match the base standard, except contains_bug = bug
    df.rename(columns={'buggy_RA':'bug'}, inplace=True)
    # df = df.reindex(columns=COLS_ORDER)
    print("Grrr...fan")
"""
Description: DONE W/ INFO NEEDED
Input:
Output:
"""
def catolino2019_transformations(df):
    """"
    Project Notes:
    Nearly ZERO non-null values - lowest count is 28618/28648
    fix - only appears as 1 and 0
    """
    # dropping columns only used in catolino + exp + sexp + lt
    df.drop(columns=['exp', 'sexp', 'lt'], inplace=True)
    # changing column names to match the base standar(Catolino), except contains_bug = bug
    df.rename(columns={'contains_bug':'bug'}, inplace=True)
    df = df.reindex(columns=COLS_ORDER)
    print("Grrr...catolino")


"""
Description: DONE W/ INFO NEEDED
Input:
Output:
"""
def kamei2012_transformations(df):
    """"
    Project Notes[Page 8]:
    -"We found that NF and ND, and REXP and EXP are highly correlated. Therefore, we excluded ND and REXP7 from our model
    and instead used NF and EXP. Further- more, we found LA and LD to be highly correlated. Nagappan and Ball [46]
    reported that relative churn metrics perform better than absolute metrics when predicting defect density. Therefore,
    we normalized LA and LD by dividing by LT, similarly to Nagappan and Ball's approach. We also normalized LT and NUC
    by dividing by NF since these metrics have high correlation with NF. We also normalized LT and NUC by dividing by NF
    since these metrics have high correlation with NF." Standard log transformation applied to each metric(except FIX).
    -defect inducing changesets are small percentage of data
    -ZERO non-null values && and ZERO non-numerical values
    """
    # dropping columns only used in Kamei2012 + transactionid + exp + sexp + lt
    df.drop(columns=['transactionid', 'commitdate', 'exp', 'sexp', 'lt'], inplace=True)
    # changing column names to match the base standar(Catolino), except contains_bug = bug
    df.rename(columns={'nm':'nd', 'pd':'age', 'npt':'nuc'}, inplace=True)
    df = df.reindex(columns=COLS_ORDER)
    print("Grrr...kamei")

"""
Description: DONE W/ INFO NEEDED
Input:
Output:
"""
def mcintosh2017_transformations(df):
    """"
    Project Notes:
    -"We choose a rank correlation instead of other types of correlation (e.g., Pearson) because rank correlation is
    resilient to data that is not normally distributed. For sub-hierarchies of code change prop- erties with correlation
    |⇢| > 0.7, we select only one property from the sub-hierarchy for inclusion in our models"
    Bugcount - 6262/59009 non-null; if bugcount > 0 then 1; unique values - [ nan   0.   1.   2.   5.   3.   4.  39.  24.   6.  10.  23. 810.  28.
    37.   7.  97.  13.   9.  11.   8.  29.]
    Fixcount - 5237/59009 non-null
    """
    
    df['bugcount'] = df['bugcount'].apply(lambda x: transform_status_mcintosh(x))
    # dropping columns only used in Mcintosh2017 + commit_id
    df.drop(columns=['author_date', 'commit_id', 'fixcount', 'revd', 'nrev', 'rtime', 'tcmt', 'hcmt', 'self', 'app', 'arexp', 'asexp', 'rexp', 'rrexp', 'rsexp', 'oexp', 'orexp', 'osexp', 'asawr', 'rsawr', 'osawr'], inplace=True)
    # changing column names to match the base standar(Catolino), except contains_bug = bug
    df.rename(columns={'ent':'entropy', 'aexp':'rexp', 'bugcount':'bug'}, inplace=True)
    df = df.reindex(columns=COLS_ORDER)
    print("Grrr...mcintosh")



"""
Description: 
Input: pd.Dataframe
Output: None
"""
def make_data_uniform(df) -> None:
    fan2019_transformations(df[0])
    catolino2019_transformations(df[1])
    kamei2012_transformations(df[2])
    mcintosh2017_transformations(df[3])

"""
df = gather_joined_projects()
make_data_uniform(df)
mc = df[3]
mc.info()
mc['bug'].value_counts()
"""

# %%
"""
Description: Calls gather_joined_projects(), UNIFORMIZES data and transforms each project into statistical information
via pd.DataFrame.describe().
Input: none
Output: list of pd.Dataframes
"""
def individual_computed_statistics_list() -> list:
    individual_combined_dataframe_statistics_list = []
    df = gather_joined_projects()
    make_data_uniform(df)
    for project in df:
        individual_combined_dataframe_statistics_list.append(project.describe())
    return individual_combined_dataframe_statistics_list




# %%
"""
Description: THIS METHOD DOES NOT UNIFORMIZE NOR NORMALIZE DATA; BEST USED WHEN ALL DATA IS NORMALIZED TO SHARE THE SAME NAME FOR EQUVALENT ATTRIBUTES!
Calls get_projects_as_dataframe() and merges them all into a single dataframe, then prints statistical
information about the dataframe, and returns the merged dataframe.
Input: None
Output: pandas.DataFrame
"""
def complete_computed_statistics_list() -> list:
    df = gather_joined_projects()
    complete_combined_dataframe_statistics = pd.concat(df, ignore_index=True)
    #print(complete_combined_dataframe_statistics)
    #print("Computing the collective minimum, maximum, median, and mean for the following csv files: \n",df)
    #print(combined_project_dataframe.describe())

    return complete_combined_dataframe_statistics.describe()


# %%
# print(individual_computed_statistics_list()[0])