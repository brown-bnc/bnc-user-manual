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

### 1. Make a directory to store your downloads under your HOME

```text
# change directory to your HOME 
cd ~
# make a directory called LCModel
mkdir LCModel
# change into the new LCModel directory
cd LCModel
```

### 2. Download LCModel binaries and uncompress file

```text
# download LCModel
wget http://s-provencher.com/pub/LCModel/programs/lcm-64.tar -O lcm-64.tar
# un-tar file
tar xf lcm-64.tar
```

### 3. Run the installer script

```text
./install-lcmodel
```

At this point a GUI window will pop as follows:

![LCModel Select PostScript Display or Print Command](../.gitbook/assets/image%20%287%29.png)

**Press Continue.** A test report should show up as follows:

![LC Model Sample PostScript Result](../.gitbook/assets/image%20%286%29.png)

**Close the result window.** A new success window will follow

![Confirmation Screen for a Successful LCModel Test](../.gitbook/assets/image%20%288%29.png)

Finally, you can **Exit LCMgui**

### **4. Install the License**

In order to run LCModel with your data you need to install a License. To do so, simply copy the license file to the appropiate location

```text
cp /gpfs/data/bnc/licenses/lcmodel-license ~/.lcmodel/license
```

### 5. Copy the Basis Set

```text
cp -r /gpfs/data/bnc/shared/lcmodel/basis-sets ~/.lcmodel/basis-sets
```





