# NextLogic-Intern-DTR

### Prerequisite

- Python.
  - [Click here to download Python](https://www.python.org/downloads).
- Git bash.
  - [Click here to download Git](https://git-scm.com/downloads).
- Telegram Bot.
  - [Watch here how to create a telegram bot](https://www.youtube.com/watch?v=aNmRNjME6mE).
- Google Service API Key.
  - [Watch here how to get your Google Service API Key](https://www.youtube.com/watch?v=anqwLrVPBYg&feature=youtu.be).
- Virtual Environment .
  - To install Virtual Environment, **`pip install virtualenv`**

### Setup

1. Extract the files.
2. Open the folder.
3. Open git bash terminal.
4. To create virtual environment, **`python -m venv venv`**
5. To activate the virtual environment, **`source venv/scripts/activate`**
6. To install all package needed, **`pip install -r requirements.txt`**
7. Change the Telegram Bot API Token in `line 20`
   > API_TOKEN = '5434114429:AAHW-aXVZtza22fBjb8-JvL0Wqax7DHIGTo'
8. Remove `APIKEY.json` and replace it with your own..
9. Change the pygsheet configuration in `line 12 - 17`
   > \# Pygsheet Config  
   > service_file = r'APIKEY.json'  
   > gc = pygsheets.authorize(service_file=service_file)  
   > sheetname = 'CvSU Interns Design, Development, and Management Reference Sheet | 2022'
   > sh = gc.open(sheetname)  
   > wks = sh.worksheet_by_title('Time Logs')  
   > wksnames = sh.worksheet_by_title('Authorized Interns')

### How to run

```
python main.py
```
