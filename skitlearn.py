from sklearn.linear_model import LinearRegression

X = [[1],[2],[3],[4],[5],[6],[7],[8]]

y = [30,50,70,90,100,120]

Model = LinearRegression()

Model.fit(X,y)

print(Model.predict([[5]]))

 