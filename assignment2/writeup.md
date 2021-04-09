# Assignment 2

Laura Zheng
114769015

## Getting Started

### Creating the DB
I've provided the CSV file used to load the database (anime_processed.csv) as well as the commands I've used to set up my database (database_setup). Just as specified, I created a user named cmsc828d and a database called a2database; these user creation steps are *included* in the setup file. What I do is simply copy and paste the contents of that file into a PSQL command prompt. Make sure to replace the path of the anime_processed.csv file in the SQL commands to the one local to your machine. 

### The dataset
The dataset includes data on anime/manga/webnovels produced in the last few decades or so, and includes information on everything including the anime rating (score attribute) and general metadata such as genre, air date, air season, day of broadcast, etc. I figured this would be a fun dataset to analyze since it provides so many attributes (and that I'm also an avid anime/manga fan). 

## Which visualizations are implemented
I implemented 1) a histogram count of discrete values according to attribute, and 2) a scatterplot which display relationships between an anime's score 

### Running the visualization
Running the visualization is as simple as "python server.py", just like assignment 1, no filenamed needed to be provided, as that is used to initialize the database. Then, open localhost:8000 in the browser, and it should show up!

## Rationale 

### My design
I chose to create a [histogram](http://bl.ocks.org/jonahwilliams/2f16643b999ada7b1909) representing the count of discrete values for a certain attribute. Usually, I wouldn't think this would be a good idea for attributes with a large domain of values. But, after examining the data, I realized that the limited possibilities of values made this a viable idea. The order of the values on the x-axis does not have any intrinsic meaning, so I tried to emphasize the height of the rectangles instead. This histogram automatically organizes bars from greatest count to least count based on the present date. 

Then, I added a date [slider](https://blockbuilder.org/officeofjane/f132634f67b114815ba686484f9f7a77)  because I really wanted to do something with time as a variable. I think change over time is one of the most fascinating things to study, especially with data that has measured "popularity". The time slider represents the maximum date to consider data. It can be considered as a range slider, except the minimum is always at the earliest date. This is something that I wish I had more time to work on; I would definitely like to implement a more flexible time range filter here. 

The [scatter plot](https://www.d3-graph-gallery.com/graph/scatter_basic.html) serves the purpose of visualizing quantitative data. Since I wanted to incorporate popularity as a main factor, I made "score" a permanent attribute of the y-axis. The scatter plot and the histogram both update as the time slider changes. Moreover, both histogram and scatter plots have a filter interaction built in using the drop down menus. 

There was a point in time where I had to choose the fill color of the bars. Initially, they were going to be a color that I liked.. minor detail, but they were going to be light pink. But, referencing the work "Using color in visualization: A survey" by Silva et al., I realized that this may not be the best color for determining differences in bar heights and discerning dots on the scatter plot. Colors like yellow or lighter colors may be harder to differentiate from bar to bar, or point to point. In addition, even though we used histogram in assignment 1, I felt compelled that a histogram would be a good visualization for the purposes of this dataset too. I promise I did not use a histogram for convenience, hehe. I wanted a visualization that would convey the distribution of discrete variables succinctly. Staying true to Tufte's principle of serving a clear purpose, I believe a histogram and scatter plot are the most intuitive to understand. One regret is not having enough time to animate the scatter plot. 

The taxonomy of interactive dynamics for visual analysis (Heer et al.) greatly helped me solve a problem that I encountered early into creation of the histogram. Originally, I did not sort the histogram based on discrete value counts, and the ordering was a little all over the place. Since there is no intrinsic ordering to discrete nominal data, I thought there wasn't a way around this. However, since we are focusing on the counts of each value, I figured I would sort it to at least give structure to my visualization. Hopefully with sorting it, relationships between value counts which are close are more clear. 

### Alternatives I've considered
At first I was really looking forward to using the [parallel coordinates](http://bl.ocks.org/syntagmatic/3150059) graph from class. I was really into the vision of creating this visualization along with brushing, but after some on-paper design brainstorming, I realized it was not the best fit for my data. Barely any data of mine was quantitative. Actually, about half of it involved nominal data! Parallel coordinates would not have been a good option because it would give some implicit ordering to attribute values where they may not be any. So, I scratched that idea sadly. I feel that including this visualization, even though I am a fan of it, would be a violation of graphical integrity (Tufte) by trying to fit nominal data into a quantitative visualization. 

One thing that I have considered (albeit too late into the assignment) is varying the scatter plot point size as an encoding. While the position encoding indicates, for example, the trend between a score and the number of favorites that series got, the size could indicate the duration of each series, which would make it obvious to differentiate patterns in regular 24-minute episodes versus longer movies. 

## Challenges and Timeline
This project took much longer in areas that I did not expect. The dataset includes data types that I have never worked with. Overall, I would say that this project took around 30 hours total, with a lot of it going into learning how design in D3 works so I can modify visualizations, as well as more complex SQL queries. Being new to database languages like SQL, a lot of time went into understanding how more complex queries worked. Here are some notable challenges that took longer than you may expect: 
* Preprocessing with Python did not take too long, but was necessary. I included the preprocessing python script in the zip folder. This was done on "anime.csv" to produce "anime_processed.csv". 
* The "genre" attribute was something I insisted on being included in the visualization.. knowing what genres trended through time was a personal question of mine that I wanted to address. However, each record in the data included a *list* of genres, not just one. Thus, I had to come up with server-side queries and processing that would be able to parse arrays as attribute values. 
* The date slider was definitely the largest hurdle for interaction. Date objects / values can be finicky in general. Python has regex for parsing date values, but there was a modest amount of time spent on figuring out how the dots connected from database to server to visualization. 
* Lots of time spent on the nitty gritty of how D3 works. There were some aspects I wanted from other visualizations (like animation and vertical axes labels, etc.), and quite some time went into adapting those into my own plots. 
* Animating the histogram was pretty difficult. Actually, there are some things I wish I knew how to fix. For example, when the bar heights update with filtering, the animation causes the bars to move around. I thought that maybe this was a problem with my x axes labels not updating, but upon inspecting the data from the console at each step, I realized the bar values correspond correctly with the values from the server. Not sure why they move, and I sure wish they didn't. It definitely introduces a lie factor by implying there is some relationship between the two values that the bar moves between. 


