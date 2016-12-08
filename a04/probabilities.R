dataset <- read.delim("//diskstation/homes/ODU/CS-834_Information-Retrieval/a04/dataset-prob.txt", header=TRUE)

y_hardmn <- dataset$Hard.mn
y_softmn <- dataset$Soft.mn
y_hardmb <- dataset$Hard.mb
y_softmb <- dataset$Soft.mb

plot(y_hardmn, main="Probability Estimate for Word Set Ex. 9.4", xlab = "Feature (Word)", ylab = "Probability", 
            type="l", lwd=2, ylim = c(0, 0.7))
axis(1, at = seq(1, 20))
#
points(y_softmn, type =  "l", lwd=2, col="blue")
points(y_softmn, col="blue", pch=17)
#
points(y_hardmn, type =  "l", lwd=2)
points(y_hardmn, pch=16)
#
points(y_hardmb, type =  "l", lwd=2, col="orange")
points(y_hardmb, col="orange", pch=15)
#
points(y_softmb, type =  "l", lwd=2, col="red")
points(y_softmb, col="red", pch=18)

legend(x=14, y=0.7,c("Hardware Multinomial","Software Multinomial","Hardware Berneoulli", "Software Bernoulli"), lty = c(1,1,1,1),
       col=c('black','blue','orange', 'red'), pch = c(17, 16, 15, 18), bty ="n", horiz = FALSE)
