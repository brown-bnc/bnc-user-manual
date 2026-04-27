# Step 1: Preprocessing

1. Convert diffusion files from NIFTI to MIF

    ```bash
    ## AP 
    mrconvert $bids_dir/$subID/$sesID/dwi/${subID}_${sesID}_acq-b1500_dir-ap_dwi.nii.gz $output_dir/${subID}_${sesID}_AP_dwi.mif -fslgrad $bids_dir/$subID/$sesID/dwi/${subID}_${sesID}_acq-b1500_dir-ap_dwi.bvec $bids_dir/$subID/$sesID/dwi/${subID}_${sesID}_acq-b1500_dir-ap_dwi.bval
    ## PA
    mrconvert $bids_dir/$subID/$sesID/dwi/${subID}_${sesID}_acq-b1500_dir-pa_dwi.nii.gz $output_dir/${subID}_${sesID}_PA_dwi.mif -fslgrad $bids_dir/$subID/$sesID/dwi/${subID}_${sesID}_acq-b1500_dir-pa_dwi.bvec $bids_dir/$subID/$sesID/dwi/${subID}_${sesID}_acq-b1500_dir-pa_dwi.bval

    ```

2. Denoise

    ```bash
    ## Denoise AP
    dwidenoise ${output_dir}/${subID}_${sesID}_AP_dwi.mif ${output_dir}/${subID}_${sesID}_AP_den.mif -noise ${output_dir}/noise_AP.mif
    ## Denoise PA
    dwidenoise ${output_dir}/${subID}_${sesID}_PA_dwi.mif ${output_dir}/${subID}_${sesID}_PA_den.mif -noise ${output_dir}/noise_PA.mif

    # Create residual map
    ## AP Map
    mrcalc ${output_dir}/${subID}_${sesID}_AP_dwi.mif ${output_dir}/${subID}_${sesID}_AP_den.mif -subtract ${output_dir}/residual_AP.mif
    ## PA Map
    mrcalc ${output_dir}/${subID}_${sesID}_PA_dwi.mif ${output_dir}/${subID}_${sesID}_PA_den.mif -subtract ${output_dir}/residual_PA.mif

    ```

3. Extract B0s

    ```bash
    ## The --bzero flag reads the embedded b-table and extracts the b0s automatically
    ## mrmath takes the 13 B0 frames per run, and merges them into the mean (1 frame per PE dir)
    dwiextract ${output_dir}/${subID}_${sesID}_AP_den.mif - -bzero | mrmath - mean ${output_dir}/mean_b0_AP.mif -axis 3
    dwiextract ${output_dir}/${subID}_${sesID}_PA_den.mif - -bzero | mrmath - mean ${output_dir}/mean_b0_PA.mif -axis 3

    # Sanity check to make sure the B0s are extracted correctly. You should have a dset with 13 frames and all should be B0s
    # dwiextract sub-101_ses-01_AP_den.mif -bzero 

    # Concatenate AP and PA B0s, to be input into topup 
    mrcat ${output_dir}/mean_b0_AP.mif ${output_dir}/mean_b0_PA.mif -axis 3 ${output_dir}/b0_pair.mif

    ```

4. Preprocess!&#x20;

    ```bash
    dwifslpreproc ${output_dir}/${subID}_${sesID}_AP_den.mif ${output_dir}/${subID}_${sesID}_den_preproc.mif -nocleanup -scratch $output_dir -pe_dir AP -rpe_pair -se_epi ${output_dir}/b0_pair.mif -eddy_options " --slm=linear --data_is_shelled"

    ```
