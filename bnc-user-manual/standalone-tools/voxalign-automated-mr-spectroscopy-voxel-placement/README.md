# voxalign: automated MR spectroscopy voxel placement

We have developed a python package "[voxalign](installation.md)" that takes much of the guesswork out of MR spectroscopy voxel placement.



* One of voxalign's core functions is to ensure reproducible voxel placements across multiple scan sessions within the same participant. To do this, voxalign takes in the spectroscopy DICOM(s) and a T1 anatomical scan from a first MR session, and a T1 from an in-progress MR session, and provides the prescription to enter on the console to match the exact voxel position and orientation from the first session. Learn how to use voxalign for longitudinal studies like this [in our documentation on multi-session alignment](multi-session-alignment.md).

<figure><img src="../../.gitbook/assets/vox_overlap.png" alt="Overlaid onto an anatomical MRI scan are the two spectroscopy voxels (session 1 and session 2). Session 2 was aligned to session 1 using voxalign, and this image shows how accurate the overlay is. "><figcaption><p>Scan session 1 voxel outline (dark blue) overlaid on the scan session 2 voxel</p></figcaption></figure>



* Voxalign can also tell you where to position the center of your voxel if you instead have a set of MNI coordinates to target. This is useful in helping to standardize voxel placement across participants, and for choosing voxel placements in the first session of a longitudinal study. Learn how to determine your voxel position based on MNI coordinates [in our section on centering on MNI coordinates](center-on-mni-coordinate.md).

<figure><img src="../../.gitbook/assets/mni_lookup.png" alt="A red cross overlaid onto an anatomical scan shows where the center of the ROI is, using MNI coordinates. "><figcaption><p>MRS voxel center position corresponding to an MNI coordinate of [-8, 38, 31]</p></figcaption></figure>
