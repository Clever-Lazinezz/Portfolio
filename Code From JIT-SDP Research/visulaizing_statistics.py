# import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import get_data_and_statistics as gds
import normalizing_data as nd
from fan2019 import Fan2019Dataset
from catolino2019 import Catolino2019Dataset
from kamei2012 import Kamei2012Dataset
from mcintosh2017 import Mcintosh2017Dataset

data_object_classes = [Fan2019Dataset, Catolino2019Dataset, Kamei2012Dataset, Mcintosh2017Dataset]


# print(gds.complete_computed_statistics_list())
"""
Description: This function retrieves four dataframes, uniformized to share column names,
and plots their raw unnormalized means for each attribute against each other.
Input: None
Output: graphs
"""
def mean_of_uniform_attributes_graphes() -> None:

    individual_complete_project = gds.gather_joined_projects()
    gds.make_data_uniform(individual_complete_project)
    # print(individual_complete_project[2].value_counts())
    # print(gds.individual_computed_statistics_list())
    df1 = individual_complete_project[0]
    df2 = individual_complete_project[1]
    df3 = individual_complete_project[2]
    df4 = individual_complete_project[3]


    for attribute in gds.UNIFORM_ATTRIBUTES:
        means1 = df1[attribute].mean()
        means2 = df2[attribute].mean()
        means3 = df3[attribute].mean()
        means4 = df4[attribute].mean()

        plt.plot(means1, 'o', label='Fan')
        plt.plot(means2, 'o', label='Catolino')
        plt.plot(means3, 'o', label='Kamei')
        plt.plot(means4, 'o', label='Mcintosh')
        plt.xlabel(attribute)
        plt.ylabel('Means')
        title = 'Mean of ' + attribute + " for all DataFrames"
        plt.title(title)
        plt.legend()
        plt.show()


"""
Description: This function uniformizes data from all datasets, and creates histograms for
each attribute of a chosen project.
Input: project name(String)
Output: graphs
"""
def visual_attributes_distribution(project) -> None:
    project_dict = {'Fan2019' : 0, 'Catolino2019' : 1, 'Kamei2012' : 2, 'Mcintosh2017' : 3,
                    'fan2019' : 0, 'catolino2019' : 1, 'kamei2012' : 2, 'mcintosh2017' : 3,
                    'fan' : 0, 'catolino' : 1, 'kamei' : 2, 'mcintosh' : 3,
                    'f' : 0, 'c' : 1, 'k' : 2, 'm' : 3}
    project_num = project_dict.get(project)

    print('Visualizing the attribute distribution for project:', project)
    individual_complete_project = gds.gather_joined_projects()
    gds.make_data_uniform(individual_complete_project)
    target_project = individual_complete_project[project_num]
    # nd.fan2019_normilization(target_project)
    #target_project = target_project.describe().iloc[3:8]
    #print(target_project)

    #plt.plot(target_project['nf'], 'o')
    for attribute in gds.UNIFORM_ATTRIBUTES:
        plt.hist(target_project[attribute], 50, density=True)
        xlabel = 'Distribution of ' + attribute
        plt.xlabel(xlabel)
        # plt.ylabel('Y Label')
        title = attribute + ' distribution'
        plt.title(title)

        plt.show()


visual_attributes_distribution('f')

