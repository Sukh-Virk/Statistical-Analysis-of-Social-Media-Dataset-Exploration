import sys
import pandas as pd
import numpy as np
from scipy import stats


OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)

def readdata(filepath):
    """Reads JSON data, filters for 'canada' subreddit, and categorizes weekdays vs. weekends."""
    dataf = pd.read_json(filepath, lines=True)

   
    beg, end = 2012, 2013
    dataf['date'] = pd.to_datetime(dataf['date'])
    dataf = dataf[(dataf['date'].dt.year >= beg) & (dataf['date'].dt.year <= end)]

   
    dataf = dataf[dataf['subreddit'] == 'canada']

   
    dataf['is_weekend'] = dataf['date'].dt.weekday >= 5 
    
    return dataf

def firsttest(weekdays, weekends):
    
    return {
        'initial_weekday_normality_p': stats.normaltest(weekdays).pvalue,

        'initial_weekend_normality_p': stats.normaltest(weekends).pvalue,

        'initial_ttest_p': stats.ttest_ind(weekdays, weekends).pvalue,

        'initial_levene_p': stats.levene(weekdays, weekends).pvalue
    }

def transtest(weekdays, weekends):
    
    trans_weekdays, trans_weekends = np.sqrt(weekdays), np.sqrt(weekends)
    return {
        'transformed_weekday_normality_p': stats.normaltest(trans_weekdays).pvalue,

        'transformed_weekend_normality_p': stats.normaltest(trans_weekends).pvalue,

        'transformed_levene_p': stats.levene(trans_weekdays, trans_weekends).pvalue
    }

def aggregate_weekly(cweekday, cweekend):
    

    weekd = cweekday.groupby(['iso_year', 'iso_week'])['comment_count'].mean().reset_index()

    weekend = cweekend.groupby(['iso_year', 'iso_week'])['comment_count'].mean().reset_index()


    weekdc = weekd['comment_count']
    weekendc = weekend['comment_count']

    return weekdc, weekendc

def weektest(c1_week_count, c2_week_count):
    
    return {
        'weekly_weekday_normality_p': stats.normaltest(c1_week_count).pvalue,

        'weekly_weekend_normality_p': stats.normaltest(c2_week_count).pvalue,

        'weekly_levene_p': stats.levene(c1_week_count, c2_week_count).pvalue,

        'weekly_ttest_p': stats.ttest_ind(c1_week_count, c2_week_count).pvalue
    }

def whitney(weekdays, weekends):
    
    return stats.mannwhitneyu(weekdays, weekends, alternative='two-sided').pvalue

def main():
    
    reddit_counts = sys.argv[1]

    counts = readdata(reddit_counts)

   
    counts_weekday = counts[~counts['is_weekend']].copy()

    counts_weekend = counts[counts['is_weekend']].copy()

  
    counts_weekday['iso_year'] = counts_weekday['date'].dt.isocalendar().year

    counts_weekday['iso_week'] = counts_weekday['date'].dt.isocalendar().week

    counts_weekend['iso_year'] = counts_weekend['date'].dt.isocalendar().year

    counts_weekend['iso_week'] = counts_weekend['date'].dt.isocalendar().week

    
    weekdays = counts_weekday['comment_count']

    weekends = counts_weekend['comment_count']

   
    it = firsttest(weekdays, weekends)

    tt = transtest(weekdays, weekends)


    
    weeklydays, weeklyends = aggregate_weekly(counts_weekday, counts_weekend)

    wt = weektest(weeklydays, weeklyends)
    
    
    whit = whitney(weekdays, weekends)

    
    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=it['initial_ttest_p'],
        initial_weekday_normality_p=it['initial_weekday_normality_p'],
        initial_weekend_normality_p=it['initial_weekend_normality_p'],
        initial_levene_p=it['initial_levene_p'],
        transformed_weekday_normality_p=tt['transformed_weekday_normality_p'],
        transformed_weekend_normality_p=tt['transformed_weekend_normality_p'],
        transformed_levene_p=tt['transformed_levene_p'],
        weekly_weekday_normality_p=wt['weekly_weekday_normality_p'],
        weekly_weekend_normality_p=wt['weekly_weekend_normality_p'],
        weekly_levene_p=wt['weekly_levene_p'],
        weekly_ttest_p=wt['weekly_ttest_p'],
        utest_p = whit,
    ))

if __name__ == '__main__':
    main()
