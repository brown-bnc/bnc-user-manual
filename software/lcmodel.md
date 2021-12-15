---
description: Installation of LCModel GUI
---

# Installation

## Installing LCModel in Oscar

Installing LCModel in Oscar for personal use is a simple process. Because LCModel has a graphical interface, you will need to connect to Oscar using [Oscar's VNC Client](https://docs.ccv.brown.edu/oscar/connecting-to-oscar/vnc), this will make sure we are using a node that can find its `$DISPLAY`.

### 0. Connecting to Oscar

#### Connecting via VNC

Please follow the instructions in the [Oscar Manual](https://docs.ccv.brown.edu/oscar/connecting-to-oscar/vnc).

After logging in, you will need to **launch the Terminal application**

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

![LCModel Select PostScript Display or Print Command](<../.gitbook/assets/image (7).png>)

**Press Continue.** A test report should show up as follows:

![LC Model Sample PostScript Result](<../.gitbook/assets/image (6).png>)

**Close the result window.** A new success window will follow

![Confirmation Screen for a Successful LCModel Test](<../.gitbook/assets/image (8).png>)

Finally, you can **Exit LCMgui**

{% hint style="info" %}
You may see the following error message: Infiniband hardware address can be incorrect! Please read BUGS section in ifconfig(8). This should have any effect. It is known message in Oscar that will go away in a future update
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
cp -r /gpfs/data/bnc/shared/lcmodel/basis-sets ~/.lcmodel/basis-sets
```



