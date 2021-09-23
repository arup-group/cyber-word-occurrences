#!/usr/bin/env python3
#Title       : Count Occurrences
#Description : Count occurrences of duplicated words over multiple documents
#Author      : QuidsUp
#Date        : 2021-09-22
#Version     : 1
#Usage       : occurrences.py file [file ...] [-i file of words to ignore]

#Standard Imports
import argparse
import csv
import os
import re

#Look for words starting with alphabetic char followed by 2-60 alphanumeric chars
wordfinder = re.compile(r'\b([A-Za-z][\w\-\.]{2,60})\b')

class DocumentAnalyser:
    """
    DocumentAnalyser class can be used in multiple ways:
    1. Count the occurrences of words in a single document (checkdocuments parameter)
    2. Count the occurrences of words in multiple documents (checkdocuments parameter as a list), but only show the count of words that appear in all documents
    3. As with 2. but disregard words that appear in "ignoredocuments" parameter

    Parse the documents to be checked when initialising the class

    find_duplicates will provide a dictionary or words and count of occurrences
    display_results calls find_duplicates and displays the results on screen
    save_results calls find_duplicates and saves the results to results.csv
    """
    def __init__(self, checkdocuments: list, **kwargs):
        """ DocumentAnalyser Init
        Processes parsed values and counts occurrences of words in the documents supplied

        Parameters:
            checkdocuments: string of text to check or list text strings to check
        Optional Parameters
            ignoredocuments: string of text to check or list text strings to ignore
            mincount: Minimum count for duplicate words (default 1)
            maxcount: Maximum count for duplicate words (default 256)

        """
        self._mincount = 1
        self._maxcount = 256
        self._documents = list()
        self._ignorewords = set()

        ignoredocuments = kwargs.get('ignoredocuments', None)
        self._mincount = kwargs.get('mincount', self._mincount)
        self._maxcount = kwargs.get('maxcount', self._maxcount)

        self.__process_ignore(ignoredocuments)
        self.__process_check(checkdocuments)


    def __add_ignore(self, textdata: str) -> None:
        """
        Add words from a string to _ignorewords set
        Not bothered about count or duplicates (since sets will ignore duplicates)
        """
        #Use finditer regex to find all alphanumeric words in textdata
        words = wordfinder.finditer(textdata)

        for word in words:
            self._ignorewords.add(word.group(0))           #Add word to _ignorewords set


    def __count_occurrences(self, textdata: str) -> None:
        """
        Count the number of times a word appears in a string
        Disregard any words that appear in the _ignore set
        Add resultant dictionary of words to _documents list
        """
        worddict = dict()                                  #Dictionary of words found

        #Use finditer regex to find all alphanumeric words in textdata
        words = wordfinder.finditer(textdata)

        for word in words:
            #Is word in _ignorewords set?
            if word.group(0) in self._ignorewords:
                continue
            #Check if the word is already in worddict
            if word.group(0) in worddict:
                worddict[word.group(0)] += 1
            #Or add it to worddict
            else:
                worddict[word.group(0)] = 1

        #Add the current worddict to _documents list
        self._documents.append(worddict)


    def __process_check(self, checkdocuments: str or list) -> None:
        """
        Process documents to check
        Parameters:
            checkdocuments can be either a single text string or list of strings
        """
        if checkdocuments is None:
            return
        #Single text string to count
        if type(checkdocuments) == str:
            self.__count_occurrences(checkdocuments)
        #Multiple text strings to count
        else:
            for document in checkdocuments:
                self.__count_occurrences(document)


    def __process_ignore(self, ignoredocuments: str or list):
        """
        Process documents to ignore
        Parameters:
            ignoredocuments can be either a single text string or list of strings
        """
        if ignoredocuments is None:
            return
        #Single text string of words to ignore
        if type(ignoredocuments) == str:
            self.__add_ignore(ignoredocuments)
        #Multiple text strings of words to ignore
        else:
            for document in checkdocuments:
                self.__count_occurrences(document)


    def display_results(self) -> None:
        """
        Find duplicate words then print resultant count to screen
        """
        worddict = self.find_duplicates()

        if worddict is None:
            print('No results found')
            return

        for key, value in worddict.items():
            print(f'{key:<32} {value}')


    def find_duplicates(self) -> dict:
        """
        Count number of duplicate words from dictionaries that appear in all the _documents list

        Returns:
            sorted dictionary of words with occurrences of each word
        """
        results = dict()
        documentslen = 0
        foundin = 0                #Count number of documents a word has been found in

        documentslen = len(self._documents)

        if documentslen == 0:
            return None

        if documentslen == 1:
            results = self._documents[0]
            #Sort by number of occurrences from lowest to highest
            results = dict(sorted(results.items(), key=lambda x:x[1]))
            #Limit results to between min and max count
            results = {key: value for key, value in filter(lambda x: x[1] >= self._mincount and x[1] <= self._maxcount, results.items())}
            return results


        #Review all words in dict zero
        for word, firstcount in self._documents[0].items():
            foundin = 1
            wordcount = 0
            #Check all dict's from one to n
            for i in range (1, documentslen):
                if word in self._documents[i]:
                    foundin += 1
                    wordcount += self._documents[i][word]

            #Has word not been found in all dict's?
            if foundin < documentslen:
                continue

            wordcount += firstcount                        #Include the count from dict 0

            #Check if total count is in the specified min/max range
            if wordcount >= self._mincount and wordcount <= self._maxcount:
                results[word] = wordcount

        #Return sorted worddict
        return dict(sorted(results.items(), key=lambda x:x[1]))


    def save_results(self) -> None:
        """
        Find duplicate words then save results to a csv file
        """
        csvresults = list()
        titles = list(['Word', 'Count'])
        worddict = self.find_duplicates()

        if worddict is None:
            print('No results to write to results.csv')
            return

        csvresults = list(worddict.items())

        with open('results.csv', 'w') as fh:
            csvout = csv.writer(fh)
            csvout.writerow(titles)
            csvout.writerows(csvresults)

        fh.close()


