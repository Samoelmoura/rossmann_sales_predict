import pickle
import pandas as pd

class Rossmann(object):
    def __init__(self):
        # constant_competition_distance
        self.constant_competition_distance = pickle.load(constant_competition_distance, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\constant_competition_distance', 'rb'))

        # month_map
        self.month_map = pickle.load(month_map, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\month_map', 'rb'))

        # cols_filtering
        self.cols_filtering = pickle.load(cols_filtering, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\cols_filtering', 'rb'))

        # rs_competition_distance
        self.rs_competition_distance = pickle.load(rs_competition_distance, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\rs_competition_distance', 'rb'))

        # rs_competition_time_month
        self.rs_competition_time_month = pickle.load(rs_competition_time_month, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\rs_competition_time_month', 'rb'))

        # mm_promo2_time_week
        self.mm_promo2_time_week = pickle.load(mm_promo2_time_week, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\mm_promo2_time_week', 'rb'))

        # map_state_holiday
        self.map_state_holiday = pickle.load(map_state_holiday, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\map_state_holiday', 'rb'))

        # map_store_type
        self.map_store_type = pickle.load(map_store_type, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\map_store_type', 'rb'))
=
        # map_assortment
        self.map_assortment = pickle.load(map_assortment, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\map_assortment', 'rb'))

        # map_year
        self.map_year = pickle.load(map_year, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\map_year', 'rb'))

        # day_of_week_cicle
        self.day_of_week_cicle = pickle.load(day_of_week_cicle, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\day_of_week_cicle', 'rb'))

        # week_cicle
        self.week_cicle = pickle.load(week_cicle, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\week_cicle', 'rb'))

        # year_quarters_cicle
        self.year_quarters_cicle = pickle.load(year_quarters_cicle, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\year_quarters_cicle', 'rb'))

        # cols_feature_selection
        self.cols_feature_selection = pickle.load(cols_feature_selection, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\features\\cols_feature_selection', 'rb'))

        # xgb_fit
        self.model = pickle.load(xgb_fit, open('D:\\My Drive\\Pessoal\\Projetos\\rossmann_sales_predict\\src\\models\\xgb_fit', 'rb'))


    def data_cleaning(df1):
        snake_case = lambda x: inflection.underscore(x)

        cols_old = df1.columns.to_list()
        cols_new = list(map(snake_case, cols_old))

        # rename
        df1.columns = cols_new

        # changing date datatype
        df1['date'] = pd.to_datetime(df1['date'])

        # competition_distance
        df1.loc[df1['competition_distance'].isna(), 'competition_distance'] = self.constant_competition_distance

        # competition_open_since_month
        df1['competition_open_since_month'] = df1.apply(lambda x: x['date'].month if np.isnan(x['competition_open_since_month']) else x['competition_open_since_month'], axis=1) 

        # competition_open_since_year
        df1['competition_open_since_year'] = df1.apply(lambda x: x['date'].year if np.isnan(x['competition_open_since_year']) else x['competition_open_since_year'], axis=1)

        # promo2_since_week
        df1['promo2_since_week'] = df1.apply(lambda x: x['date'].week if np.isnan(x['promo2_since_week']) else x['promo2_since_week'], axis=1)

        # promo2_since_year
        df1['promo2_since_year'] = df1.apply(lambda x: x['date'].year if np.isnan(x['promo2_since_year']) else x['promo2_since_year'], axis=1)

        # promo_interval
        df1['promo_interval'].fillna(0, inplace=True)
        df1['month_map'] = df1['date'].dt.month.map(self.month_map)
        df1['is_promo'] = df1[['promo_interval', 'month_map']].apply(lambda x: 0 if x['promo_interval'] == 0 else 1 if x['month_map'] in x['promo_interval'].split(',') else 0, axis=1)
        df1.drop(['promo_interval', 'month_map'], axis=1, inplace=True)

        # change datatypes
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype('int')
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype('int')

        df1['promo2_since_week'] = df1['promo2_since_week'].astype('int')
        df1['promo2_since_year'] = df1['promo2_since_year'].astype('int')

        # return df
        return df1
    

    def feature_engineering(df2):
        # week
        df2['week'] = df2['date'].dt.isocalendar().week

        # year
        df2['year'] = df2['date'].dt.year

        # quarters
        df2['year_quarters'] = df2['date'].dt.month.apply(lambda x: 1 if x <= 3 else (2 if x <= 6 else (3 if x <= 9 else 4)))

        # weekends
        df2['weekends'] = df2['date'].dt.day_name().apply(lambda x: 0 if x not in ['Friday', 'Saturday'] else 1)

        # last_week_of_month
        df2['last_week_of_month'] = df2['date'].dt.day.apply(lambda x: 0 if x <= 23 else 1)

        # competition_since
        df2['competition_since'] = df2.apply(lambda x: datetime.datetime(day=1, month=x['competition_open_since_month'], year=x['competition_open_since_year']), axis=1)
        df2['competition_time_month'] = ((df2['date'] - df2['competition_since']) / 30).apply(lambda x: x.days).astype('int')
        df2.drop(['competition_since', 'competition_open_since_month', 'competition_open_since_year'], axis=1, inplace=True)

        # promo_since
        df2['promo2_since'] = df2['promo2_since_year'].astype(str) + '-' + df2['promo2_since_week'].astype(str)
        df2['promo2_since'] = df2['promo2_since'].apply(lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days=7))
        df2['promo2_time_week'] = ((df2['date'] - df2['promo2_since']) / 7).apply(lambda x: x.days).astype(int)
        df2.drop(['promo2_since', 'promo2_since_year', 'promo2_since_week'], axis=1, inplace=True)

        # assortment
        df2['assortment'] = df2['assortment'].apply(lambda x: 'basic' if x=='a' else 'extra' if x=='b' else 'extended')

        # state_holiday
        df2['state_holiday'] = df2['state_holiday'].apply(lambda x: 'public_holiday' if x=='a' else 'easter_holiday' if x=='b' else 'christmas' if x=='c' else 'regular_day')

        # day_of_week
        df2['day_of_week'] = df2['date'].dt.day_name()

        # return df
        return df2


    def data_filtering(df4):
        # rows filtering
        df4 = df4.loc[df4['open']!=0]

        # columns filtering
        cols_filtering = ['open', 'customers']
        df4 = df4.drop(cols_filtering, axis=1)

        # return df
        return df4


    def data_preparation(df5):
        # 'competition_distance'
        df5['competition_distance'] = self.rs_competition_distance.transform(df5[['competition_distance']].values)

        # 'competition_time_month'
        df5['competition_time_month'] = self.rs_competition_distance.transform(df5[['competition_time_month']].values)

        # 'promo2_time_week'
        df5['promo2_time_week'] = self.mm_promo2_time_week.transform(df5[['promo2_time_week']].values)

        # 'state_holiday'
        df5['state_holiday'] = df5['state_holiday'].map(self.map_state_holiday)

        # 'store_type'
        df5['store_type'] = df5['store_type'].map(self.map_store_type)

        # 'assortment'
        df5['assortment'] = df5['assortment'].map(self.map_assortment)

        # 'year'
        df5['year'] = df5['year'].map(self.map_year)

        # 'day_of_week'
        df5['day_of_week'] = df5['date'].dt.dayofweek
        df5['day_of_week_sin'] = df5['day_of_week'].apply(lambda x: np.sin(x*(2*np.pi/self.day_of_week_cicle)))
        df5['day_of_week_cos'] = df5['day_of_week'].apply(lambda x: np.cos(x*(2*np.pi/self.day_of_week_cicle)))
        df5.drop('day_of_week', axis=1, inplace=True)

        # 'week'
        df5['week_sin'] = df5['week'].apply(lambda x: np.sin(x*(2*np.pi/self.week_cicle)))
        df5['week_cos'] = df5['week'].apply(lambda x: np.cos(x*(2*np.pi/self.week_cicle)))
        df5.drop('week', axis=1, inplace=True)

        # 'year_quarters'
        df5['year_quarters_sin'] = df5['year_quarters'].apply(lambda x: np.sin(x*(2*np.pi/self.year_quarters_cicle)))
        df5['year_quarters_cos'] = df5['year_quarters'].apply(lambda x: np.cos(x*(2*np.pi/self.year_quarters_cicle)))
        df5.drop('year_quarters', axis=1, inplace=True)

        # feature selection
        df5.drop(self.cols_feature_selection, axis=1, inplace=True)

        # return df
        return df5

    def predictions(df_raw, df7):
        # removing especific features
        X = df7.drop(['date', 'store'], axis=1).values

        # predicting
        y_hat = model.predict(X)

        # dataframe
        df = df_raw.copy()
        df['predictions'] = y_hat
        
        # return df
        return df
        