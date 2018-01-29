null = 10
total = 30
par(mfrow=c(1,3))
for (alt in c(0,0.2,0.5)){
plot(1:3,c(0,0,1),col="white")
l = 0
for (eff in c(0,0.2)){
l = l+1
mnT = c()
vaT = c()
typeI = power = c()
k = 0
for (null in seq(0,29,10)){
  k = k+1
  print(null)
p = c()
t = c()
for (i in 1:10000){
  y = c(rnorm(total-null,eff,1),rep(alt,null))
  test = t.test(y)
  p[i] = test$p.value
  t[i] = test$statistic
}
mnT[k]=mean(t)
vaT[k]=var(t)
typeI[k] = mean(p<0.05)
}

lines(typeI,col=l)
}
}