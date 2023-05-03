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

def basic_prep(df):
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

def fill_missing_basic(df, float_cols, object_cols):
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