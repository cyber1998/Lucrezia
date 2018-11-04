# Lucrezia

This small application helps you to read, write and update your google
spreadsheets right from the comfort from your command line! I created
this to manage all the series that I watch and have a clear overview of
what I want to watch next.

#### Step 1

Clone the repository first and then create a virtual environment for this
project (recommended).

---
#### Step 2

Activate your virtual environment, change to the project directory you just cloned
and type `pip install -e .` to install the app along with it's dependencies.

---

#### Step 3
Follow step 1 of [this](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the)
guide to get your own `credentials.json` in your directory. <br> 

---

#### Step 4
Create a new file and name it `spreadsheets.json`. In it, do the paste this format:
```
{
  "spreadsheets": [
    {
      "serial_no": 1,
      "name": "Name of your series",
      "creds": {
        "id": "id of your spreadsheet",
        "range": "range name desired"
      }
    }
  ]
} 
```
To find out the `id` and `range` of your spreadsheet, please refer the guide mentioned [here](https://developers.google.com/sheets/api/guides/values)

---
### Commands available

- `lucrezia get`: Get the contents of the spreadsheet
- `lucrezia update_existing`: Update an existing entry in the spreadsheet
- `lucrezia update_new`: Update the spreadsheet with a new entry