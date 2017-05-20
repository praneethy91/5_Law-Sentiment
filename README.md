# Causal Inference - The Effect of Circuit Court Decisions on Social Attitudes

## Abstract
We present an application of machine learning and causal inference to study the
effect on social and political attitude of the public, based on court rulings and characteristics of judges involved. Our goal is to determine if the sentiment of the judges
in the court rulings towards certain targets(like republicans, democrats, woman, femi-
nists, etc) is a factor through which we can infer the public opinion towards the same
targets. We not only use the judges sentiment towards these targets, but we also weight
the similarities to those targets using word2vec. We also use the biographical and
other characteristics of the judge(s) involved in the cases for determining this causal ef-
fect, by using them as instruments. Using them as instruments in 2-stage least squares
regression helps to ensure that this determined causal effect is infact consistent and
unbiased. We also find which of these characteristics are important as instruments,
using different feature selection methods. We use American National Election Survey data, Court rulings data, and judge
characteristics data for this analysis into the causal effect.

## Poster Presentation
[Project poster](https://github.com/praneethy91/5_Law-Sentiment/blob/master/Poster.pdf)

## Project Report
[Project report](https://github.com/praneethy91/5_Law-Sentiment/blob/master/project-report.pdf)
