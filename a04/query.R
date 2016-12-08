dataset <- read.delim("query.txt", header=TRUE)


x1_r <- dataset$q1r
y1_p <- dataset$q1p
x2_r <- dataset$q2r
y2_p <- dataset$q2p

plot(x=x1_r, y=y1_p, main="Uninterpolated Precision-Recall Graph", xlab = "Recall", ylab = "Precision", 
            type="l", lwd=2, col="blue",  xlim = c(0,1), ylim = c(0,1), axes = FALSE)
#
points(x=x2_r, y=y2_p, col="red", type = "l", lwd=2)
points(x=x1_r, y=y1_p, col="blue", pch=17)
points(x=x2_r, y=y2_p, col="red", pch=15)

points(x=x2_r, y=y2_p, col="red", pch=15)
axis(1, at = seq(0, 1, 0.2))
axis(2, at = seq(0, 1, 0.2))

legend('bottomright',c("Query #1","Query#2"), lty = c(1,1),
       col=c('blue', 'red'), pch = c(17, 15), bty ="n", horiz = FALSE)
