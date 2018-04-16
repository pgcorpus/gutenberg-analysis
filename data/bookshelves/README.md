# Bookshelves pages
These are html files of all PG wiki bookshelf records
Scrapped on April 2018 as follows:
```
wget --random-wait -r -p --no-parent -e robots=off -U mozilla http://www.gutenberg.org/wiki/Category:Bookshelf
mv www.gutenberg.org/wiki/*Bookshelf* .
rm -rf www.gutenberg.org
```

