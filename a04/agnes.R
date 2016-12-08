library(cluster)

x <- c(-4, -3, -2, -1, 1, 1, 2, 3, 3, 4)
y <- c(-2, -2, -2, -2, -1, 1, 3, 2, 4, 3)

d <- data.frame(x = x, y = y)

ag <- agnes (d, metric="euclidean", method ="single")
ag <- agnes (d, metric="euclidean", method ="complete")
ag <- agnes (d, metric="euclidean", method ="average")
ag <- agnes (d, metric="euclidean", method ="gaverage")
ag <- agnes (d, metric="euclidean", method ="ward")

print(ag)

plot(ag, ask = FALSE, which.plots = NULL)

groups <- cutree(ag, k=3) # cut tree into 3 clusters
rect.hclust(H.fit, k=3, border="red") 
