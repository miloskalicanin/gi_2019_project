import subprocess
import sys

if sys.version_info[:2] < (3, 0):
    code = subprocess.call(['python3'] + sys.argv)
    raise SystemExit(code)

import matplotlib.pyplot as plt
import os
from utils import get_alphabet
from Heuristics.good_suffix import GoodSuffix
from Heuristics.bad_character import BadCharacter
from Heuristics.last_character import LastCharacter
from Heuristics.next_to_last_character import NextToLastCharacter
from Heuristics.bmhs2 import HorspoolSunday2
import boyer_moore as bm
import timeit
import tracemalloc
from termcolor import colored
import datetime

heuristics = [[LastCharacter(), HorspoolSunday2()], [LastCharacter()], [HorspoolSunday2()],
              [GoodSuffix(), BadCharacter()]]

colors = ["r", "b", "g", "y"]
index = 0
test_directory = "./test"


def get_heuristics_name(heurisitcs):
    ret = [heuristic.get_name() for heuristic in heurisitcs]
    ret = '+'.join(ret)
    return ret


def get_number_of_patterns():
    ret = 0
    dirpath = os.path.abspath(test_directory)
    all_files = (os.path.join(basedir, filename) for basedir, dirs, files in os.walk(dirpath) for filename in files)
    for filepath in all_files:
        with open(filepath) as f:
            text = f.readlines()
            patterns_text = text[0]
            patterns = patterns_text.split(",")
            ret = ret + len(patterns)
            f.seek(0)
            f.close()
    return ret


positions = list(range(get_number_of_patterns()))

dirpath = os.path.abspath(test_directory)
all_files = (os.path.join(basedir, filename) for basedir, dirs, files in os.walk(dirpath) for filename in files)
sorted_files = sorted(all_files, key=os.path.getsize)

memory_in_bytes_all = []
time_in_s_all = []
positions_all = []
test_names = []

plt.rcParams['xtick.labelsize'] = 7
f1 = plt.figure(1)

for algorithm in heuristics:
    time_in_s = []
    memory_in_bytes = []
    bm.set_heuristics(heuristics[index])
    for filepath in sorted_files:
        with open(filepath) as f:
            text = f.readlines()
            text = [line.rstrip("\n\r") for line in text]
            patternsText = text[0]
            patterns = patternsText.split(",")
            text = ''.join(text[1:])
            f.close()

        for pattern in patterns:
            print("Executing " + colored(get_heuristics_name(heuristics[index]), 'red')
                  + " on file " + colored(os.path.basename(filepath), 'red')
                  + " with pattern " + colored(pattern, 'red') + ". Timestamp: "
                  + colored(datetime.datetime.now().time(), "red"))

            test_name = "File: " + os.path.basename(filepath) + "\nPattern: " + pattern
            test_names.append(test_name)

            tracemalloc.start()
            bm.preprocess(pattern, get_alphabet(text))
            memory_in_bytes.append(round(tracemalloc.get_tracemalloc_memory(), 2))
            tracemalloc.stop()

            time = min(timeit.repeat('boyer_moore(text)', number=1, repeat=5,
                                     setup='from boyer_moore import boyer_moore; text=\"' + text + "\""))
            time_in_s.append(round(time, 2))

    print("\r")
    time_in_s_all.append(time_in_s[:])
    memory_in_bytes_all.append(memory_in_bytes[:])
    positions_all.append(positions[:])
    plt.bar(positions[:], time_in_s[:], width=0.1, color=colors[index])
    positions = [x + 0.1 for x in positions]
    index = index + 1

middle_position = list(range(get_number_of_patterns()))
middle_position = [x + 0.15 for x in middle_position]
plt.xticks(middle_position, test_names)
plt.gca().legend(('Boyer Moore - Horspool and Horspool Sunday 2',
                  'Boyer Moore - Horspool',
                  'Boyer Moore - Horspool Sunday 2',
                  'Boyer Moore - Bad character and Good suffix'))

plt.title("Time benchmark")
plt.xlabel('Test files')
plt.ylabel('Time(s)')

f2 = plt.figure(2)
index = 0
for memoryList in memory_in_bytes_all:
    plt.bar(positions_all[index], memory_in_bytes_all[index], width=0.1, color=colors[index])
    index = index + 1

plt.xticks(middle_position, test_names)
plt.gca().legend(('Boyer Moore - Horspool and Horspool Sunday 2',
                  'Boyer Moore - Horspool',
                  'Boyer Moore - Horspool Sunday 2',
                  'Boyer Moore - Bad character and Good suffix'))
plt.title("Memory benchmark")
plt.xlabel('Test files')
plt.ylabel('Memory(B)')

plt.show()

fig, ax = plt.subplots()

# hide axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
plt.title("Time benchmark")

table = plt.table(cellText=time_in_s_all,
                  colWidths=[0.07 for x in test_names],
                  rowColours=colors,
                  colLabels=test_names,
                  loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.5, 1.5)

cellDict = table.get_celld()
for x in range(1, len(colors) + 1):
    cellDict[(x, -1)].set_width(0.05)
    cellDict[(x, -1)]._loc = 'right'

for cell in table._cells:
    if cell[0] == 0:
        table._cells[cell].set_fontsize(8)

fig.tight_layout()

fig, ax = plt.subplots()

# hide axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
plt.title("Memory benchmark")

table = plt.table(cellText=memory_in_bytes_all,
                  colWidths=[0.07 for x in test_names],
                  rowColours=colors,
                  colLabels=test_names,
                  loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.5, 1.5)

cellDict = table.get_celld()
for x in range(1, len(colors) + 1):
    cellDict[(x, -1)].set_width(0.05)
    cellDict[(x, -1)]._loc = 'right'

for cell in table._cells:
    if cell[0] == 0:
        table._cells[cell].set_fontsize(8)

fig.tight_layout()

plt.show()
