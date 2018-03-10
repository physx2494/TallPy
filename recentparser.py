import requests, re, time
from bs4 import BeautifulSoup
def get_recent():
	result = requests.get("http://rpforumbleach.proboards.com/threads/recent/")
	soup = BeautifulSoup(result.content, 'html.parser')
	recent_threads = []
	for link in soup.find_all('a'):
		href = link.get('href')
		try:
			r = re.search("thread/\d+", href).group()
			r = re.search("\d+", r)
			r = int(r.group())
			if r not in recent_threads:
				recent_threads.append(r)
		except AttributeError:
			continue
		except TypeError:
			continue
			#print('TypeError: {}'.format(href))
	recent_threads.remove(9656)
	recent_threads.remove(6283)
	recent_threads.remove(9475)
	return(recent_threads)

def save_list(_list):
	with open('recent thread list.txt', "w") as outfile:
		for thread in _list:
			outfile.write(str(thread))
			outfile.write("\n")
		outfile.close()

def read_list():
	_list = []
	with open('recent thread list.txt', "r") as infile:
		for line in infile:
			r = re.search("\d+", line).group()
			_list.append(int(r))
		infile.close()
	return(_list)

def convert_to_url(num):
	url = 'https://rpforumbleach.proboards.com/thread/{}'.format(num)
	return(url)

def check_if_updated(old_list, new_list):
	updated = []
	for thread in new_list:
		try:
			if new_list.index(thread) < old_list.index(thread):
				updated.append(thread)
		except ValueError:
			print('ValueError when checking thread lists {}'.format(thread))
			updated.append(thread)
	return(updated)

def main_loop():
	read_thread_list = read_list()
	thread_list = get_recent()
	save_list(thread_list)
	#print(thread_list == read_thread_list)
	updated_list = check_if_updated(read_thread_list, thread_list)
	return(updated_list)
'''
def main_loop():
	try:
		len(old_list)
	except:
		old_list = read_list()
	new_list = get_recent()
	updated_list = check_if_updated(old_list, new_list)
	print(old_list == new_list)
	print(updated_list)
	old_list = new_list
	return(updated_list)'''


if __name__ == "__main__":
	main_loop()


