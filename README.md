# ay18_capstones
This is the base repository for XE401-XE402 AY181-182 capstone project code.

One member of your capstone team should FORK this repo (click the button in the top right corner of GitHub).
The same team member should navigate to the fork, and click "Settings"
Rename your fork with a short version of your project name.
Under "Collaborators & Teams" in the Settings, remove the "CL2018" team (keep "Faculty" access), and individually add your capstone teammates as well as any other collaborators.
Replace this README with text that includes your project name, members, and a brief description.
Commit your changes


*************
## Constant Vigilance
Constant Vigilance analyzes inbound network traffic for CTFs and automatically launches outbound attacks every round of the CTF. The critical portion of Constant Vigilance is in the Code folder.
### Getting Started
To use Constant Vigilance,

####Prerequisites
To run Constant Vigilance, you will need to install SplitCap. Everything else will install automatically when the installation files are run.
####Installing
Run the installation files from the command prompt. Install SplitCap by following this link: https://www.netresec.com/?page=SplitCap

dad.py is the main launcher file. Dad launches and manages childNO. Dad re-launches childNO every round of the CTF exercise. For future developers, it is possible to add more child processes for dad to launch and maintain, if desired. That was the original design of dad and it should not be difficult to re-integrate this feature.
childNO.py sends out attacks and chaff to the rest of the network. The attacks and chaff are user-provided. To add an attack or chaff, place the script into the appropriate folder (attacks for attacks, chaff for chaff).
childNI.py anlayzes and sorts inbound network traffic using pcaphandler. Note that childNI does not work in real time. To analyze the network traffic, put the pcaps from tcpdump into the put_pcaps_here folder. ChildNI and pcaphandler will take the pcaps, convert them to .csv files, scan the payloads for known flags, and add any CSVs with flags to a database. The .csv files are then put into a the processed folder.
pcaphandler.py searches for known flags that the user enters in the configuration file.
constvig.conf is used to configure a number of things that might otherwise be hardcoded into the scripts. The majority of the interaction users will have with the configuration file will be to add known flags so they can be found in the inbound traffic.
utilities.py stores code from processes that are used by other processes.
test.py contains the testing harnesses for the code.
ssResponse.py is the scoring server.
installation.bat and installation.sh are for installing Constant Vigilance Code.
