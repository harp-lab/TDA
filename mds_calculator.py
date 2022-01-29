from sklearn.manifold import MDS


def get_mds(dissimarity_matrix):
    print(dissimarity_matrix.shape)
    embedding = MDS(dissimilarity='precomputed')
    X_transformed = embedding.fit_transform(dissimarity_matrix)
    print(X_transformed.shape)
    return X_transformed
