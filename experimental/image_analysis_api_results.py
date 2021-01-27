"""Ipython kernel to analyze API results at image level"""

import numpy as np
import pandas as pd

import scipy.stats as stats

from database import db_img_predict


def create_chi2_cross_table(df):
    r"""Convert DataFrame one-hot encoded to chi2 cross table

    Underlying assumption is only one-hot encoded columns are included in the
        input DataFrame

    :param df: DataFrame that is one-hot encode
    :return: DataFrame of chi2 cross table
    """
    df_chi = df.sum().to_frame('Yes')  # count the ones and convert to yes
    df_chi['No'] = df_chi.sum()[0] - df_chi['Yes']
    return df_chi


# define constants and import database:
classes_of_interest = ['american_express', 'chase', 'emirates_airlines',
                       'jp_morgan', 'us_open_tennis']
classes_normalization = [4, 2, 4, 2, 2]
df_cols_of_interest = ['area', 'clear', 'straight']

db_img_results = db_img_predict()
db_img_results()
db_img_results.df_analysis_filter(
    wid_upper_limit = 250, classes_of_interest = classes_of_interest
)
df = db_img_results.df_analysis

len(db_img_results.df)
df_logo_hot = pd.get_dummies(df['logo_class']).astype(float)

# number of images the logo(s) is present:
df_img_join = df_logo_hot.join(df['img_id'])
df_img_occ = pd.DataFrame()
for img_id in df_img_join['img_id'].unique():
    df_itr = pd.DataFrame()
    df_itr = df_img_join[df_img_join['img_id'] == img_id].apply(
        pd.value_counts).iloc[1].to_frame().transpose()
    df_itr['img_id'] = img_id
    df_img_occ = df_img_occ.append(df_itr, ignore_index=True)
df_img_occ.fillna(value=0, inplace=True)
# changing all value >1 to 1:
df_img_occ.replace(2,1,inplace=True)
df_img_occ.replace(3,1,inplace=True)
df_img_occ.drop('img_id', axis=1, inplace=True)
# normalize df_img_occ:
df_img_occ_norm = df_img_occ.div(classes_normalization, axis=1)

# testing if occurance of logo in an image is assoicated with location:
df_img_chi_cross = create_chi2_cross_table(df_img_occ_norm)
tup_img_chi_stat = stats.chi2_contingency(df_img_chi_cross)

print(f'Did the logo or logos occur in the image? :')
print(df_img_chi_cross)
print(f'p value for image occurances: {tup_img_chi_stat[1]}\n')
img_norm_sum = df_img_chi_cross['Yes'].sum()
print(f'Normalized total {img_norm_sum}\n Raw total: {len(df_img_occ_norm)}\n')

# use df_logo_hot defined above:
df_logo_hot_norm = df_logo_hot.div(classes_normalization, axis=1)

# testing if occurance of logo is assoicated with location:
df_logo_chi_cross = create_chi2_cross_table(df_logo_hot_norm)
tup_logo_chi_stat = stats.chi2_contingency(df_logo_chi_cross)

print(f'Occurrences of the logo (Yes = occurred) (No = not present):')
print(df_logo_chi_cross)
print(f'p value for image occurances: {tup_logo_chi_stat[1]}\n')
logo_norm_sum = df_logo_chi_cross['Yes'].sum()
print(f'Normalized total {logo_norm_sum}\n Raw total: {len(df_logo_hot)}\n')
