# CAMGS

Computer Assisted Music Generation System

## Running the Tool

To run this tool, first ensure that you have pipenv installed.  This will enable
you to easily install the dependencies for this project.  To do this, run the
command from the root of the repo:

```shell
pipenv install
```

To enter the virtual environment run:

```shell
pipenv shell
```

To begin using the tool navigate to the directory `camgs` with the command:

```shell
cd camgs
```

Before you can run the Django server, you must build the database.  To do this,
run the commands:

```shell
python manage.py makemigrations
python manage.py migrate
```

Next, you must generate a file called `secret_key.txt` in the root of the
repository.  In this file, place a 50 character alpha-numeric string.

To run the user interface, type the command:

```shell
python manage.py runserver
```

It will display a local web address.  Paste this address into a browser to view
the UI and begin using the tool.

To stop the server, use `ctrl c`.

### Output and Analysis

To run the output and analysis part of the tool, navigate to the `utilities`
directory with the command:

```shell
cd utilities
```

The `utilities` directory can be found inside of the `camgs` directory.  Note:
the Django server does not need to be running to perform the analysis.

Locate the id of your composition within the database and enter in into the
`generate_output.py` file as the `composition_id` variable.

You can now run:

```shell
python generate_output.py
```

This will create the files:

```
composition#.csv
midi#.midi
notes#.csv
xml#.xml
```

These files are located inside the `utilities` directory within the `camgs`
directory.

In the terminal, you will see the raw analysis output.

Restart the Django server if you stopped it and navigate to My Compositions. You
can now hit the play button on your composition to hear it.

If you would like to see the notation of your composition, go to
[OpenSheetMusicDisplay](https://opensheetmusicdisplay.github.io/demo/) and drop
the xml file into the window.
