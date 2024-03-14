packnames = ('fitzRoy','dplyr')
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import pandas as pd
from afl_dashboard import styles

pandas2ri.activate()

base = importr('base')
utils = importr('utils')
utils.chooseCRANmirror(ind=1)

from afl_dashboard.templates import template

import reflex as rx
names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
if len(names_to_install) > 0:
    print(names_to_install)
    utils.install_packages(StrVector(names_to_install))


# data = robjects.r('''
#                 library(fitzRoy)
#                 p_data22 = fetch_player_stats(2022)
#                 #p_data23 = fetch_player_stats(2023)''')

#p_data22 = pandas2ri.rpy2py_dataframe(robjects.r['p_data22'])
#p_data22.to_parquet("C:/Users/Liam/Documents/afl_dashboard/afl_dashboard/data/p_data22.snappy.parquet",compression='snappy')
def make_clickable(val):
    return '<a href="{}">{}</a>'.format(val,val)

p_data22 = pd.read_parquet("C:/Users/Liam/Documents/afl_dashboard/afl_dashboard/data/p_data22.snappy.parquet")
p_data22['player.photoURL'] = p_data22['player.photoURL'].apply(make_clickable)
p_data22 = p_data22.iloc[:99,p_data22.columns.isin(['player.givenName','player.surname','team.name','player.photoURL'])]
p_data22 = p_data22.to_html(escape=False)

@template(route="/dashboard", title="Dashboard")
def db_main() -> rx.Component:
    
    #p_data23 = pandas2ri.rpy2py_dataframe(robjects.r['p_data23'])
    #rx.text(",".join(p_data22.columns))
    

    return rx.vstack(
        rx.heading("Dashboard", size="8"),
        rx.text("Welcome to Reflex!"),
        rx.data_table(data = p_data22,
                pagination = True,
                search = True,
                sort = True),
        rx.text(
            "You can edit this page in ",
            rx.code("{your_app}/pages/dashboard.py"),
        ),
    )