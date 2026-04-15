---
description: Installation of LCModel GUI
---

# Installation

{% hint style="info" %}
The use of LCModel in Oscar is no longer the reccomended method to analyze MRS data. We now suggest that users conduct MRS preprocessing, spectra fitting, and metabolite value extraction using Osprey. We provide documentation on Osprey in this user manual. This page on LCModel remains public for legacy purposes.&#x20;
{% endhint %}

## Installing LCModel in Oscar

Installing LCModel in Oscar for personal use is a simple process. Because LCModel has a graphical interface, you will need to connect to Oscar using the Desktop Application via OpenOnDemand, this will make sure we are using a node that can find its `$DISPLAY`.

### 0. Connecting to Oscar

#### Connecting via Desktop App in Open on Demand

* Visit [the Oscar Open On Demand Portal](https://ood.ccv.brown.edu/).
* Click on the Desktop Icon and start a Desktop job. \
  If you receive an error the error `you are already running a Desktop session,` you will need to click on "My interactive sessions" at the top panel on the page. You will see your existing session. Click _Launch to start this session._
* Launch a terminal inside the Desktop interface.

### 1. Download LCModel tar under your HOME

```
# change directory to your HOME 
cd ~
```

### 2. Download LCModel binaries and uncompress file

```
# download LCModel
wget http://s-provencher.com/pub/LCModel/programs/lcm-64.tar -O lcm-64.tar
# un-tar file
tar xf lcm-64.tar
```

### 3. Run the installer script

```
./install-lcmodel
```

At this point a GUI window will pop as follows:

<figure><img src="../../.gitbook/assets/image (8).png" alt="The LCMgui pop up window, instructing users to use the default display command “evince” by pressing “Continue”. "><figcaption><p>LCModel Select PostScript Display or Print Command</p></figcaption></figure>

**Press Continue.** A test report should show up as follows:

<figure><img src="../../.gitbook/assets/image (11).png" alt="A LC Model PostScript file called test.ps, which shows various spectroscopy plots. "><figcaption><p>LC Model Sample PostScript Result</p></figcaption></figure>

**Close the result window.** A new success window will follow

<figure><img src="../../.gitbook/assets/image (19).png" alt="An “Installation/Update Successful” pop up. It notifies the user that the test runs were successful and allows them to opt in to “Further tests” or to “Exit LCMgui”."><figcaption><p>Confirmation Screen for a Successful LCModel Test</p></figcaption></figure>

Finally, you can **Exit LCMgui**

{% hint style="info" %}
You may see the following error message: Infiniband hardware address can be incorrect! Please read BUGS section in ifconfig(8). This should not have any effect. It is a known message in Oscar that will go away in a future update
{% endhint %}

### **4. Install the License**

LCModel is now free. However, you'll need to create an empty license file. You can do so from the terminal as follows.&#x20;

```
cd ~/.lcmodel
touch license
```

{% hint style="warning" %}
If you have used LCModel before and have an outdated license file, please remove it
{% endhint %}

### 5. Copy the Basis Set

```
cp -r /oscar/data/bnc/shared/lcmodel/basis-sets ~/.lcmodel/basis-sets
```



