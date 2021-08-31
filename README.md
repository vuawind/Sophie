# Sophie
A simple Slack bot with question selections and answers. This was one of project during an internship from Telio.

## Installation
    pip install pandas openpyxl
## Features
* Read excel file with questions and answers.
* Easy to set up and use in an organization.
* Submit a ticket if the question is not in the selection.
## Usage
First, look up how to build and run a Slack app, go through the basics of building a Slack app. A recommended guide is: [Guide to build Slack app](https://www.digitalocean.com/community/tutorials/how-to-build-a-slackbot-in-python-on-ubuntu-20-04)

After you are done with setting up a Slack app, export necessary tokens

    export SLACK_SIGN="your signin secret token"
    
    export SLACK_BOT_TOKEN="your oauth bot token"

Run the Slack app with

    python3 app.py
    
Create a global shortcut and name the callback id a sophie.
### Set up excel file
For the chat bot to work, follow the excel template
questions | answers
------------ | -------------
example question 1 | example answer 1
example question 2 | example answer 2

Each sheet will be the section of the questions and answers.
