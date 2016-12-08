dataset <- read.delim("query.txt", header=TRUE)


x1_r <- dataset$q1r
y1_p <- dataset$q1p

plot(x=0, y=0, main="Average Interpolated Precision-Recall Graph", xlab = "Recall", ylab = "Precision", 
            type="l", lwd=2, col="blue",  xlim = c(0,1), ylim = c(0,1), axes = FALSE)
#
points(x=x1_r, y=y1_p, col="blue", pch=17)
points(x=x2_r, y=y2_p, col="red", pch=15)

points(x=x2_r, y=y2_p, col="red", pch=15)
axis(1, at = seq(0, 1, 0.2))
axis(2, at = seq(0, 1, 0.2))

legend('bottomright',c("Query #1","Query#2", "Average"), lty = c(1,1,1),
       col=c('blue', 'red', 'purple'), pch = c(17, 15, 18), bty ="n", horiz = FALSE)

# create all upper segment for Query#1
segments(0, 1, 0.29, 1, lwd=2, col= 'blue')
segments(0.29, 1, 0.29, 0.70, lwd=2, col= 'blue')
segments(0.29, .70, 1, 0.70, lwd=2, col= 'blue')

# create all upper segment for Query#2
segments(0, 1, 0.33, 1, lwd=1, col= 'red')
segments(0.33, 1, 1, 1, lwd=2, col= 'red')
segments(1, 1, 1, 0.3, lwd=2, col= 'red')

# place average points
points(x=x1_r, y=dataset$avg.prec, col="purple", pch=18)
# create all upper segment for average points
segments(0.29, 0.70, 0.29, 0.50, lwd=2, col= 'purple')
segments(0.29, 0.50, 1.0, 0.50, lwd=2, col= 'purple')

