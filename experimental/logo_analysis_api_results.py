"""Ipython kernel to analyze data in df"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import scipy.stats as stats

from autil import get_data_paths, get_new_images, ipynb_kernel_used
import constants
from database import db_img_predict
from putil import display_box_plot, display_results, plot_dist


def calc_class_stats(df, df_col, ces_of_interest, ces_of_interest_display,
    plot=True):
    r"""Calculate class level statistics

    :param df: DataFrame
    :param df_col: str of column to calculate
    :param ces_of_interest: list of classes to plot on x axis
    :param ces_of_interest_display: list of classes to display as x axis labels

    :return: Series with mean of column
    :return: Series with standard deviation of column
    :return: Series with variance of column
    :return: float with minimum of column
    :return: float with maximum of column
    """
    S_class_mean = df.groupby('logo_class')[f'{df_col}'].mean()
    S_class_std = df.groupby('logo_class')[f'{df_col}'].std()
    S_class_var = df.groupby('logo_class')[f'{df_col}'].var()
    flt_min = df.groupby('logo_class')[f'{df_col}'].min()
    flt_max = df.groupby('logo_class')[f'{df_col}'].max()
    if plot:
        display_box_plot(df, df_col, ces_of_interest, ces_of_interest_display)
    return (S_class_mean, S_class_std, S_class_var, flt_min, flt_max)


# import needed data:
lst_ces_of_int = ['american_express', 'chase', 'emirates_airlines',
    'jp_morgan', 'us_open_tennis']
lst_ces_of_int_dis = ['American Express', 'Chase', 'Emirates Airlines',
    'JP Morgan', 'US Open Tennis']
df_cols_of_interest = ['area', 'clear', 'straight']

db_img_results = db_img_predict()
db_img_results()
db_img_results.df_analysis_filter(
    wid_upper_limit = 250, classes_of_interest = lst_ces_of_int
)
df = db_img_results.df_analysis

# %%
# determine if data is from a normal distribution using Shapiro-Wilk test:

print('H0: population is normally distributed. If p value less than 0.05 ',
    'H0 will be rejected.')
for df_col in df_cols_of_interest:
    for class_item in lst_ces_of_int:
        temp_store = None
        temp_store = stats.shapiro(df[df['logo_class'] == class_item][df_col])
        print(f'Results for {df_col}, {class_item}:\n',
            f'W value: {temp_store[0]} ; P value: {temp_store[1]}')

# results show distribution is not normal for any values

# show plots if visual validation needed:
# plot_dist(df, classes_of_interest, df_cols_of_interest)

# %%
# determine if data has a normal variance using Levene's test
print('\n\nH0: all input samples are from populations with equal variances. ',
    'If p value less than 0.5 H0 will be rejected.')
for df_col in df_cols_of_interest:
    lst_lst_data = [df[df_col][df['logo_class'] == c_of_i] for c_of_i in lst_ces_of_int]
    print(f'Equal variance results for {df_col}:')
    print(stats.levene(*lst_lst_data))

# results show that variances are not equal

# %%
# use Kruskal-Wallis H-test (non-parametric test anova alternative) due to
#   above findings
print('\n\nH0: distributions are not significantly different ',
    'If p value less than 0.5 H0 will be rejected.')
for df_col in df_cols_of_interest:
    lst_lst_data = [df[df_col][df['logo_class'] == c_of_i] for c_of_i in lst_ces_of_int]
    print(f'Stat test  {df_col}:')
    print(stats.kruskal(*lst_lst_data))

# results all seem to have significantly different distributions

# %%
# Conduct Dunn-Bonferroni post-hoc
import scikit_posthocs as sp
dunn_b_p_val = pd.Series()
for df_col in df_cols_of_interest:
    dunn_b_p_val[df_col] = sp.posthoc_dunn(
        df, val_col=df_col, group_col='logo_class', p_adjust='bonferroni'
    )
    print(f'Dunn-Bonferroni results for {df_col}:')
    print(dunn_b_p_val[df_col]['jp_morgan'])
# get means and std for reporting
df_img_results = pd.DataFrame()
for df_col in df_cols_of_interest:
    print(f'{df_col}:')
    dunn_b_p_val[df_col]
    (df_img_results[f'mean_{df_col}'], df_img_results[f'std_{df_col}'],
     _, _, _) = calc_class_stats(df, df_col, lst_ces_of_int,
                                 lst_ces_of_int_dis)
print(df_img_results)

df_img_results

# Notes:

# If multiple hypothesis are tested, the chance of observing a rare event
#  increases, and therefore, the likelihood of incorrectly rejecting a null
#  hypothesis (i.e., making a Type I error) increases.

# Bonferroni correction compensates for that increase by testing each
#  individual hypothesis at a significance level of
#  {\displaystyle \alpha /m}\alpha /m, where {\displaystyle \alpha }\alpha
#  is the desired overall alpha level and {\displaystyle m}m is the number of
#  hypotheses.
