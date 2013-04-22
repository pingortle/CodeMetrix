#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import walk, getcwd
from os.path import join, getsize, splitext
from fileinput import input

dataExts = [
    '.png',
    '.bmp',
    '.txt',
    '.spritefont',
    '.wmv',
    '.fbx',
    '.x',
    '.dds',
    '.jpg',
    '.csproj',
    '.contentproj',
    '.dll',
    '.ico',
    '.xml',
    ]
codeExts = [
    '.cs',
    '.xaml',
    '.nsi',
    '.iss',
    '.py',
]
ignoredFolders =  ['.git', 'packages', 'bin', 'obj']

def printDirInfo(root):
    fileExts = dataExts + codeExts
    fileExtensionCounts = {}
    byteSum = 0
    lineSum = 0

    for (path, dirs, files) in walk(root):
        for name, ext in filter(\
            lambda x: x[1].lower() in fileExts,\
            map(lambda y: splitext(y), files)):
            key = ext.lower()
            try:
                fileExtensionCounts[key] += 1
            except KeyError:
                fileExtensionCounts[key] = 1
            byteSum += getsize(join(path, name + ext))
            if key in codeExts:
                lineSum += sum(1 for line in open(join(path, name + ext)))
        for d in ignoredFolders:
            if d in dirs:
                dirs.remove(d)

    print 'Data files:'
    for key in sorted(set(fileExtensionCounts.keys()) & set(dataExts)):
        print key, ' = ', str(fileExtensionCounts[key])

    print
    print 'Code files:'
    for key in sorted(set(fileExtensionCounts.keys()) & set(codeExts)):
        print key, ' = ', str(fileExtensionCounts[key])

    print
    print 'Total # of files: ', str(sum(fileExtensionCounts.values()))
    print 'Total # of lines: ', lineSum

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
        printDirInfo(getcwd())
        print getcwd()
