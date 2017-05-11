from functools import reduce
import sys
import git
import glob
from astropy.table import Table
from tqdm import tqdm
import matplotlib.pyplot as plt

def analyse_file(filename, repo):

    commits = repo.iter_commits(paths=filename)

    allcommits = [c for c in commits]
    if len(allcommits) == 0:
        return None
    authors = set()
    for commit in allcommits:
        authors.add(commit.author.name)
        if len(authors) > 1:
            return None
    commits_number = len(allcommits)
    return [str(authors.pop()), commits_number, "{:%Y-%m-%d}".format(allcommits[0].authored_datetime)]

def piechart(total, unique):
    labels = ['ok', 'no ok']
    fig1, ax1 = plt.subplots()
    ax1.pie([total, unique], labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def main():
    files = reduce(lambda l1, l2: l1 + l2, [glob.glob(sys.argv[1] + "/**/*." + e, recursive=True) for e in ['py', 'f', 'c', 'h', 'pyx']])
    t = Table([[], [], [], []],
              names=('filename', 'author', 'commits', 'last date'),
              dtype=('S100','S100', 'i4', 'S10' ))
    t.convert_bytestring_to_unicode()
    for file_i in tqdm(files):
        row = analyse_file(file_i, git.Repo())
        if row:
            t.add_row([file_i] + row)

    t.sort(['last date','filename'])
    t.write('{}_critic.txt'.format(sys.argv[1]), format='ascii.fixed_width', overwrite=True)
    piechart(len(files), len(t))

# What else I want to do?
## DONE:sort table by date
## Find last commit from these critic authors (are they still contributing?)
## DONE: Plot pie chart with files vs unique // also in lines of code?
## Plot user ranking vs files (lines of code)

