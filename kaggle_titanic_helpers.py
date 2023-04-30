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