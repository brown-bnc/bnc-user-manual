# LCModel

## Installing LCModel in Oscar

Installing LCModel in Oscar for personal use is a simple process. Because LCModel has a graphical interface, you will need to connect using [Oscar's VNC Client](https://docs.ccv.brown.edu/oscar/connecting-to-oscar/vnc) or  via SSH with X11 fowarding enables. i.e 

`ssh -X username@ssh.ccv.brown.edu`

### 1. Make a directory to store your downloads under your HOME

```text
cd ~
mkdir LCModel
cd LCModel
```

### 2. Download LCModel binaries and uncompress file

```text
wget http://s-provencher.com/pub/LCModel/programs/lcm-64.tar -O lcm-64.tar
tar xf lcm-64.tar
```

### 3. Run the installer script

```text
./install-lcmodel
```



