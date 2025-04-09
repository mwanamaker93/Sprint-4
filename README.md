# Sprint-4
Project for Sprint 4

Description: This project is for the purpose of practice in using streamlit and plotly via the render platform to do analysis and visualization for a vehicle advertisements dataset. There will be scrollable dataframes which were used during the project, and several distributions oriented around price, vehicle condition and brand available as well. A selectbox is used for one histogram to compare one brand to another and checkbox to adjust another histogram's x-axis.

**Checkbox in question adjusts histogram's x-axis: displaying vehicle age 3 to 10 when toggled. It is toggled by default.**

Web App: 
The web application can be accessed on render here: https://sprint-4-7nnw.onrender.com

How to install and run locally: 

Clone repository with the following command in your terminal: git clone https://github.com/mwanamaker93/Sprint-4.git

Then create a virtual environment.
Install associated packages as seen in (requirements.txt).

You should be seeing these associated files: 

.gitignore

EDA.ipynb

README.md

app.py

requirements.txt

vehicles_us.csv

In your repository’s virtual environment run:

streamlit run app.py

To run on the web: 

Open account on render.com and create a new web service.

Create new web service linked to GitHub repository. 

Add the following to your build command: pip install streamlit & pip install -r requirements.txt

Add to Start Command: streamlit run app.py

This will launch an additional tab with the app. 
