# Statistical-Analysis-of-Social-Media-Dataset-Exploration

Exploring Data: Summary Statistics & Statistical Testing



📌 Overview

This exercise focuses on summary statistics, data transformations, and hypothesis testing using Python. The tasks include:

Summary Statistics - Computing key metrics for given datasets.

Reddit Weekends Analysis - Investigating comment activity trends on weekdays vs weekends using statistical tests.

📊 Task 1: Summary Statistics

Objective

Analyze multiple datasets and compute key statistical measures.

📂 Input Files

data-*.csv: Various datasets containing numerical values.

🛠 Process

Compute mean, standard deviation, and range (min & max) for both variables.

Calculate the correlation coefficient (r-value) between the two variables.

Write a one-sentence description summarizing the dataset.

Document findings in summary.txt.

🚀 Running the Notebook

Use summary.ipynb to compute all statistics.

No specific output format required.

📅 Task 2: Reddit Weekends Analysis

Objective

Determine if there are significant differences in Reddit comment activity between weekdays and weekends.

📂 Input File

reddit-counts.json.gz: Contains daily comment counts for various Canadian subreddits.

🛠 Process

Filter Data

Use data from 2012 and 2013.

Extract data for /r/canada subreddit.

Separate weekdays and weekends based on date.weekday().

Statistical Tests

Perform a T-test to check for significant differences in comment volume.

Verify normality and equal variance using stats.normaltest and stats.levene.

Apply data transformation (log, sqrt, etc.) if needed.

Use Mann–Whitney U-test as a non-parametric alternative.

Apply Central Limit Theorem

Aggregate data by week number and take means.

Re-evaluate normality and conduct statistical tests.
