packnames = ('fitzRoy','dplyr')
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import pandas as pd

pandas2ri.activate()

base = importr('base')
utils = importr('utils')
utils.chooseCRANmirror(ind=1)

names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
if len(names_to_install) > 0:
    print(names_to_install)
    utils.install_packages(StrVector(names_to_install))


data = robjects.r('''
                  library(fitzRoy)
                  p_data22 = fetch_player_stats(2022)
                  p_data23 = fetch_player_stats(2023)''')

p_data22 = pandas2ri.rpy2py_dataframe(robjects.r['p_data22'])
p_data23 = pandas2ri.rpy2py_dataframe(robjects.r['p_data23'])
print(p_data22)