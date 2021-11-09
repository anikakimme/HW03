# HW 3: Scraping from ebay
Check out the project instructions [here](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03)
## Explanation of the ebay-dl.py file 

They ebay-dl.py file contains a program that scrapes ebay for information and stores the results in a json file. It uses the argparse library to get a search term for any item on ebay (e.g. hammers, stuffed animals, clothes, shoes, textbooks, etc.). Then the program will download the first 10 pages of results on the search term unless fewer pages are specified. The program also uses beautiful soup to take out items from the search results. Finally, the program creates a list with dictionaries for six categories. These include (1) the name of the item on ebay (2) the price of the item in cents (3) the status of the item such as whether it is new or refurbished (4) the price of shipping (5) whether the item has free returns (6) and how many items have been previously sold. 

At the end, the program will return a json file named after the search term that has the information for all of these categories for each item in the first ten pages of the search term. If the tag --csv is added to the command then a csv file can be created instead of a json file. 

## How to run the ebay-dl.py file
To run the ebay-dl.py file and receive a json file of your results the following command should be used:

```
python3 ebay-dl.py 'search term'
```

where search term can be whatever you want to look for on ebay (such as earrings or a laptop).

For example:


    python3 ebay-dl.py 'Thanksgiving'


To only get one page the command line flag `--num_pages` should be used: 

```
python3 ebay-dl.py 'search term' --num_pages=1
```

To get multiple pages the number of pages can be changed. This command will give pages one and two:

```
python3 ebay-dl.py 'search term' --num_pages=2
```

To get a csv file instead of a json file the command line flag `csv` can be added:

```
python3 ebay-dl.py 'search term' --csv
```

Both the command line flag `--num_pages`and `--csv` can be used at the same time:

```
python3 ebay-dl.py 'search term' --num_pages=1 --csv
```

I used the following commands to generate the files in this repository:

```
python3 ebay-dl.py 'Earrings'
python3 ebay-dl.py 'Harry Potter'
python3 ebay-dl.py 'Thanksgiving' 
python3 ebay-dl.py 'Earrings' --csv
python3 ebay-dl.py 'Harry Potter' --csv
python3 ebay-dl.py 'Thanksgiving' --csv
```