def fill_cryosleep(df):
    
    num_nulls = df.isna()['CryoSleep'].sum()
    print(f'{num_nulls} Initially')
    
    # Anyone spending money isn't in CryoSleep
    df.loc[(df['CryoSleep'].isna())&(df['total_spend']>0),['CryoSleep']] = 0
    num_nulls = df.isna()['CryoSleep'].sum()
    print(f'{num_nulls} After Step 1: Spending Money = No CryoSleep')
    
    # Zero spend for only passenger in group
    df.loc[(df['CryoSleep'].isna())&(df['num_group_max']==1)&(df['total_spend']==0),['CryoSleep']] = 1
    num_nulls = df.isna()['CryoSleep'].sum()
    print(f'{num_nulls} After Step 2: 1 Passenger / Zero Spend = CryoSleep')
    
    # Groups with zero total spend
    df.loc[(df['CryoSleep'].isna())&(df['total_spend_max']==0),['CryoSleep']] = 1
    num_nulls = df.isna()['CryoSleep'].sum()
    print(f'{num_nulls} After Step 3: Total Group Spend Zero = CryoSleep')
    
    # Groups with total spend >0
    df.loc[(df['CryoSleep'].isna())&(df['total_spend_max']>0),['CryoSleep']] = 0
    num_nulls = df.isna()['CryoSleep'].sum()
    print(f'{num_nulls} After Step 4: Total Group Spend > Zero = No CryoSleep')
    
    return df

def check_pass_group(df,group_num):
    return df[df['PassengerId'].apply(lambda x: str(x[:4]))==group_num]

def basic_prep(df,spend_cols):
    import pandas as pd
    import numpy as np
    
    df[['deck', 'number', 'side']] = pd.DataFrame(
        df.Cabin.apply(lambda x: str(x).split('/')).tolist(),
        index= df.index,
        columns=['deck', 'number', 'side'],
    )
    # PassengerId follows XXXX_XX structure for all
    df['passenger_group'] = df['PassengerId'].apply(lambda x: str(x[:4]))
    df['num_group'] = df['PassengerId'].apply(lambda x: x[-2:])
    
    df['total_spend'] = df[spend_cols].sum(axis=1)
    df = df.join(df.groupby('passenger_group')\
                   .agg({'total_spend':'sum','num_group':'max'}),on='passenger_group',rsuffix='_max')
    df['num_group_max'] = df['num_group_max'].astype('int')
    
    df['surname'] = df[df['Name'].notna()].Name.apply(lambda x: str(x).split(" ")[-1])
    
    df.replace({'nan':np.nan},inplace=True) # Needed, since split above creates "nan"
    df.number = df.number.astype(float)


    # Setting up error handling as test_df doesn't have "Transported"
    try:
        df["Transported"] = df["Transported"].replace({True: 1, False: 0})
    except:
        pass
    return df

def fill_missing_basic(df, float_cols, object_cols, spend_cols):
    df[spend_cols] = df[spend_cols].fillna(df[spend_cols].mean())
    df[float_cols] = df[float_cols].fillna(df[float_cols].mean().to_dict())
    object_dict = {k:v[0] for k, v in df[object_cols].mode().to_dict().items()}
    df[object_cols] = df[object_cols].fillna(object_dict)
    return df

def fill_homeplanet(df):
    
    num_nulls = df.isna()['HomePlanet'].sum()
    print(f'{num_nulls} Initially')
    
    home_planet = df.loc[~df['HomePlanet'].isna()][['passenger_group','HomePlanet']]
    
    df.loc[df['HomePlanet'].isna(),['HomePlanet']] = df.passenger_group.map(home_planet.set_index('passenger_group').to_dict()['HomePlanet'])
    num_nulls = df.isna()['HomePlanet'].sum()
    print(f'{num_nulls} after filling passenger groups')
    
    # If passengers are on decks A,B,C they always are coming from Europa
    df.loc[(df['HomePlanet'].isna())&(df['deck'].isin(['A','B','C','T'])),['HomePlanet']] = 'Europa'
    num_nulls = df.isna()['HomePlanet'].sum()
    print(f'{num_nulls} after filling Europa decks')
    
    # If passengers are on deck G they always are coming from Europa
    df.loc[(df['HomePlanet'].isna())&(df['deck'].isin(['G'])),['HomePlanet']] = 'Earth'
    num_nulls = df.isna()['HomePlanet'].sum()
    print(f'{num_nulls} after filling Earth decks')
    
    # Filling the rest with Earth
    df.loc[(df['HomePlanet'].isna()),['HomePlanet']] = 'Earth'
    num_nulls = df.isna()['HomePlanet'].sum()
    print(f'{num_nulls} after filling the rest with Earth')
    
    return df


def random_null_assignment(df,discrete_variables):

    for variable in discrete_variables:
        # Getting MISSING indexes to fill with new values
        missing_indexes = (df[df[variable]=='nan'].index | df[df[variable].isna()].index)

        # Creating new array with counts for each non-missing value
        non_missing_values = df[df[variable]!='nan'].groupby(by=variable).count()['PassengerId']

        # Setting options to fill missing values with
        value_options = list(non_missing_values.index)

        # Setting probabilities for random function to assign values
        value_mix = [x/sum(non_missing_values.values) for x in non_missing_values.values]

        # Creating array of values to populate
        missing_values = np.random.choice(value_options,len(missing_indexes), p=value_mix)

        # Assign values based on index of missing values and new values array
        df.loc[missing_indexes,variable] = missing_values
    
    return df

def feature_transformation(df):

    cat_df = pd.get_dummies(df[discrete_variables], drop_first=False)
    
    # define min max scaler
    scaler = MinMaxScaler()
    # transform data
    num_df = pd.DataFrame(scaler.fit_transform(df[numeric_variables]),columns=numeric_variables)
    
    final_df = pd.merge(df,num_df,left_index=True,right_index=True)
    
    return final_df

def plot_feature_importance(importance,names,model_type):
    
    #Create arrays from feature importance and feature names
    feature_importance = np.array(importance)
    feature_names = np.array(names)
    
    #Create a DataFrame using a Dictionary
    data={'feature_names':feature_names,'feature_importance':feature_importance}
    fi_df = pd.DataFrame(data)
    
    #Sort the DataFrame in order decreasing feature importance
    fi_df.sort_values(by=['feature_importance'], ascending=False,inplace=True)
    
    #Define size of bar plot
    plt.figure(figsize=(10,8))
    #Plot Searborn bar chart
    sns.barplot(x=fi_df['feature_importance'], y=fi_df['feature_names'])
    #Add chart labels
    plt.title(model_type + ' FEATURE IMPORTANCE')
    plt.xlabel('FEATURE IMPORTANCE')
    plt.ylabel('FEATURE NAMES')