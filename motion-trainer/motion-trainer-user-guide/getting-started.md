---
description: >-
  This guide will help you quickly set up and run your first session. You'll
  learn how to launch the app, adjust basic settings, and try out the different
  movement-based games.
---

# Getting Started

## Launching Motion Trainer

1. On the **desktop**, locate the **Motion Trainer** shortcut icon:
   * It will be labeled `MotionTrainer`.
2. **Double-click** the icon to launch the application.
3. When the application launches, you should see the following splash screen.
4. **Click** the arrow to continue.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-09 at 3.51.29 PM.png" alt="The Motion Trainer splash page shows the version (v1.0) and an arrow button to enter the application. "><figcaption></figcaption></figure>

## Configuring Game Settings

Next, you should be navigated to the Settings Page.  The Settings Page allows you to configure the different experimental games:&#x20;

* **Balloon Game** – A movement-sensitivity game where users must keep their head movement within a gradually shrinking threshold.
* **Fixation Game** – Encourages the subject to remain still and focus for a given duration.
* **Video Game** – Plays a video file if the subject stays still; pauses if they move too much.

Each game has a few tunable parameters (like movement tolerance and duration), but for now, you can use the defaults to get started.

<figure><img src="../../.gitbook/assets/Screenshot 2025-06-09 at 4.02.36 PM.png" alt="The “Game Settings” page of the Motion Trainer Application. Sections include: Balloon Game, Fixation Game, and Video Game. The upper right corner shows that the current settings are the default. "><figcaption></figcaption></figure>

Press **"Done"** to begin the session after configuring your games.

## Game Selection Screen

After saving your settings and clicking **Done**, you'll arrive at the **Game Selection Screen**, where you can choose which game to run:

* **Blow Up the Balloon**\
  Inflate a balloon by pressing a button while staying still. The balloon grows while movement stays within tolerance and deflates if the subject moves too much.
* **Stay Still**\
  A fixation-style task. The subject must remain still for a fixed period to succeed.
* **Watch Video**\
  Plays a video file when the subject remains still. Movement pauses playback.

To change game parameters, click **Settings** to return to the previous configuration screen.

<figure><img src="../../.gitbook/assets/image (1).png" alt="The “Select the game you would like to play” page of the Motion Trainer application. Options include: “Blow Up the Balloon”, “Stay Still”, “Watch Video”, and “Settings”. "><figcaption></figcaption></figure>

## 🎈 Blow Up the Balloon

In this game, the participant inflates a balloon by pressing a button on a handheld device (e.g., a button box). With each button press:

* The balloon **grows slightly**
* The **tolerance for movement decreases**, making it harder to stay still as the game progresses

### Objective

* Inflate the balloon until it **pops** — this counts as a successful trial!
* If the participant moves **outside the allowed tolerance**, the balloon **deflates** and they are given a chance to try again

### How It Works

* The movement tolerance begins at the **“Movement Tolerance Start”** value (set in the Settings Page)
* It gradually scales down to the **“Movement Tolerance End”** as the balloon inflates
* Movement is monitored continuously, so the participant must press carefully and remain still

<figure><img src="../../.gitbook/assets/image (1) (3).png" alt="An example of the &#x22;Blow Up the Balloon&#x22; game. A white background contains a small image of a nail toward the top of the screen, and a balloon below. "><figcaption></figcaption></figure>

## ✳️ Stay Still

In this game, the participant is shown a fixation graphic on screen and must remain completely still for a set amount of time.

### Objective

* Stay still for the full **duration** (set via `Fixation Duration` in the Settings Page)
* If movement exceeds the allowed **tolerance** (set via `Movement Tolerance`), the trial **fails** and the participant is prompted to try again
* If they successfully remain within tolerance for the entire duration, the trial is **a success**

### How It Works

* The fixation graphic remains visible on screen throughout the task
* A **fixed movement threshold** is used (does not change over time like in the balloon game)
* The trial ends automatically after either a success or a failure

<figure><img src="../../.gitbook/assets/image (2).png" alt="An example of the &#x22;Stay Still&#x22; game. A black fixation cross is displayed over a white background. "><figcaption></figcaption></figure>

## 📺 Watch Video

In this game, a video (e.g., a short animated clip) plays while the participant remains still. It pauses whenever movement exceeds a configured threshold and resumes once the participant is still again.

### Objective

* Watch the full video without interruption
* If the participant **moves too much**, the video **pauses**
* A message saying **“Stay still!”** appears as feedback
* Once the participant’s movement falls **back within the tolerance**, the video automatically resumes

### How It Works

* The video file is selected on the **Settings Page**
* A **fixed movement tolerance** (in mm) is configured for this game
* There is also a **timeout value** — if the participant doesn’t return to stillness within this time, the session can be stopped or retried

<figure><img src="../../.gitbook/assets/image (3).png" alt="An example of the &#x22;Watch Video&#x22; feature of Motion Trainer. A default childrens video is shown on screen. "><figcaption></figcaption></figure>
