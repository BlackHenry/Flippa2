import pandas as pd


class Wrapper:
    def __init__(self, path):
        self.db = pd.read_csv(path, dtype='str').fillna('-1')

    def count_nan(self):
        values = {}
        for column in self.db.columns[1:]:
            values[column] = self.db[(self.db[column] != '-1')].shape[0]
        return values

    def wrap_net_profit(self, x):
        x = x.replace('$', '').replace(' p/mo', '').replace('—', '0').replace(',', '')
        return ''.join(x.split())

    def wrap_site_age(self, x):
        x = ''.join(x.split())
        x = x.replace('years', 'year').replace('year', 'years')
        x = x.replace('months', 'month').replace('month', 'months')
        if 'y' in x:
            x = x.replace('years', '')
            x = pd.to_numeric(x)
            x *= 365
        elif 'n' in x:
            x = x.replace('months', '')
            x = pd.to_numeric(x)
            x *= 31
        return x

    def wrap_site_type(self, x):
        x = x.replace('eCommerce', '1').replace('—', '0').replace('Services', '2').replace('Content', '3')
        x = x.replace('SaaS', '4').replace('Transactional / Marketplace', '5')
        return pd.to_numeric(x)

    def wrap_starting_price(self, x):
        x = ''.join(x.split())
        x = x.replace('$', '').replace('EndedWithoutaWinner', '0').replace(',', '')
        return pd.to_numeric(x)

    def wrap(self):
        self.db = self.db[self.db['page_views_0'] != '-1'].reset_index()
        del self.db['content_unique?'], self.db['template_unique?'], self.db['design_unique?']
        del self.db['index'], self.db['Unnamed: 0'], self.db['listing_type'], self.db['platform']
        self.db['avg._session_duration'] = self.db['avg._session_duration'].apply(lambda x: ''.join(x.split()))
        self.db['avg._session_duration'] = pd.to_numeric(pd.to_timedelta(self.db['avg._session_duration'])) / 1e9
        self.db['bounce_rate'] = pd.to_numeric(self.db['bounce_rate'].apply(lambda x: x.replace('%', ''))) / 100
        self.db['net_profit'] = pd.to_numeric(self.db['net_profit'].apply(self.wrap_net_profit))
        for _ in range(10):
            self.db['page_views_' + str(_)] = pd.to_numeric(self.db['page_views_' + str(_)].apply(lambda x: x.replace(',', '')))
            self.db['page_visitors_' + str(_)] = pd.to_numeric(self.db['page_visitors_' + str(_)].apply(lambda x: x.replace(',', '')))
        self.db['pages_/_session'] = pd.to_numeric(self.db['pages_/_session'])
        self.db['site_age'] = self.db['site_age'].apply(self.wrap_site_age)
        self.db['site_type'] = self.db['site_type'].apply(self.wrap_site_type)
        self.db['starting_price'] = self.db['starting_price'].apply(self.wrap_starting_price)


w = Wrapper('Database2.csv')
w.wrap()
