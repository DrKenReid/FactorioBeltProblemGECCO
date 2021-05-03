# FactorioBeltProblemGECCO

This repository contains the Factorio interface first described in our pre-print: https://arxiv.org/abs/2102.04871

## Installation instructions for Docker (recommended)

1) Install docker  ([link](https://www.docker.com/products/docker-desktop)).
2) Install your preferred image (such as goofball222's image [https://hub.docker.com/r/goofball222/factorio/](here)).
3) In the docker-based directory, navigate to the /factorio/mods/ sub-directory. Place the interface_0.1.1 folder found here on Git (from within the /Mod/ folder) within the /factorio/mods/ folder.
4) Modify all required settings for your local machine. Some changes we considered include:
4.1) Ports for RCON
4.2) Ports for your docker container - though defaults should suffice
4.3) Auto-save interval
4.4) RCON.pwd
4.5) Server visibility
5) Restart docker / container.
6) The interface should now be working.

If you're having issues with docker (we certainly had a few) pay close attention to IPs and ports made available within docker and make sure they align with those in RCON settings. We cannot assist with any docker related issues - so please only contact us with issues relating to the interface itself.

## Installation instructions for Factorio (recommended for testing purposes only)

1) Purchase Factorio (I recommend via the Factorio website, as more money goes to Wube this way - otherwise you can purchase it on Steam)
2) Download Factorio.
3) Navigate to the mods folder 
For Windows: C:\Users\user name\AppData\Roaming\Factorio\mods\
For Linux: ~/.factorio/mods
For Mac OS X: ~/Library/Application Support/factorio/mods
4) Place the /interface_0.1.1/ folder into the mods folder.
5) Run Factorio, click on "Mods", and turn on interface_0.1.1

## Running 

1) Write your optimizer in your preferred language, which can create *.txt files containing integer-encoded solutions (see FactorioBeltProblemGECCO/blob/main/Interface/input/matrix.txt for an example).
2) In the language of your choice, call the interface script (FactorioBeltProblemGECCO/Interface/interface.py) with the correct parameters (see interface.py's main() method for details).
3) Repeat #2 as many times as required with new input files and parameters.

Of course running on docker is much faster in a graphic-less mode than the standard Factorio version, but it can be useful to see the solutions visually to troubleshoot the solutions your optimizer creates.

Please get in touch with Dr. Ken Reid for any collaboration requests: ken@kenreid.co.uk
