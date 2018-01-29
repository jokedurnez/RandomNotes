Before starting this tutorial, please install [RStudio](https://www.rstudio.com/products/RStudio/).  If you're experiencing problems preparing the software, look at this excellent tutorial: http://web.cs.ucla.edu/~gulzar/rstudio/

Once you've install RStudio, please also install the following packages (using the following commands):
```
source('https://neuroconductor.org/neurocLite.R')
neuro_install(‘neurobase', release = "stable")

source('https://bioconductor.org/biocLite.R')
biocLite("graph")
biocLite(‘RBGL')
biocLite('pcor')

install.packages('RColorBrewer')
install.packages('scales')
install.packages('lattice')
install.packages('Rcmdr')
install.packages('neurosim')
```
