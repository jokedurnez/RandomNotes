
# coding: utf-8

# In[1]:

import numpy as np
from random import shuffle as sfl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import gamma
import scipy
import itertools



get_ipython().magic(u'matplotlib inline')


# ## Define hrf functions

# In[2]:

def spm_Gpdf(s,h,l):
    s = np.array(s)
    res = (h-1)*np.log(s) + h*np.log(l) - l*s - np.log(gamma(h))
    return np.exp(res)

def canonical(resolution):
    # translated from spm_hrf
    p=[6,16,1,1,6,0,32]
    dt = resolution/16.
    s = np.array(xrange(int(p[6]/dt+1)))
    #HRF sampled at 0.1 s
    hrf = spm_Gpdf(s,p[0]/p[2],dt/p[2]) - spm_Gpdf(s,p[1]/p[3],dt/p[3])/p[4]
    hrf = hrf[[int(x) for x in np.array(xrange(int(p[6]/resolution+1)))*16.]]
    hrf = hrf/np.sum(hrf)
    # duration of the HRF
    durhrf = 32.0
    # length of the HRF parameters in resolution scale
    laghrf = int(np.ceil(durhrf/resolution))
    hrf = hrf[:laghrf]

    return {"basishrf":hrf,"laghrf":laghrf}


# # Define class for the experiment
# 
# 
#  There are a few settings that can be changed in the functions:
#  The total number of trials: 256
#  The ITI: 6 seconds --> note: we assume a fixed ITI, could (and maybe should) be jittered !
#  The resolution: 0.1 seconds
#  The gains: range 10\$ - 40\$, by 2\$ (as Tom et al.)
#  The losses: range 5\$ - 20\$, by 1\$ (as Tom et al.)

# In[3]:

def shuffle_in_unison(a, b):
        assert len(a) == len(b)
        shuffled_a = np.empty(len(a), dtype=int)
        shuffled_b = np.empty(len(b), dtype=int)
        permutation = np.random.permutation(len(a))
        for old_index, new_index in enumerate(permutation):
                shuffled_a[new_index] = a[old_index]
                shuffled_b[new_index] = b[old_index]
        return shuffled_a, shuffled_b
    
    
class experiment(object):
    def __init__(self,ITI,ntrials=256,resolution=0.1):
        self.ntrials = ntrials
        self.ITI = ITI
        self.AvgITI = round(np.mean(ITI))
        self.resolution = resolution
        self.xaxis = np.arange(0,ntrials*self.AvgITI,resolution)
        #was - self.xaxis = np.arange(0,ntrials*ITI,resolution)

     
    #was -def get_experiment(self):
    def  get_experiment(self,ITI):

        #was - self.onsets = range(0,int(self.ntrials*self.ITI/self.resolution),int(self.ITI/self.resolution))
        self.onsets = [int(x) for x in np.cumsum(ITI, dtype=float)]
        #print self.onsets
        #was -self.gains = np.round(np.random.uniform(10,40,self.ntrials)/2)*2
        #was -self.losses = np.round(np.random.uniform(5,20,self.ntrials))
        largeRange= range(10,41,2)
        smallRange= range(5,21)
        RangeLen=len(largeRange)
        LossesVec=list(itertools.chain.from_iterable(map(lambda x: (list(itertools.repeat(x,RangeLen))),smallRange)))
        GainsVec=largeRange*RangeLen
        [self.gains , self.losses] = shuffle_in_unison(GainsVec,LossesVec)
        distance = self.gains-self.losses
        
        #print self.AvgITI
        #print int(self.ntrials*self.AvgITI/self.resolution)
        reg_task = np.zeros(int(self.ntrials*self.AvgITI/self.resolution))
        reg_task[self.onsets] = 1
        reg_task_c = np.convolve(reg_task,canonical(self.resolution)['basishrf'][:len(reg_task)])
        
        reg_gain = np.zeros(int(self.ntrials*self.AvgITI/self.resolution))
        reg_gain[self.onsets] = (self.gains-np.mean(self.gains))/np.std(self.gains)
        reg_gain_c = np.convolve(reg_gain,canonical(self.resolution)['basishrf'][:len(reg_gain)])
        
        reg_loss = np.zeros(int(self.ntrials*self.AvgITI/self.resolution))
        reg_loss[self.onsets] = (self.losses-np.mean(self.losses))/np.std(self.losses)
        reg_loss_c = np.convolve(reg_loss,canonical(self.resolution)['basishrf'][:len(reg_loss)])

        reg_dist = np.zeros(int(self.ntrials*self.AvgITI/self.resolution))
        reg_dist[self.onsets] = (distance-np.mean(distance))/np.std(distance)
        reg_dist_c = np.convolve(reg_dist,canonical(self.resolution)['basishrf'][:len(reg_dist)])
      
        self.design = np.array([reg_task,reg_gain,reg_loss,reg_dist])
        self.design_c = np.array([reg_task_c,reg_gain_c,reg_loss_c,reg_dist_c])
               
        return self

    def compute_efficiency(self,contrasts):
        
        C = contrasts
        
        XtX = np.dot(EXP.design_c,EXP.design_c.T)  
        invZ = scipy.linalg.inv(XtX)
        CMC = np.matrix(C)*np.matrix(invZ)*np.matrix(C.T)
        
        self.Aopt = float(len(C) / np.matrix.trace(CMC))
        
        return self


