# Team 76 Data Warriors

## DESCRIPTION

Note: in order to view this file in a better format, render it as a markdown file.

This folder contains the whole code for the project by *Team 76 Data Warriors*. There are two main folders in this project *Housing Recommender System* and *School_CleanUp*. The latter is just a legacy folder containing one python script and some of the datasets we collected for school data. The former folder is the most important one and will be described in detail.

**Housing Recommender System**
This folder contains the main code where all our files and the application executable are found. There are additionally some raw and processed datasets contained within the subfolders. The purpose of each subfolder are:
- Database: contains python code for connecting to a PostgreSQL database. This was initially going to be our main storage solution, but due to the lack of time the migration could not be completed.
- DataExtraction: contains several python scripts, notebooks and data files for both raw and processed data. This is the folder where most of the data experimentation was carried out.
- DataVisualization: contains python scripts necessary to plot some of the visualizations for the final page. There is additionally one dataset used to generate the choropleth maps of the United States with each county outlined.
- ML: this folder contains all the models used to generate the predictions. The python scripts are all separated in subfolders respective to each different model. Additionally, there are some final datasets used to generate predictions.
- Static: used to store images, video and HTML templates. In general, front-end files that are immutable could be found here.
- templates: HTML files used to render the visual application in a web browser.

The application entry point (*app.py*) could also be found on this folder.

## INSTALLATION
The next steps are necessary to get the application working. Prerequisites for this includes having Python installed in your system and the "python" and "pip" commands added to the path of your shell profile. To know if you comply with all of them, just open a terminal and type "python" is there is no error, you have python installed. Do the same but type "pip" to know if Pip is installed in your system.

We recommend using at least Python 3.8.13.

Follow the next instructions to get your code working.

1. To setup the code go to the *Housing Recommender System* folder.
2. Open a terminal on the aforementioned folder.
3. Once on that folder, type the following command: ```pip install -r requirements.txt``` to install the necessary dependencies.

## EXECUTION

To get the application working, go to the *Housing Recommender System* folder and open a terminal there. Follow the next two instructions to start the application.

1. Run the application using the command ```python app.py```
2. Open a web browser and go to ```http://127.0.0.1:5000```

You should then see a screen with seven different option to choose preferences. Each of them has a selector to choose your preferred value and a slider to select the importance you give to that specific variable.

When you have selected all the values according to your preferences, click on the "Get Recommendations" button and you should be redirected to a new page where you can see visualizations for the different variables according to data we have collected. The generated recommendations take some seconds to load and are displayed in the "Recommended Counties" graph.

## DEMO VIDEO

