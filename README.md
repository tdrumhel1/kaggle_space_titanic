# kaggle_space_titanic

## Contributors: tyler.drumheller@gmail.com, joe.mac.1986@gmail.com

## Background:
This project is meant to be a great tutorial into Machine Learning (ML) methods, as well as, an opportunity to brush up on skills, ahead of taking on more complex projects. 

## File Structure
1. <b>spaceshiptitanic_joemac_first_sub.ipynb:</b> First, simplest implementation of the CatBoost Classifier model, with basic filling (mean or mode). 
2. <b>Tyler Catboost.ipynb:</b> Tyler's notebook using Catboost, and various methods for fixing values and improving model scores (except not actually improving them).
3. <b>XGBoost K-Means Imputed Implementation.ipynb:</b> Another notebook with various methods of creating an XG Boost Gradient Boosted model. Includes more sophisticated null value filling methods, as well as, GridSearch.
4. <b>Feature Exploration.ipynb:</b> Scratch notebook used to learn about features. 
5. <b>kaggle_titanic_helpers.py:</b> Various helper functions developed to re-use in multiple model notebooks. 

## Learnings from Data Exploration:
We did quite a bit of data exploration to try to uncover consistencies in features/missing values, and also understand which features potentially split the model best. This was all predicated by creating a few new features related to a passengers cabin, and what passenger group they were a part of. 

Feature Engineering (basic_prep function in kaggle_titanic_helpers.py):
1. Cabin follows a structure of deck/number/side, so all passengers with a cabin can also be split into three additional features. <b>Deck</b> and <b>Side</b> were important to the analysis, but number was not.
2. PassengerId follows a structure of <b>passengergroup_numgroup</b>. These were split to allow us to find connections between passengers in the same group. 
3. All passengers also got additional features for total group spend and max group size, based on what passenger_group they were in. 

Some Insights:
1. People in <b>CryoSleep</b> do not spend any money, or conversely, people who spent money, were not in CryoSleep. This helped fill in missing CryoSleep values. You can find details of how this works in the fill_cryosleep function, available in kaggle_titanic_helpers.py. 
2. People in the same passenger group all come from the same <b>HomePlanet</b>. Also, some ship decks exclusively had passengers from a single planet. For single passengers, not on exclusive decks, the mode (Earth) was used for filling. You can find details of how this works in the fill_homeplanet function, available in kaggle_titanic_helpers.py.
3. <b>CryoSleep</b> appears to be the best splitter for our target variable Transported, but didn't always become the most important feature in our models.
4. Most people tended to spend 0 or near zero, but there is along tail of extensive spend, which makes filling values with the mean inappropriate.

[Add Graphs?]

## Model Performance:
Surprisingly, model performance actually degraded from the initial basic CatBoost model. Any feature engineering, outside of basic filling, and scaling values didn't seem to be a better splitter for our target variable. We do know CatBoost uses internal techniques to handle scaling and outliers, and these techniques outperform any manual techniques deployed. 

## Where do we go from here?
<b>Feature Engineering:</b> Feature Engineering is the most important part of model development. As our models all hit a plateau around 80% accuracy, better feature engineering should allow us to develop better model performance. We think there are better ways to connect passengers to one another, which could provide better intuition into who gets transported. Coincidentally, all feature engineering we did performed worse than our base CatBoost model.
<b>Model Output Tuning:</b> We would love to take the output of our models and further tune the results either with algorithms, or another ML model, creating an ensemble model. We have seen anomalies in our data that the model doesn't pick up well (e.g. Passengers in entire group are transported when not in CrySleep, but are when in it. This goes against the basic idea that being in CryoSleep means you are more likely to be transported.)
