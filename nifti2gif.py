import sys
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Input and output file
fn_img = '/home-local/Data/demo/1401_Skinny_T2AX_e1.nii.gz'
fn_gif = '/home-local/Data/demo/1401_Skinny_T2AX_e1.gif'

# TODO: add axial, coronal, sagital view options
type_view = 'axial' # sagittal/coronal/all

# Load nifti image
nifti_img = nib.load(fn_img)
nifti_data = nifti_img.get_fdata() 
affine_code = nib.aff2axcodes(nifti_img.affine) # affine code with orientation info

# We prefer "A", "L", "S", if not, flip the image
if 'S' in affine_code:
    si_index = affine_code.index('S')
elif 'I' in affine_code:
    si_index = affine_code.index('I')
    nifti_data = np.flip(nifti_data, axis=si_index)
else:
    sys.exit("Check the orientation of the image!")
    
if 'L' in affine_code:
    lr_index = affine_code.index('L')
elif 'R' in affine_code:
    lr_index = affine_code.index('R')
    nifti_data = np.flip(nifti_data, axis=lr_index)
else:
    sys.exit("Check the orientation of the image!")

if 'A' in affine_code:
    ap_index = affine_code.index('A')
    nifti_data = np.flip(nifti_data, axis=ap_index) # TODO: check
elif 'P' in affine_code:
    ap_index = affine_code.index('P')
else:
    sys.exit("Check the orientation of the image!")

# Re-arange axis so that it follows ('A', 'L', 'S')
nifti_data = np.moveaxis(nifti_data, [ap_index, lr_index, si_index], [0, 1, 2])


fig, ax = plt.subplots(figsize=(4,4))

ax.imshow(nifti_data[:,:,22], cmap='gray')
ax.axis('off')
plt.show()    

#TODO: https://imageio.readthedocs.io/en/stable/examples.html#optimizing-a-gif-using-pygifsicle