# # Example of creating a random design

# In[4]:

# Jittered ITI with an avarage of 8 s 
ITIs=map(lambda x: round(x),(np.random.normal(loc=8, scale=1, size=256)))


# In[5]:

print min(ITIs) # to make sure we have enough time for the response (4 s for response + fixation)


# In[6]:

EXP = experiment(ITIs)
EXP.get_experiment(ITIs)
print EXP.onsets
#was -EXP = experiment()
#was -EXP.get_experiment()


# In[7]:

# print out gains and losses choice
print("Gains: %s"%(str(EXP.gains)))
print("Losses: %s"%(str(EXP.losses)))


# In[8]:

# generate figure
plt.figure(figsize=(12,8))
labs = ["task",'parametric_gain','parametric_loss','parametric_diff']
for x in range(4):
    plt.plot(EXP.xaxis[:600],EXP.design_c.T[:600,x],label=labs[x])
plt.legend()


# # Contrasts
# 

# In[9]:

# To compute the efficiency of the design, we also need to define the contrasts. 
#Here I defined a contrast of main effect of task (&) difference between loss and gain trials


# In[10]:

conts = np.array([
        [1,0,0,0],
        [0,1,-1,0]
    ])

EXP.compute_efficiency(conts)
print(EXP.Aopt)


# # Extract optimal design

# In[11]:

allexp = []
for seed in range(1000):
    EXP = experiment(ITIs)
    EXP.get_experiment(ITIs)
    conts = np.array([
            [1,0,0,0],
            [0,1,-1,0]
        ])
    EXP.compute_efficiency(conts)
    #print("Random experiment %i: efficiency %f"%(seed,EXP.Aopt))
    out = {"opt":EXP.Aopt,"gains":EXP.gains,"losses":EXP.losses,"experiment":EXP.design_c,"xaxis":EXP.xaxis}
    allexp.append(out)
    EXP = None


# In[12]:

# Distribution of optimisation scores:

opt = [x['opt'] for x in allexp]

ax = plt.axes()
sns.distplot(opt,ax=ax)
ax.set_title("distribution of detection power scores")


# In[13]:

# making sure the difference between gain and loss does not affect optimality scores
ist = np.mean([x['gains']-x['losses'] for x in allexp],axis=1)
sns.jointplot(ist,np.array(opt),ylim=(-1e-14,1e-14),kind='kde')


# In[17]:

# making sure the variance on the difference between gain and loss does not affect optimality scores
ist = np.var([x['gains']-x['losses'] for x in allexp],axis=1)
sns.jointplot(ist,np.array(opt),ylim=(-1e-14,1e-14),kind='kde')


# # Optimal design:
# 

# In[15]:

optind = int(np.where(np.array(opt)==np.max(opt))[0])
optimum = allexp[optind]
# compute efficiency

print(optimum)


# In[16]:

# generate figure
plt.figure(figsize=(12,8))
labs = ["task",'parametric_gain','parametric_loss','parametric_diff']
for x in range(4):
    plt.plot(optimum['xaxis'][:1200],optimum['experiment'].T[:1200,x],label=labs[x])

plt.legend()


# In[ ]:




# In[ ]:



