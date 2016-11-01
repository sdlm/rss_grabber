#!/usr/bin/python
import feedparser
import os.path
import hashlib
import codecs
import re

TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
	return TAG_RE.sub('', text)


def get_lenta_rss():
	lenta = feedparser.parse('https://lenta.ru/rss')
	return [remove_tags(e['summary']) for e in lenta['entries'][:5]]


def get_dict_by_lines(lines):
	db = dict()
	for k, line in enumerate(lines):
		l = line.encode('utf-8', 'ignore')
		_hash = hashlib.md5(l).hexdigest()
		db[_hash] = line
		if k < 5:
			print('{}: {}'.format(_hash, l[:90]))
	return db


def write_to_file(file_name, lines):
	with codecs.open(file_name, 'w', 'utf-8') as fo:
		for e in lines:
			print(e)
			fo.write(e.encode('utf-8', 'ignore'))

def append_to_file(file_name, lines):
	with codecs.open(file_name, 'a', 'utf-8') as fo:
		for e in lines:
			fo.write(e.encode('utf-8', 'ignore') + u'\n')


def update_base(temp_file, base_file):
	if not os.path.isfile(temp_file):
		raise Exception()

	if os.path.isfile(base_file):

		data = []

		with codecs.open(temp_file, 'r', 'utf-8') as f:
			t_data = f.readlines()
			print(t_data)
			with codecs.open(base_file, 'r', 'utf-8') as fo:
				b_data = fo.readlines()

				t_dict = get_dict_by_lines(t_data)
				b_dict = get_dict_by_lines(b_data)
				hashes_t = set([k for k, v in t_dict.items()])
				hashes_b = set([k for k, v in b_dict.items()])
				hashes = hashes_t - hashes_b
				for h in hashes:
					if h in hashes_t:
						data.append(t_dict[h])

		append_to_file(base_file, data)

	else:
		write_to_file(base_file, get_lenta_rss())



if __name__ == '__main__':

	t_fname = './temp.txt'
	fname = './base.txt'

	write_to_file(t_fname, get_lenta_rss())

	update_base(t_fname, fname)
