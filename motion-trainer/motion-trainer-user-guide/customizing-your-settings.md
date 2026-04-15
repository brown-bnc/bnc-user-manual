# Customizing Your Settings

## Game Settings Overview

Each game in Motion Trainer can be customized from the Settings Page. You can adjust how sensitive the system is to motion, how long trials last, and what feedback is shown to the participant.

### 🎈 Balloon Game Settings

* **Movement Tolerance Start (mm):** Initial max allowed movement. Balloon begins inflating from this threshold.
* **Movement Tolerance End (mm):** Final movement threshold as balloon nears popping.
* **Color Feedback:** (toggle) Show visual feedback if enabled. The balloon turns yellow and then red as movement magnitude increases.

### ✳️ Fixation Game Settings

* **Duration for Success (sec):** Time the participant must stay still to succeed.
* **Movement Tolerance (mm):** Fixed threshold for allowable movement.
* **Fixation Graphic:** Image shown during the trial.

### 📺 Video Game Settings

* **Timeout Duration (sec):** How long to wait after excessive movement before timing out.
* **Movement Tolerance (mm):** Max allowed movement while video is playing.
* **Video File:** Video shown to the participant.

***

## Saving and Loading Configurations

You can save your custom settings using the **“Save Config”** button. To reuse them later, click **“Load Config”** and select your saved file.

When you modify any setting, you’ll see "Unsaved Changes" noted at the top of the page:

<figure><img src="../../.gitbook/assets/image (4).png" alt="The Motion Trainer settings page, with &#x22;Unsaved Changes&#x22; in the upper right corner. "><figcaption></figcaption></figure>

If you want to revert to default values, press the **yellow “Defaults”** button.

### Save Your Configuration

1. Press the **green “Save Config”** button
2. A popup will appear prompting you to **name your configuration**
3. Press **Save** to store your configuration locally as a JSON file

<figure><img src="../../.gitbook/assets/image (5).png" alt="Pressing the &#x22;Save Config&#x22; button will open a pop up where users can type a filename. "><figcaption></figcaption></figure>

### Load a Previous Configuration

To reuse a saved config:

1. Press the **gray “Load Config”** button
2. Use the file browser to select your previously saved file
3. Press **Open**

<figure><img src="../../.gitbook/assets/image (6).png" alt="Pressing &#x22;Load Config&#x22; opens a file explorer where users can select their configuration file. "><figcaption></figcaption></figure>

You can now launch your games with the restored settings.
