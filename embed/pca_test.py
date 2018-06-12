from sklearn.decomposition import PCA

X = [[1,1,1],[1,0,1],[0,2,1],[1,2,0]]

pca = PCA(2)
y = pca.fit_transform(X)
z = pca.components_

print(y)
print(z)