def load_file(filename: str) -> str:
    """
    Load contents of file and returns as a string
    Check file exists
    Read all lines of file

    Returns:
        String of all lines in file
        Blank string if file doesn't exist or error occured
    """
    if not os.path.isfile(filename):                       #Check file exists
        print(f'Error: Unable to load {filename}, file is missing')
        return ''

    try:
        f = open(filename, 'r')                            #Attempt to open file for reading
    except IOError as e:
        print(f'Error: Unable to read to {filename}')
        print(e)
        return ''
    except OSError as e:
        print(f'Error: Unable to read to {filename}')
        print(e)
        return ''
    else:
        filelines = f.read()
    finally:
        f.close()

    return filelines


def main():
    mincount = 0
    maxcount = 0
    checkdocuments = list()
    ignoredocuments = ''

    #Process arguments
    parser = argparse.ArgumentParser(description = 'Document analyser')
    parser.add_argument('files', nargs='+', help='Files to analyse')
    parser.add_argument('-i', '--ignore', help='Files of words to ignore')
    parser.add_argument('--maxcount', type=int, help='Maximum word count')
    parser.add_argument('--mincount', type=int, help='Mimimum word count')
    args = parser.parse_args()

    #Load all text files to check for duplicates
    for filename in args.files:
        filelines = load_file(filename)
        checkdocuments.append(filelines)

    #Any text documents to check for ignore words?
    if args.ignore is not None:
        ignoredocuments = load_file(args.ignore)

    #Set maximum and minimum word count based on arguments or leave as defaults
    mincount = args.mincount or 1
    maxcount = args.maxcount or 256

    docanalyser = DocumentAnalyser(checkdocuments, ignoredocuments=ignoredocuments, maxcount=maxcount, mincount=mincount)
    docanalyser.display_results()
    docanalyser.save_results()

if __name__ == '__main__':
    main()
