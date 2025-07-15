# Diffusion Weighted Imaging (DWI) Analysis

## Basic Terminology

_**B-value:**_ A factor which describes the amount of diffusion weighting, i.e., the duration, amplitude, and time between the application of diffusion gradients. Higher b-values indicate stronger diffusion effects and are achieved by increased amplitude/duration of gradient pulses as well widening the intervals between the pulses ([Abou khadrah & Imam, 2019](https://ejrnm.springeropen.com/articles/10.1186/s43055-019-0054-3)). The higher the b-value, the lower the signal. Volumes with a b-value of 0 are those with no diffusion gradient applied.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2024-06-14 at 2.07.27 PM (1).png" alt=""><figcaption><p>Three diffusion weighted images with b-values of bval=0, 750, and 1500</p></figcaption></figure>

_**B-vector:**_ A 3x1 vector (x, y, and z) for each volume, which describes the direction that the diffusion gradient will be applied.&#x20;

**B-table:** A table where each row has four entries: the b-value followed by the x, y, and z components of the b-vector. This repeats with one row for each volume. B-tables are embedded in the DWI protocol on the MRI console, and are used to control the strength, direction, and duration of the diffusion gradients at the scanner level. B-tables are also used in many common diffusion preprocessing software packages, including dsi-studio (where it is transformed into the b-matrix and used to create diffusion tensor images).&#x20;

{% hint style="info" %}
B-tables are sometimes also called "gradient tables".
{% endhint %}

_**Shell:**_ The number of shells of a DWI protocol describes the number of non-zero b-values used. Single-shell protocols have one b-value which repeats with varying directions of the diffusion gradient. Multi-shell protocols acquire two or more b-values at multiple directions.&#x20;

**q-space:** A 3-dimensional mathematical space that represents how water diffusion is measured in the DWI sequence. Each point in this space corresponds to a particular bvec/bval pair, where the distance from the origin is the amount of diffusion sensitization (b-value), and the orientation on the 3D grid is the direction of diffusion sensitivity (b-vector).&#x20;

The b-table can be viewed in q-space, where you can more clearly see how volumes are differentiated by shell. Volumes with equal diffusion sensitization (b-values) but different diffusion directions (b-vectors) will form a spherical shape, such as the two shown below in blue and yellow:&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2025-07-15 at 4.37.33 PM.png" alt=""><figcaption><p>q-space visualization of the b-table of Demodat2 subject 101 session 01 (sub-101_ses-01_acq-b1500_dir-ap_dwi) in q-space. As you can see, this is a two shell acquisition with b-values of 750 and 1500. </p></figcaption></figure>

<details>

<summary>Python Script to Create Your Own Shell Visualization!</summary>

Here is the script used to create the graph shown above. It can be used to make a map of q-space with your own b-table data. All you have to do is add the path and filenames to your own .bvec and .bval data in the first section of code.&#x20;

```python
import numpy as np
import matplotlib.pyplot as plt

# ===== Load bvals and bvecs =====
bvals = np.loadtxt('your_file.bval')  # Replace with your actual file
bvecs = np.loadtxt('your_file.bvec')

# Ensure there are 3 bvec values per volume 
if bvecs.shape[0] != 3:
    bvecs = bvecs.T

# ===== Compute q-space vectors (√bval * bvec) =====
q_vectors = bvecs * np.sqrt(bvals)

# ===== Plot =====
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Use colormap based on actual b-value
sc = ax.scatter(
    # 0=X, 1=Y, and 2=Z gradient directions
    q_vectors[0], q_vectors[1], q_vectors[2],
    c=bvals,
    cmap='viridis',
    s=40,
    alpha=0.85
)

# Add colorbar to show b-value scale
cb = plt.colorbar(sc, ax=ax, pad=0.1)
cb.set_label('b-value (s/mm²)', fontsize=12)

# Formatting
ax.set_title('Q-space Shells from Original b-values', fontsize=14)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_box_aspect([1, 1, 1])
ax.grid(True)

plt.tight_layout()
plt.show()

```

</details>

_**Susceptibility Distortion:**_ Susceptibility is the property of a substance that determines if it becomes magnetized when placed in a magnetic field. Further, substances can be diamagnetic (resulting in a repelling/dispersion of the magnetic field around it), or paramagnetic (resulting in an attraction/concentration of the magnetic field around it). Most biological tissues such as bone, muscle, and fat are slightly diamagnetic. Air, such as that in the sinuses, is slightly paramagnetic. Certain MRI sequences are more prone to susceptibility distortion artifacts, including many common diffusion scans ([Embleton et al., 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC6870737/)). More information on magnetic susceptibility and how it can create artifacts can be found [here](https://mriquestions.com/susceptibility-artifact.html).&#x20;

_**Eddy Currents:**_ Electrical currents (eddy currents) appear in nearby conductive materials (coils, shields, the participant) when an MRI is creating a rapidly changing magnetic field. The magnitude of the eddy current increases as the rate of change of the magnetic field increases. Because of this, EPI, DWI, MR Spectroscopy, and anything else with a short echo time will be affected. It is an issue in MRI processing because it results in image distortions (shearing/scaling artifacts, global position shifts) and in the case of DWI, it can result in spuriously high ADC values.&#x20;
