# Polar, Developing code for processing trainingsdata 
3-10-'23
## Goal: 
    <li><strong>unlocking training data</strong><li>
    <li><strong>Practicing software development skills</strong><li>
        
## History 
Originally started putting data registered with my polar devices. 
And the wish to classify the training data.
It is extended with data registered with Garmin.
Code is written, with some shell scripts. 


## Workflow philosophy.
Source data is in the form of files, with a representing a training.
The general workflow is to read these datafiles and put the data in an database (MongoDB) 
The database runs in Docker container. 
Configuration of the app is aranged with a toml file. 

## Present state
Almost everything is work in progress. 
Coupling between files and database is in a reasonable.
Analysis tools is very simple and not foul proof. 
Web interface is for a next phase.


# Backup Database
See mongodb/backup-notes.txt