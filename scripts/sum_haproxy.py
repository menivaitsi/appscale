#!/usr/bin/python2

""" Present an overview of HAProxy stats for a given application over time. """

import argparse
import csv
import logging
import sys

CURRENT_QUEUE_INDEX = 2
MAX_QUEUE_INDEX = 3
CURRENT_SESSIONS_INDEX = 4
MAX_SESSIONS_INDEX = 5
SESSIONS_RATE_INDEX = 33

def print_sum_line(stats):
  print '\t'.join(str(item) if item!=0 else '-' for item in stats)

def summarize(args):
  print '\t'.join(['#AppServers', 'Q CUR', 'Q MAX', 'CUR Session', 'MAX Sessions'])

  num_appservers = 0
  total_qcur = 0
  total_qmax = 0
  total_scur = 0
  total_smax = 0

  # New Session Rate as given by HAProxy
  srate = 0

  # Persist global maxima between HAProxy reloads   
  prev_qmax = 0
  prev_smax = 0

  with open(args.ha_file, 'rb') as ha:
    ha_reader = csv.reader(ha, delimiter=',')
    for row in ha_reader:
      if args.appid not in row[0] or row[1] == 'FRONTEND':
        num_appservers = 0
        total_qcur = 0
        total_qmax = 0
        total_scur = 0
        total_smax = 0
        continue

      if row[1] == 'BACKEND':
        total_qcur = int(row[CURRENT_QUEUE_INDEX])
        total_qmax = int(row[MAX_QUEUE_INDEX])
        total_smax = int(row[MAX_SESSIONS_INDEX])
        total_scur = int(row[CURRENT_SESSIONS_INDEX])

        if prev_qmax > total_qmax:
          total_qmax = prev_qmax
        else:
          prev_qmax = total_qmax

        if prev_smax > total_smax:
          total_smax = prev_smax
        else:
          prev_smax = total_smax
 
        print_sum_line(
          [num_appservers, total_qcur, total_qmax, total_scur, total_smax])

        continue

      num_appservers += 1


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--app_id', '-a', 
    dest='appid',
    required=True,
    help='The application ID to summarize stats for')
  parser.add_argument('--ha_file', 
    dest='ha_file',
    required=True,
    help='The path to the HAProxy stats file')

  args = parser.parse_args()
  summarize(args)

if __name__ == '__main__':
  main()
