from sklearn.decomposition import LatentDirichletAllocation as LDA

X = [[1,1,1],[1,0,1],[0,2,1],[1,2,0]]

lda = LDA(3,learning_method='online')
y = lda.fit_transform(X)
z = lda.components_

print(y)
print(z)
