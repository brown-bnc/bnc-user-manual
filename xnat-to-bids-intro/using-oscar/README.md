# Exporting to BIDS using Oscar

## Interacting with Oscar

You can connect to Oscar via different methods. You can [ssh using your terminal](https://docs.ccv.brown.edu/oscar/connecting-to-oscar/ssh), you can [connect via the Desktop GUI or OSCAR shell access apps on Open OnDemand(OOD](https://docs.ccv.brown.edu/oscar/connecting-to-oscar/open-ondemand/interactive-apps-on-ood)), or if your editor can connect to remote servers, [you can connect via your favorite IDE](https://docs.ccv.brown.edu/oscar/connecting-to-oscar/remote-ide) (VSCode is great!). If this is your first time using Oscar and you are new to unix command line, we recommend connecting via the Desktop GUI on Open OnDemand.

{% hint style="info" %}
If you connect to Oscar via SSH or the OOD shell access app, you arrive at a login node, we will need to wrap our commands in a batch file or use an interactive session. You can learn more about running jobs in the Oscar [docs](https://docs.ccv.brown.edu/oscar/submitting-jobs/shared-machine). Please **remember not to run processing on the login nodes**
{% endhint %}

## Installing XNAT2BIDS

**🎉 Skip -** You will not need to install any software. We keep a Singularity image of the most recent tagged release of [`xnat-tools`](https://github.com/brown-bnc/xnat-tools)in Oscar. If this is the first time that you hear the word `Singularity image` don't worry, we will expand more on that soon.

