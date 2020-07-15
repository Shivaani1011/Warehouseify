import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeRegressor
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def main():
      
    df=pd.read_csv(r'C:\Users\Shivaani\Desktop\Wholesale customers data.csv')
    page = st.sidebar.selectbox("Choose a page", ['Login','About', 'Exploration', 'User Input','Prediction'])

    if page == 'Login':
      st.title('Enter Your Details')
      t1 = st.text_input("Email")
      
      st.sidebar.markdown("---")

      t2 = st.text_input("Password")

      st.write(t1)
      st.write(t2)

      button = st.button("Submit")

   
    elif page == 'About':
      st.title('Warehouseify')
      st.markdown(f'<div class="markdown-text-container stText" style="width: 698px;"><div style="font-size: medium;">Most products lose their market value (outdate) over time. Some products lose valuefaster than others; these are known as perishable products. Traditionally, perishables outdate due to their chemical structure. Examples of such perishable products are grocery, fresh produce, frozen products, dairy products, delicassens etc. So  This application is used to predict the demands required in a warehouse for a short period of time. So, we aim to analyse the data regarding sales and production and to extract the daily data from warehouse which is used to detect the fluctuations in the sales. The web application uses machine learning algorithms to predict the requirements for production which helps in managing the warehouse. </div>',unsafe_allow_html=True)
      
    elif page == 'Exploration':
      st.title('Explore the Product Availability')
      if st.checkbox('Show column descriptions'):
        st.dataframe(df.describe())  
      st.markdown('### Analysing column relations')
      st.text('Correlations:')
      fig, ax = plt.subplots(figsize=(10,10))
      sns.heatmap(df.corr(), annot=True, ax=ax)
      st.pyplot()
      st.text('Effect of the different classes')
      sns.pairplot(df, vars=['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen'], hue='Channel')
      st.pyplot()
      st.line_chart(df)
    elif page == 'User Input':
        st.header('Place your order')
        Fresh = st.slider('Fresh', 3, 56000, 28001)
        Milk = st.slider('Milk', 50, 80000, 40025)
        Grocery = st.slider('Grocery', 3, 92780, 46390)
        Frozen = st.slider('Frozen', 25, 63869, 31947)
        Detergents_Paper = st.slider('Detergents_Paper', 3, 40827, 20415)
        Delicassen = st.slider('Delicassen', 3, 47943, 24000)
        warehouse = {'Fresh': Fresh,
                     'Milk': Milk,
                     'Grocery': Grocery,
                     'Frozen': Frozen,
                     'Detergents_Paper': Detergents_Paper,
                     'Delicassen': Delicassen}
        features = pd.DataFrame(warehouse, index=[0])
        st.write("""
          *You selected*""",warehouse)

        button = st.button("Submit")
    else:
        def pca_results(good_data, pca):
          dimensions= ['Dimension {}'.format(i) for i in range(1,len(pca.components_)+1)]
          components= pd.DataFrame(np.round(pca.components_, 4), columns = list(good_data.keys()))
          components.index = dimensions
          ratios = pca.explained_variance_ratio_.reshape(len(pca.components_), 1)
          variance_ratios = pd.DataFrame(np.round(ratios, 4), columns = ['Explained Variance'])
          variance_ratios.index = dimensions
          fig, ax = plt.subplots(figsize = (14,8))
          components.plot(ax = ax, kind = 'bar');
          ax.set_ylabel("Feature Weights")
          ax.set_xticklabels(dimensions, rotation=0)
          for i, ev in enumerate(pca.explained_variance_ratio_):
            ax.text(i-0.40, ax.get_ylim()[1] + 0.05, "Explained Variance\n%.4f"%(ev))
            predictions = pd.DataFrame(preds, columns = ['Cluster'])
            plot_data = pd.concat([predictions, reduced_data], axis = 1)
            return pd.concat([variance_ratios, components], axis = 1)
        def cluster_results(reduced_data, preds, centers, pca_samples):
          fig, ax = plt.subplots(figsize = (14,8))
          cmap = cm.get_cmap('gist_rainbow')
          for i, cluster in plot_data.groupby('Cluster'):   
            cluster.plot(ax = ax, kind = 'scatter', x = 'Dimension 1', y = 'Dimension 2', color = cmap((i)*1.0/(len(centers)-1)), label = 'Cluster %i'%(i), s=30);
          for i, c in enumerate(centers):
            ax.scatter(x = c[0], y = c[1], color = 'white', edgecolors = 'black', alpha = 1, linewidth = 2, marker = 'o', s=200)
            ax.scatter(x = c[0], y = c[1], marker='$%d$'%(i), alpha = 1, s=100)
            ax.scatter(x = pca_samples[:,0], y = pca_samples[:,1], s = 150, linewidth = 4, color = 'black', marker = 'x')
            ax.set_title("Cluster Learning on PCA-Reduced Data - Centroids Marked by Number\nTransformed Sample Data Marked by Black Cross")
        
        def biplot(good_data, reduced_data, pca):
          fig, ax = plt.subplots(figsize = (14,8))   
          ax.scatter(x=reduced_data.loc[:, 'Dimension 1'], y=reduced_data.loc[:, 'Dimension 2'], 
          facecolors='b', edgecolors='b', s=70, alpha=0.5)
          feature_vectors = pca.components_.T
          arrow_size, text_pos = 7.0, 8.0,
          for i, v in enumerate(feature_vectors):
            ax.arrow(0, 0, arrow_size*v[0], arrow_size*v[1], head_width=0.2, head_length=0.2, linewidth=2, color='red')
        def channel_results(reduced_data, outliers, pca_samples):
           try:
             full_data = pd.read_csv(r'C:\Users\Shivaani\Desktop\Wholesale customers data.csv')
           except:
              print("Dataset could not be loaded. Is the file missing?")       
              return False
           channel = pd.DataFrame(full_data['Channel'], columns = ['Channel'])
           channel = channel.drop(channel.index[outliers]).reset_index(drop = True)
           labeled = pd.concat([reduced_data, channel], axis = 1)
           fig, ax = plt.subplots(figsize = (14,8))
           cmap = cm.get_cmap('gist_rainbow')
           labels = ['Hotel/Restaurant/Cafe', 'Retailer']
           grouped = labeled.groupby('Channel')
           for i, channel in grouped:   
              channel.plot(ax = ax, kind = 'scatter', x = 'Dimension 1', y = 'Dimension 2', color = cmap((i-1)*1.0/2), label = labels[i-1], s=30)  
           for i, sample in enumerate(pca_samples):
              ax.scatter(x = sample[0], y = sample[1], s = 200, linewidth = 3, color = 'black', marker = 'o', facecolors = 'none')
              ax.scatter(x = sample[0]+0.25, y = sample[1]+0.3, marker='$%d$'%(i), alpha = 1, s=125)
              ax.set_title("PCA-Reduced Data Labeled by 'Channel'\nTransformed Sample Data Circled")
        st.write(df.describe())
        np.random.seed(2018)
        indices = np.random.randint(low = 0, high = 441, size = 3)
        print("Indices of Samples => {}".format(indices))

        samples = pd.DataFrame(df.loc[indices], columns = df.keys()).reset_index(drop = True)
        print("\nChosen samples of wholesale customers dataset:")
        
        def sampl_pop_plotting(sample):
          fig, ax = plt.subplots(figsize=(10,5))
          index = np.arange(sample.count())
          bar_width = 0.3
          opacity_pop = 1
          opacity_sample = 0.3

          rect1 = ax.bar(index, data.mean(), bar_width,
                         alpha=opacity_pop, color='g',
                         label='Population Mean')
          rect2 = ax.bar(index + bar_width, sample, bar_width,
                         alpha=opacity_sample, color='k',
                         label='Sample')
    
          ax.set_xlabel('Categories')
          ax.set_ylabel('Total Purchase Cost')
          ax.set_title('Sample vs Population Mean')
          ax.set_xticks(index + bar_width / 2)
          ax.set_xticklabels(samples.columns)
          ax.legend(loc=0, prop={'size': 15})
          fig.tight_layout()
          plt.show()
          display(samples.iloc[0] - data.mean())
          sampl_pop_plotting(samples.iloc[0])
          display(samples.iloc[1] - data.mean())
          sampl_pop_plotting(samples.iloc[1])
          display(samples.iloc[2] - data.mean())
          sampl_pop_plotting(samples.iloc[2])

          percentiles_data = 100*data.rank(pct=True)
          percentiles_samples = percentiles_data.iloc[indices]
          plt.subplots(figsize=(10,5))
          _ = sns.heatmap(percentiles_samples, annot=True)

        def predict_one_feature(dropped_feature):
            print("Dropping feature -> {}".format(dropped_feature))
            new_data = data.drop([dropped_feature], axis = 1)
            X_train, X_test, y_train, y_test = train_test_split(new_data, data[dropped_feature], test_size=0.25, random_state=0)
            regressor = DecisionTreeRegressor(random_state=0)
            regressor.fit(X_train, y_train)
            score = regressor.score(X_test, y_test)
            print("Score for predicting '{}' using other features = {:.3f}\n".format(dropped_feature, score))
            predict_one_feature('Milk')
            print("Features in data -> {}\n".format(data.columns.values))
            for cols in data.columns.values:
                predict_one_feature(cols)
        
        corr = df.corr()
        plt.figure(figsize = (10,5))
        ax = sns.heatmap(corr, annot=True)
        ax.legend(loc=0, prop={'size': 15})
        for cols in df.columns.values:
            ax = sns.kdeplot(df[cols])
            ax.legend(loc=0, prop={'size': 15})
        log_data = np.log(df)
        log_samples = np.log(samples)
        log_corr = log_data.corr()

        f = plt.figure(figsize = (16,8))
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask)] = True
        with sns.axes_style("white"):
            ax1 = sns.heatmap(corr, annot=True, mask=mask, cbar_kws={'label': 'Before Log Normalization'})

        mask2 = np.zeros_like(corr)
        mask2[np.tril_indices_from(mask2)] = True
        with sns.axes_style("white"):
            ax2 = sns.heatmap(log_corr, annot=True, mask=mask2, cmap="YlGnBu", cbar_kws={'label': 'After Log Normalization'})

        outliers_list = []
        for feature in log_data.keys():
            Q1 = np.percentile(log_data[feature], 25)
            Q3 = np.percentile(log_data[feature], 75)
            step = (Q3 - Q1) * 1.5
            print("Data points considered outliers for the feature '{}':".format(feature))
            outliers = list(log_data[~((log_data[feature] >= Q1 - step) & (log_data[feature] <= Q3 + step))].index.values)
            outliers_list.extend(outliers)
    
        print("List of Outliers -> {}".format(outliers_list))
        duplicate_outliers_list = list(set([x for x in outliers_list if outliers_list.count(x) >= 2]))
        duplicate_outliers_list.sort()
        print("\nList of Common Outliers -> {}".format(duplicate_outliers_list))
        outliers  = duplicate_outliers_list
        good_data = log_data.drop(log_data.index[outliers]).reset_index(drop = True)

        pca = PCA(n_components = 6, random_state=0)
        pca.fit(good_data)
        pca_samples = pca.transform(log_samples)
        print("Explained Variance Ratio => {}\n".format(pca.explained_variance_ratio_))
        print("Explained Variance Ratio(csum) => {}\n".format(pca.explained_variance_ratio_.cumsum()))
        pca = PCA(n_components = 2, random_state=0)
        pca.fit(good_data)
        reduced_data = pca.transform(good_data)
        pca_samples = pca.transform(log_samples)
        reduced_data = pd.DataFrame(reduced_data, columns = ['Dimension 1', 'Dimension 2'])

        biplot(good_data, reduced_data, pca)
        def sil_coeff(no_clusters): 
            clusterer_1 = KMeans(n_clusters=no_clusters, random_state=0 )
            clusterer_1.fit(reduced_data)
            preds_1 = clusterer_1.predict(reduced_data)
            centers_1 = clusterer_1.cluster_centers_
            sample_preds_1 = clusterer_1.predict(pca_samples)
            score = silhouette_score(reduced_data, preds_1)
            print("silhouette coefficient for `{}` clusters => {:.4f}".format(no_clusters, score))
    
        clusters_range = range(2,15)
        for i in clusters_range:
            sil_coeff(i)
        clusterer = KMeans(n_clusters = 2)
        clusterer.fit(reduced_data)
        preds = clusterer.predict(reduced_data)
        centers = clusterer.cluster_centers_
        sample_preds = clusterer.predict(pca_samples)
        log_centers = pca.inverse_transform(centers)
        true_centers = np.exp(log_centers)
        segments = ['Segment {}'.format(i) for i in range(0,len(centers))]
        true_centers = pd.DataFrame(np.round(true_centers), columns = df.keys())
        true_centers.index = segments
        st.write(samples)

        for i, pred in enumerate(sample_preds):
            st.write("Sample point", i, "predicted to be in Cluster", pred)
        channel_results(reduced_data, outliers, pca_samples)
           
@st.cache(allow_output_mutation=True)
def train_model(df):
    X = np.array(df.drop(['Milk'], axis=1))
    y= np.array(df['Milk'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    return model, model.score(X_test, y_test)

@st.cache
def load_data():
    return pd.read_csv(r'C:\Users\Shivaani\Desktop\Wholesale customers data.csv')
    names=['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen']

if __name__ =='__main__':
    main()

