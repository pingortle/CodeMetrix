#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from os.path import join, getsize, splitext

fileExts = [
    '.cs',
    '.xaml',
    '.png',
    '.bmp',
    '.txt',
    '.spritefont',
    '.wmv',
    '.fbx',
    '.x',
    '.dds',
    '.nsi',
    '.iss',
    '.jpg',
    '.py',
    ]
ignoredFolders = ['.git', 'packages', 'bin', 'obj']

def printDirInfo(root):
    fileExtensionCounts = {}
    byteSum = 0

    for (path, dirs, files) in os.walk(root):
        for name, ext in filter(\
            lambda x: x[1].lower() in fileExts,\
            map(lambda y: splitext(y), files)):
            key = ext.lower()
            try:
                fileExtensionCounts[key] += 1
            except KeyError:
                fileExtensionCounts[key] = 1
            byteSum += getsize(join(path, name + ext))
        for d in ignoredFolders:
            if d in dirs:
                dirs.remove(d)

    for key in sorted(fileExtensionCounts.keys()):
        print key, ' = ', str(fileExtensionCounts[key])

    print 'Total # of files: ', str(sum(fileExtensionCounts.values()))

    print
    print 'Total relevant file size:', dataUnitsFromBytes(byteSum)

def dataUnitsFromBytes(numberOfBytes):
    abbreviations = [
        'B',
        'KB',
        'MB',
        'GB',
        'TB',
        'PB',
        'EB',
        'ZB',
        'YB',
        'Insane Bytes!',
        ]

    displayedSize = float(numberOfBytes)
    for abbrev in abbreviations:
        if displayedSize / 1000 < 1:
            return str(displayedSize) + ' ' + abbrev
            break
        else:
            displayedSize /= 1000
    else:
        return 'This is just way too big.'

if __name__ == '__main__':
    from sys import argv
    if argv.count > 1:
        map(printDirInfo, argv[1:])
    else:
        printDirInfo(os.getcwd())
        print os.getcwd()
