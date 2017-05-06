# Software Setup
Below are the steps required to set up the software related to MedSession. Included in these steps are how change permissions, set up SSH keys for rsync, and run the software (assuming the hardware has been set up as described above).

## Changing Permissions
On a Linux system, we will need to change permissions to allow the system to connect freely to the Flora controller, as well as store and modify information with the `/tmp` directory.

### Connect to Flora Automatically
On Linux machines, the owner of USB connections must be within the group ‘dialout’ to access. To place your user within that group use the command, where USERNAME is the user that will be running the service:

`usermod -a -G dialout USERNAME`


### Modify Data with `/tmp` Directory
The service and session manager save and access data from within the `/tmp` directory. However, this directory is only writable by the root user by default. To change this, run the command (and enter the root user password when prompted): 

`sudo chown root:root /tmp`

`sudo chmod 1777 /tmp`

## Setting Up SSH Keys
This sections describes the process to create and trade SSH keys between the machines that will be using the system. SSH keys are necessary to enable secure communication between computers, while also enabling the transfer to reconnect automatically. For MedSession, this will need to be done on both machines, to allow each of the computers to transfer files freely.

### Generate SSH Key
On the machine that you are sending information from, run the following commands in the command line to generate public SSH keys, with no password:

`ssh-keygen -f ~/.ssh/client_rsa -q -P ""`

The file called `client_rsa.pub` is placed on another machine to allow you to establish SSH connections with them. The `.pub` file can be freely sent, whether through email or instant message. The key cannot be used to get into your own machine, so you are not in danger of any malicious activity. 

### Enabling Secure Access
Once the other machine has your public key, they will need to add it to their authorized keys. If you do not have a file to store authorized keys, you will need to create that file, and copy the contents of the key into that file. Here are the commands:

`touch ~/.ssh/authorized_keys`

`chmod 0644 ~/.ssh/authorized_keys`

`cat /path/to/client_rsa.pub > ~/.authorized_keys`

## Running the Software
The software suite consists of two separate Python3 programs: `service.py` and `manager.py`. In order to use these, you should run the following commands to ensure you have the required packages:

`sudo apt-get install openssh-server python3-pip`

`sudo apt-get update`

`sudo pip3 install -r /path/to/wearables_design/Software/requirements.txt`

###Service - Interacting with Flora
The service allows your machine to connect to the Flora controller to collect and store the data. For every context switch, the service will store that section of data into a different file. To run the service, make sure that you have changed the permissions as described above, then run the command:

`python3 service.py -R`

While it is running, you should see outputs that represent the byte that was just sent, then also the complete line of data that the controller was attempting to send. To stop the service, simply press `CTRL+C`. All files related to the session are stored in a folder in `/tmp` with a randomly generated string, which is considered our ‘session ID’ for this project.

###Session Manager
The session manager has two main functions: packaging and sending sessions, and extracting sessions. The steps to use each of these features are described below. Make sure that all permissions have been changed, and packages have been installed as described above. To read the manual on the file, use the following command:

`python3 manager.py -h`

####Packaging and Sending Sessions
To add to the information within a session, a user can include other files within the session directory created by the service. To do so, simply copy the files within the directory inside of `/tmp`. Use the `send` mode.

Sending sessions searches for a specific session with the `/tmp` directory, compresses all files that it is capable of compressing, packages the directory as a `tar.gz` file, and uses rsync to send it securely to another machine. To send a session, use the session ID generated from the service, or use another directory name within `/tmp`. The command would be structured as follows:

`python3 manager.py --mode=send --priority={low, med, high} session_id username@host_ip:/home/user/`

The priority determines which speed rsync uses. The manager will run until the session is completely sent, and will retry after a certain amount of time if the transfer fails. It has a time-based context-awareness; it will change upload speeds based on priority and time. High priority does not use any bandwidth limiting.

####Extracting Sessions
To extract a session that has been sent, you will use the `recv` mode of the manager. As the session parameter, you will use the full path to the session, including the file extension. The command would be:

`python3 manager.py --mode=recv /path/to/session.tar.gz`

This will extract the tarfile and store it in the session folder for access. 
