zipf_law <- read.delim("//diskstation/homes/ODU/CS-834_Information-Retrieval/a02/zipf_law-s.txt", header=TRUE)
View(zipf_law)
# 
# Get number of rows
max_x <- length(zipf_law$value)
x <- c(1:max_x)
y <- zipf_law$value / sum(zipf_law$value)
r <- c(1e-06, 1e-04, 1e-03, 0.1, 1)
r1 <- c(1, 10, 100, 1000, 10000, 1e+06)
# Plot Graph
plot(x, y, main="Wikipedia Words\nSmall Collection (Unigram)", 
     xlab="Rank", ylab="Pr",
     log="xy", xaxt="n")
#
#axis(side=2, at=r, lwd=1)
axis(side=1, at=r1, lwd=1)

fr <- zipf_law$value
p <- fr/sum(fr)

lzipf <- function(s, N) -s*log(1:N)-log(sum(1/(1:N)^s))
opt.f <- function(s) sum((log(p)-lzipf(s,length(p)))^2)
opt <- optimize(opt.f,c(p[1],max_x))

# 
library(stats4)
ll <- function(s) sum(fr*(s*log(1:max_x)+log(sum(1/(1:max_x)^s))))
fit <- mle(ll,start=list(s=1))
summary(fit)

#
s.sq <- opt$minimum
s.ll <- coef(fit)

# plotting best-fit line
lines(1:max_x,exp(lzipf(s.sq,max_x)),col=2)

