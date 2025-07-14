# Advanced Settings

The **Advanced Settings** panel allows you to configure low-level behavior for motion tracking and inspect device connection details.

Access it from the **“Advanced”** button on the bottom panel of the Settings Page.

***

## Motion Processing Parameters

At the top of the panel, you can tune how Motion Trainer calculates movement:

### Window Size

The number of most recent data samples used to compute the average position.

* **Smaller window** = more sensitive to sudden movement
* **Larger window** = smoother, more resistant to noise or tremors

### Lag Delta

How far back in time (in samples) the system compares movement against.

* **Smaller lag** = emphasizes quick jerks or taps
* **Larger lag** = more responsive to slow drift or gradual deviation

These two values together let you tailor how motion is interpreted — whether you're prioritizing stillness, detecting fidgets, or capturing fast motions.

***

## Device Information

This section shows the current status of the **Polhemus 3D Digitizer** (or other motion device):

* ✅ **Device Connected**: Indicates the serial device is actively streaming data
* ❌ **Device Not Connected**: Shows if no valid data stream is detected

{% hint style="info" %}
For more information on how to set up the Polhemus 3D Digitizer in the Simulator Room at Brown University, please refer to our earlier documentation [here](https://docs.ccv.brown.edu/bnc-user-manual/mrf-guides/mri-simulator-room/motion-trainer-balloon-task).&#x20;
{% endhint %}

### Connection Fields

* **Serial Device:** File path of the connected USB or serial interface (e.g. `/dev/tty.usbserial-A10NW`)
* **Driver Class:** The software driver currently in use (e.g. `PolhemusDriver`)

<figure><img src="../../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

***
