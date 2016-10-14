heaps_curve <- read.delim("//diskstation/homes/ODU/CS-834_Information-Retrieval/a02/heaps_curve-l.txt", header=TRUE)
# 
# Get number of rows
max_x <- length(as.numeric(heaps_curve$words))
x <- cumsum(as.numeric(heaps_curve$words))
y <- heaps_curve$words
r <- c(100, 1000, 10000, 100000)

# y- values for small collection
#r1 <- c(1, 10, 100, 1000, 10000, 1e+06)

# y- values for large collection
r1 <- c(1, 10, 100, 1000, 10000, 1e+06)

# Plot Graph
plot(x, y, main="Heaps Curve for\nWikipedia Words Large Collection", 
     xlab="Words in Collection", ylab="Words in Vocabulary")

# print y-axis ticks 
axis(side=2, at=r, lwd=1)

# print x-axis ticks
#axis(side=1, at=r1, lwd=1)

# y-axis values
y1 <- x ** 0.43 * 36

lines(x,y1 , col=2)

