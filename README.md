# bikeshare

**bikeshare** is a Python script which displays US bikeshare statistics for Chicago, New York, or Washington during the first half of 2017, with an option to filter the data by month and/or day of the week.

## Dependencies

* [Python 3](https://www.python.org)
   * [NumPy](https://www.numpy.org)
   * [Pandas](https://pandas.pydata.org)

## Installing

No installation is necessary. Just make sure that `bikeshare.py` and `bikeshare_data/` are in the same directory before running the script.

## Running

Navigate to the directory containing `bikeshare.py` and run the following command:

```
$ python bikeshare.py
```

Note: On some systems, the command may be `python3`.

## Usage

The following bikeshare statistics are available:
* `Time` - most frequent times of travel
* `Station` - most popular stations and trip
* `Trip Duration` - total and average trip duration
* `User` - statistics on bikeshare users

## Troubleshooting

The following error indicates Pandas is not installed:

```
$ python bikeshare.py
Traceback (most recent call last):
  File "bikeshare.py", line 3, in <module>
    import numpy as np
ImportError: No module named 'numpy'
```

Use either PyPI or Conda to install it, depending on your setup.

```
# PyPI (may need to use pip3 command)
pip install pandas
```

```
# Conda
conda install pandas
```

If you get an error like the below, verify you're running Python 3.0 or higher with `python -V`. If this lists a Python 2 version and you're certain Python 3 is installed, try running the script with the `python3` command.

```
Traceback (most recent call last):
  File "bikeshare.py", line 394, in <module>
    main()
  File "bikeshare.py", line 375, in main
    city, month, day = get_filters()
  File "bikeshare.py", line 354, in get_filters
    city = get_city()
  File "bikeshare.py", line 338, in get_city
    city = valid_input(cities, message)
  File "bikeshare.py", line 291, in valid_input
    item = input('\n' + message + '\n').lower()
  File "<string>", line 1, in <module>
```

## Example

```
$ python bikeshare.py
----------------------------------------

Hello! Let's explore some US bikeshare data during 2017!

Would you like to see data for Chicago, New York, or Washington?
New York

Would you like to filter the data by month, day, both, or neither?
Month

Which month? - January, February, March, April, May, or June?
March

Restricting data to New York during March 2017.

----------------------------------------

Calculating The Most Frequent Times of Travel...

The most popular day for traveling is Wednesday.

The most popular hour of the day to start your travels is 5:00 PM.


Press Enter to continue...

----------------------------------------

[...]
```

## Contact

#### Mayka Macinkowicz
* e-mail: m.macinkowicz@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
