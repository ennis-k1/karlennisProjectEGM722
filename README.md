# Analysis Of Social Housing In Northern Ireland

The aim of this code is to analyse the current social housing market within Northern Ireland. At present, social housing waiting lists are annually on the increase with the development market unable to meet demand, this is particularly the case in certain areas of the country.

The Northern Ireland Housing Executive periodically releases a quantity of units which are required to meet the demand in small settlements within each Local Government District. The current assessment period runs from 2022 to 2027, therefore this analysis considers both the quantity of units required and the quantity of units being delivered within this period.


## Requirements / Dependencies


•	Visual Studio Code or similar IDE

•	Anaconda

•	Chrome or similar browser

•	Github



## Installation

Visual Studio Code
Download VS Code from here
And follow the on screen instructions.
GIT
Details of installing GIT can be found at : Install GIT
Fork The Repository
Click or copy and paste the above repository link, if not already logged in you will now have to log in to git.
 
Click Fork in the upper right corner,
 
Make sure you are satisfied with the options, Copy the main branch only is not important in this instance as the repository only has one branch.
Click Create Fork, this will copy the entire repository over to your account, make a note of the new repository URL.

Clone The Repository
The Repository can be cloned in several ways:
Option 1 – Visual Studio Code
1.	Open Visual Studio Code, on the welcome page you will notice “Clone Git Repository”, select this and an input box will appear at the top of the screen.
 
2.	Paste the url from the repository you cloned earlier, this will create a clickable option to “Clone from URL ….”, click this.
 
3.	A file explorer dialog will appear to allow you to select a location to save the repository files to, this is where the files will download to. Once a location is selected, you will see an info dialog in the bottom right corner of visual studio code detailing the progress of the cloning. Once complete an option box will appear asking if you would like to open the repository, select an option.
 
N.B: “Open” – opens the code in the existing Visual Studio Code Window,
	“Open in New Window” – opens the code in a new instance of Visual Studio Code.

You should now see all files contained in the repository
 

Option 2 – Github Desktop
If you chose to install GitHub Desktop as your earlier option you can clone the repository by following the instructions at :
Clone Repo Using GitHub Desktop

Option 3 – Git Command Line Interface
1.	Open a command prompt by selecting your windows icon and begin typing cmd, click on the command prompt app, which will open a black command line dialog box.


 
2.	Open a separate windows file explorer, this can be done using the folder icon on the bottom task bar, or by again going to the windows icon and being typing file explorer. Navigate to the location where you would like to clone the repo to.
 
We will now tell the command prompt to navigate to this folder.
*HANDY TIP: If you click in the folder address bar, in this case beside the :
“This PC > OC (C:)> Ulster University > Demo”
The location will become highlighted and selected, press “CTRL” & “C” to copy this address to the clipboard.
3.	Return to the command prompt window, to navigate it to the required folder type 
“cd “ followed by a space, then “CTRL” & “V” to paste the folder location we copied in the last step, press return.

 
You should now see the command prompt in the new folder location.
4.	In the same command prompt, type 
5.	“git clone” followed by a space, then paste the url of the repo that you earlier made note of which you forked.
The command line will progress through the procedure and when complete will return to the original command line. In file explorer you should now see all of the files downloaded from the git.
Installing & Setting Up Conda / Anaconda

1.	Navigate to
https://docs.anaconda.com/free/anaconda/install/
and select the download for your operating system. Once installation is completed proceed to setting up your Conda Environment

2.	To create an environment in Anaconda we will use the yml file which is in the cloned repository. First open Anaconda navigator by clicking the windows icon and typing “Anaconda”.
3.	With Anaconda open, click on the Environments Tab from the left hand menu
 
4.	Select import from the bottom menu bar.
 
Browse to the cloned repo folder location and select the environment.yml file and click Import.

The yml file contains a list of channels to install packages from and dependencies the code relies on.

This can take some time to create, once complete you will see the new environment name appear in the environment tab of Anaconda

5.	To select the environment you just created, in Anaconda select the Home tab, you will notice two drop down boxes, the first lets you filter the applications on display, the seconds lets you choose the environment you would like to run. Choose your newly created environment.
 

## Run The Code
1.	Open Visual Studio Code. It is recommended to ensure the “Pylance” and “Python” extensions are enabled within VS Code.
2.	Ensure that your new Anaconda environment is selected. This can be determined in 2 ways:
 
A.	Click “Terminal” -> “New Terminal”, to open a new terminal at the bottom of the screen. If the command line has “(base)” at the beginning, you are not in your new environment.
B.	On the blue bar along the bottom of the screen towards the right hand side, you will notice “(‘base’:conda)”, indicating you are not in your new environment,
To change environments, click on the “(‘base’:conda)” on the bottom blue bar and you will notice a dropdown appear at the top asking you to select an interpreter, select your newly create environment. You will notice the name on the bottom blue bar change to your selected.


3.	Open the “index.py” file, in the top right corner you will notice a run button, click this
 

Any text outputs that are contained in the code will print to the terminal.

4.	To View the “Map” webpage:
Click “Go Live” on the bottom blue bar on the right, this will start your local server. Take note of the port number which appears, in this case port 5500.
 



5.	Go to your web browser and enter:
http://localhost:5500/map.html
in your address bar, replacing the 5500 with your own port number. You should then see an interactive map appear.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[View License](https://github.com/ennis-k1/karlennisProjectEGM722/blob/main/LICENSE)