# Assignment 3

Laura Zheng
114769015

In my study, there are two versions of the project: the unoptimized version (A2) and the optimized version (A3). Both versions will be running on an augmented dataset of about 1 million tuples. 

### Getting Started
* Process the dataset
	* Run "python preprocess_data.py"
	* This essentially preprocesses the data for PostgreSQL and also augments the data to around 1 million tuples.
	* This step is done once. 

Now, for both A2 and A3 versions, please do the two steps below to set up both versions. 
* Set up the database
	* Edit the database_setup.sql file and replace path of the CSV file loaded to your local path
	* Open PSQL terminal
	* Run "source /path/to/database_setup.sql"
* Set up the visualization
	* Make sure psycopg and flask python packages are installed
	* Run "python server.py"

Note: Two different databases are set up by A2 and A3. Feel free to delete after the study, they are named "a2database" and "a3database". Both databases will have 1 million tuples of data, but will be set up slightly differently for optimizations, which is why it's necessary to set up both. The visualizations take care of which database to use. 

### Tasks
* Please visit and submit this form [link](https://forms.gle/ySadJQ5k3tKUrZ238) to complete the tasks. There are only 2! A short summary:
	* Task 1: Free exploration
	* Task 2: Describe the shift in genre popularity
* This shouldn't take more than 10 minutes after setup, hopefully. If you took significantly more time, I would like to know in the form :-)
* If there are any issues/bugs with setting up the visualization, please contact me at lyzheng@umd.edu, I will respond ASAP. 






