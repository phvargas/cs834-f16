x <- c(-4, -3, -2, -1, 1, 1, 2, 3, 3, 4)
y <- c(-2, -2, -2, -2, -1, 1, 3, 2, 4, 3)

d <- data.frame(x = x, y = y)
library(ggplot2)

p <-ggplot(d , aes(x=x, y=y)) +
  geom_point() +
  lims(x=c(-4,4),y=c(-4,4)) +
  theme_minimal() +
  coord_fixed() +  
  geom_vline(xintercept = 0) + geom_hline(yintercept = 0) 
p
