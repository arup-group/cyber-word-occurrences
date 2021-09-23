# Word Occurrences

Python script to count the occurrence of a word over one or more documents.

## Usage
`python3 occurrences.py file [file ...]`

### How It Works

Say we have three files:
```
test1.txt
apple
banana
cake, cake
```
```
test2.txt
apple, apple
banana
cake
```
```
test3.txt
apple
banana
```

#### Count occurrence of words in one file:
```
$ python3 occurrences.py test1.txt
apple      1
banana     1
cake       2
```

#### Count occurrence of words in two files:
```
$ python3 occurrences.py test1.txt test2.txt
banana     2
apple      3
cake       3
```

#### Maximum count of 2
```
$ python3 occurrences.py test1.txt test2.txt --maxcount 2
banana     2
```

#### Words must exist in all files:
```
$ python3 occurrences.py test1.txt test2.txt test3.txt
banana     3
apple      4
```

#### Ignore words which appear in test3.txt:
```
$ python3 occurrences.py test1.txt test2.txt -i test3.txt
cake       3
```

## License
This project is licensed under the GNU General Public License v3.0


