from nilearn.input_data import NiftiMapsMasker
from nilearn import datasets
import pandas as pd
import os

prepdir = "/oak/stanford/groups/russpold/data/ds000030/1.0.3/derivatives/fmriprep_0.4.4"
subs = [x for x in os.listdir(prepdir) if x.startswith('sub-') and not x.endswith(".html")]

atlas = datasets.fetch_atlas_msdl()
atlas_filename = atlas['maps']

outdir = os.path.join(os.environ.get("SCRATCH"),"CNP_ts")
if not os.path.exists(outdir):
    os.mkdir(outdir)

for sub in subs:
    subnum = float(sub.split("-")[1])
    outfile = os.path.join(outdir,"%s_MSDL.csv"%sub)
    if os.path.exists(outfile):
        continue
    preprocd = os.path.join(prepdir,sub,'func','%s_task-rest_bold_space-MNI152NLin2009cAsym_preproc.nii.gz'%sub)
    if not os.path.exists(preprocd):
        continue
    masker = NiftiMapsMasker(maps_img=atlas_filename, standardize=True,memory='nilearn_cache', verbose=5)
    time_series = masker.fit_transform(preprocd)
    ts = pd.DataFrame(time_series)
    ts.to_csv(outfile,index=False,header=False)
