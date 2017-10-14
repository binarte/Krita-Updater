
################################################################################
#                                                                              #
# Krita downloader and auto updater                                            #
#                                                                              #
################################################################################

This script is made to always have the latest version of krita available to use. 

In order to use, simply run it in place of your regular krita appimage. The
script will run krita while also checking for new versions in the background.
You will be notified if a newer version is found and when it finishes
downloading. In order to run the newer version, just close Krita and run the 
script again.

Please note this script makes the assumptions:
 • That all appimages have the original filenames;
 • That you don't have non-krita appimage files with similar names to Krita
   appimages on the same directory the script runs;
 • That you're running this script on the same directory where you put Krita's
   appimage(s);
 • That the script the directory is in has read/write permissions for the user
   running it;
 • That you will remove obsolete versions yourself. This is so you don't have
   the inconvenience of having to download an old version if there's a new,
   unaccounted bug on the newer version;
 • That KDE's website won't change the download location nor page layout where
   to download Krita appimages from. If that happens contact me. In the case I'm
   unreachable or unavailable to fix the script, the script is MIT-licensed so
   anyone is free to fix it and publish the fixed versions themselves.

For best practices, you should create a directory solely for krita appimages and
run the script from there. You don't even need to have a krita appimage
initially, you can just run this script and it will automatically download and
run it for you!

You can also specify which release type you want to run, like:
./krita.py STABLE

This is also how you specify command line parameters, like:
./krita.py STABLE --version

In case you only want to run the update and not open krita, run
./krita.py norun

Note that the script will look for the latest and most stable option within the
specified release type. So if there is version 3.0 beta and 3.0 stable and you
specify you want to run the beta version, the script will run the stable version
anyways because it's the same version only stable. But if you ask to run
prealpha and prealpha 4.0 is available, it will run the prealpha version until a
alpha, beta, rc or stable 4.0 is avilable.

If you need to contact me, the quickest way is through @jackmcslay on twitter

