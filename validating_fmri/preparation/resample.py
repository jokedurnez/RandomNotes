from nilearn.image import resample_img
import nibabel as nib
import os
import numpy as np

datafolder = "/Users/Joke/Desktop/validating-fmri/data"

subs = list(np.unique([x.split("_")[0] for x in os.listdir(os.path.join(datafolder,"CNP_rest"))]))

for sub in subs:
    anatfile = os.path.join(datafolder,"CNP_rest/%s_T1w_space-MNI152NLin2009cAsym_preproc.nii.gz"%sub)
    anatfile_reduced = os.path.join(datafolder,"CNP_rest/%s_T1w_space-MNI152NLin2009cAsym_preproc_reduced.nii.gz"%sub)
    restfile = os.path.join(datafolder,"CNP_rest/%s_task-rest_bold_space-MNI152NLin2009cAsym_preproc.nii.gz"%sub)
    anat = nib.load(anatfile)
    rest = nib.load(restfile)
    anat_resampled = resample_img(anat,target_affine=rest.affine,target_shape=rest.shape[:3])
    anat_resampled.to_filename(anatfile_reduced)

atlasfile = os.path.join(datafolder,"MSDL_rois","msdl_rois.nii")
atlas = nib.load(atlasfile)
atlas_resampled = resample_img(atlas,target_affine=anat_resampled.affine,target_shape=anat_resampled.shape[:3])

data = atlas_resampled.get_data()
newdata = np.zeros(data.shape[:3])
for x in range(data.shape[0]):
    for y in range(data.shape[1]):
        for z in range(data.shape[2]):
            if np.max(data[x,y,z])<0.1:
                newdata[x-1.5,y-1.5,z-0] = 0
            else:
                newdata[x-1.5,y-1.5,z-0] = np.where(data[x,y,z]==np.max(data[x,y,z]))[0][0]+1

img = nib.Nifti1Image(newdata,affine=anat_resampled.affine,header=anat_resampled.header)
atlasfile_reduced = os.path.join(datafolder,"MSDL_rois","msdl_rois_reduced.nii.gz")
img.to_filename(atlasfile_reduced)
