import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# 2
class Preprocess:
    # constructor
    def __init__(self, path):
        self.data_frame = pd.read_excel(path, index_col=0)

    # change na to mean of column
    def clean_na(self):
        self.data_frame.fillna(self.data_frame.mean(), inplace=True)

    # normalize the data
    def normalize(self):
        col_names = []
        for col_name in self.data_frame.columns:
            if col_name != 'country' and col_name != 'year':
                col_names.append(col_name)

        features = self.data_frame[col_names]
        features = StandardScaler().fit_transform(features.values)
        self.data_frame[col_names] = features

    # aggregation: group by country and mean by year
    def aggregate_by_country(self):
        self.data_frame = self.data_frame.groupby('country').mean()
        self.data_frame = self.data_frame.drop(['year'], axis=1)


# 3
class Clustering:
    # constructor
    def __init__(self, data_frame, n_clusters, n_init):
        self.data_frame = data_frame
        self.n_clusters = n_clusters
        self.n_init = n_init

    def activate_k_means_algorithm(self):
        k_means = KMeans(n_clusters=self.n_clusters, init='random', n_init=self.n_init).fit(self.data_frame)
        self.data_frame['k-means'] = k_means.labels_


# ----------- Tests preprocess (2) -----------

# create preprocess
preprocess = Preprocess('Dataset.xlsx')

# clean_na - works
# print(process.data_frame.isna().sum())
preprocess.clean_na()
# print(process.data_frame.isna().sum())

# normalize - works
preprocess.normalize()
# print(process.data_frame.to_string())

# aggregate by country - works
preprocess.aggregate_by_country()
# print(preprocess.data_frame.to_string())
# process.data_frame.to_csv("data_frame_test.csv")


# ----------- Tests clustering (3) -----------

# create clustering
clustering = Clustering(preprocess.data_frame, 5, 5)

# activate k-means algorithm and add result as column to df - works
clustering.activate_k_means_algorithm()
print(clustering.data_frame.to_string())
