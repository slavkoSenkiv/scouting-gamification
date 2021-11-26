import pprint

lis = [{'activity': 'гра',
  'score': -1,
  'scout': ' [1@gmail.com]',
  'time_stamp': '21.11.2021 22:12:00',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': 'гра',
  'score': 1,
  'scout': ' [2@gmail.com]',
  'time_stamp': '21.11.2021 22:12:00',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': 'гра',
  'score': 2,
  'scout': ' [3@gmail.com]',
  'time_stamp': '21.11.2021 22:12:00',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': 'гра',
  'score': '',
  'scout': ' [4@gmail.com]',
  'time_stamp': '21.11.2021 22:12:00',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': '',
  'score': 1,
  'scout': ' [1@gmail.com]',
  'time_stamp': '21.11.2021 22:13:06',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': '',
  'score': 2,
  'scout': ' [2@gmail.com]',
  'time_stamp': '21.11.2021 22:13:06',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': '',
  'score': 1,
  'scout': ' [3@gmail.com]',
  'time_stamp': '21.11.2021 22:13:06',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': '',
  'score': 2,
  'scout': ' [4@gmail.com]',
  'time_stamp': '21.11.2021 22:13:06',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': 'впоряд',
  'score': 2,
  'scout': ' [1@gmail.com]',
  'time_stamp': '21.11.2021 22:13:45',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': 'впоряд',
  'score': 2,
  'scout': ' [2@gmail.com]',
  'time_stamp': '21.11.2021 22:13:45',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': 'впоряд',
  'score': 2,
  'scout': ' [3@gmail.com]',
  'time_stamp': '21.11.2021 22:13:45',
  'who evaluate': 'slavko.senkiv@gmail.com.com'},
 {'activity': 'впоряд',
  'score': 2,
  'scout': ' [4@gmail.com]',
  'time_stamp': '21.11.2021 22:13:45',
  'who evaluate': 'slavko.senkiv@gmail.com.com'}]

log_summary = {}
print('log_summary', log_summary)
for log_row in lis:
    # print(log_row['scout'], log_row['score'])

    if log_row['scout'] not in log_summary.keys():
        if log_row['score'] == '':
            log_row['score'] = 0
        log_summary.setdefault(log_row['scout'], log_row['score'])
        continue  # in order to avoid next if for same scout

    if log_row['scout'] in log_summary.keys():
        if log_row['score'] == '':
            log_row['score'] = 0
        updated_score = log_summary[log_row['scout']] + log_row['score']
        log_summary[log_row['scout']] = updated_score

print(pprint.pformat(log_summary))
