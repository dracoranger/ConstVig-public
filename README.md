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

#### Prerequisites  
To run Constant Vigilance, you will need to install SplitCap and the pytest and dpkt python libraries. SplitCap can be found online. The python libraries can be installed by running the instillation.bat or installation.sh files, assuming you have pip and it's mapped to your python3 installation.  

#### Installing  
Run the installation files from the command prompt. Install SplitCap by following this link: https://www.netresec.com/?page=SplitCap  
A backup is present in the Constant Vigilance SharePoint.    

### Running the tests  
To run tests, navigate to the code file. Running pytest test.py will run all the tests for this program.  
For optimal testing, place the file small.pcap from the CV SharePoint (http://usmasvddbackus/Courses/401-2/18SDP/Constant%20Vigilance-An%20Attack%20Defend%20CTF%20Tool%20Suite/IT%20Final%20Documents/Forms/AllItems.aspx?InitialTabId=Ribbon%2EDocument&VisibilityContext=WSSTabPersistence) in the put_pcaps_here folder. This tests the networkIn module against a known data point.  

### General information  
dad.py is the main launcher file. Dad launches childNO and kills it at the end of a round. Dad re-launches childNO every round of the CTF exercise. For future developers, it is possible to add more child processes for dad to launch and maintain, if desired.  You will need to create a storage system and a way of iterating through this system for the various children, so it is somewhat involved.  
childNO.py sends out attacks and chaff to the rest of the network. The attacks and chaff are user-provided. To add an attack or chaff, place the script into the appropriate folder (attacks for attacks, chaff for chaff) and add the appropriate command line argument in the conf file.  
childNI.py analyzes and sorts inbound network traffic using pcaphandler. Note that childNI does not run constantly, as that would generate an absurd amount of small pcaps and would make navigating to relevant flows difficult. To analyze the network traffic, put the pcaps from tcpdump into the put_pcaps_here folder. ChildNI and pcaphandler will take the pcaps, convert them to .csv files, scan the payloads for known flags (according to the regex in the conf file), and add any CSVs with flags to a database. The .csv files are then put into a the processed folder. By running childNI.py in interactive mode, you can query the sqlite database that stores flows with flags, and search for flags found by port and service.  
pcaphandler.py searches for known flags that the user enters in the configuration file.  
constvig.conf is used to configure a number of things that might otherwise be hard coded into the scripts. Explanations for each section are present in the conf file once it is generated.  
utilities.py stores code from processes that are used by other processes.  
test.py contains the testing harnesses for the code.  
ssResponse.py is the scoring server.  
installation.bat and installation.sh are for installing Constant Vigilance Code.  

### Authors  
The authors of Constant Vigilance are Cadets Tate Bowers, Abigail Kronenberg, Jaryn Villegas, and Gabriel Yarbrough.

### Acknowledgments  
Constant Vigilance would like to thank LTC Harvie, our instructor,  and LTC Moody, our product owner, for providing valuable guidance and suggestions throughout the year. We would like to thank LTC Morrell for his valuable Python module recommendations. Constant Vigilance would also like to thank the Cadet Competitive Cyber Team (C3T) and their OIC, LTC Moody, for allowing us to observe and collect data from their capture the flag exercise and for responding to our survey. We'd like to specifically thank Cadet Kyle Fauerbach of the C3T for giving us C3T's input on the project.
