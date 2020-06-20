import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objects as go


# back-end
class KMeansClustering:
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

    # run k-mean algorithm with given parameters
    def activate_k_means_algorithm(self, n_clusters, n_init):
        k_means = KMeans(n_clusters=n_clusters, init='random', n_init=n_init).fit(self.data_frame)
        self.data_frame['k-means'] = k_means.labels_

    # plot scatter
    def create_scatter_generosity_social_support(self):
        plt.scatter(self.data_frame['Generosity'], self.data_frame['Social support'], c=self.data_frame['k-means'])
        plt.title('K-Means Clustering')
        plt.xlabel('Generosity')
        plt.ylabel('Social support')
        plt.show()
        plt.savefig('k-means_scatter.png')
        return plt

    # plot Choropleth Map
    def create_country_map(self):
        df_countries = pd.read_csv('country_codes_iso_3.csv')
        fig = go.Figure(data=go.Choropleth(
            locations=df_countries['code'],
            z=self.data_frame['k-means'],
            colorscale='rainbow',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title='K-Means',
        ))

        fig.update_layout(
            title_text='K Means Clustering',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )

        py.sign_in('euguman', '3Zb8TzOCWAs0JmBmNERB')
        py.image.save_as(fig, filename='country_map.png')


# ----------- Tests preprocess (2) -----------

# create preprocess
k_means_clustering = KMeansClustering('Dataset.xlsx')

# clean_na - works
# print(k_means_clustering.data_frame.isna().sum())
k_means_clustering.clean_na()
# print(k_means_clustering.data_frame.isna().sum())

# normalize - works
k_means_clustering.normalize()
# print(k_means_clustering.data_frame.to_string())

# aggregate by country - works
k_means_clustering.aggregate_by_country()
# print(k_means_clustering.data_frame.to_string())
# k_means_clustering.data_frame.to_csv("data_frame_test.csv")


# ----------- Tests clustering (3) -----------

# activate k-means algorithm and add result as column to df - works
k_means_clustering.activate_k_means_algorithm(5, 5)
# print(clustering.data_frame.to_string())
# k_means_clustering.data_frame.to_csv("data_frame_test.csv")

# plot scatter pf Generosity:Social_Support from df
k_means_clustering.create_scatter_generosity_social_support()

# map figure - works
k_means_clustering.create_country_map()
