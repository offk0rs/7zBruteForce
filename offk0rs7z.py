import subprocess
import sys
import threading

passwordsChecked = 0
passwords = []
count = 0
founded = False

class myThread (threading.Thread):
	def __init__(self, id, fromLine, toLine, fileName):
		threading.Thread.__init__(self)
		self.id = id
		self.fromLine = int(fromLine)
		self.toLine = int(toLine)
		self.fileName = fileName
	def run(self):
		global passwords
		global founded
		for password in range(self.fromLine,self.toLine):
			if founded == False:
				stdout = subprocess.call(
					"7z t -p'{0}' {1}".format(passwords[password].rstrip('\r\n'), self.fileName), 
					stderr=subprocess.DEVNULL, 
					stdout=subprocess.DEVNULL, 
					shell=True
				)
				if stdout == 0:
					print("Password found ::{0}::".format(passwords[password].rstrip('\r\n')))
					founded = True
					return
				if (password % 100) == 0 and password > 0:
					threadLock.acquire()
					print_progress(self.id, password - self.fromLine)
					threadLock.release()
			else:
				return

def print_progress(threadID, currentPasswords):
	global passwordsChecked
	global count
	passwordsChecked += 100
	print("{0}/{1}(orientative, not exactly) passwords checked; i'm thread: {2}".format(str(passwordsChecked),str(count),str(threadID)))


threadLock = threading.Lock()


def main():
	archive = sys.argv[1]
	dictionary = sys.argv[2]
	threads = int(sys.argv[3])
	global passwords
	global count

	f = open(dictionary,encoding='latin-1')
	print("Loading dictionary, please wait...")
	for line in f:
		passwords.append(line)

	print("Passwords loaded\nCalculating nr of passwords per thread")

	with open(dictionary,encoding='latin-1') as f:
		count = len(f.read().split('\n')) - 1

	print("Done, lets start party;)")

	for threadID in range(0, threads):
		thread = myThread(threadID, threadID*(count/threads), (threadID*(count/threads)) + (count/threads),archive)
		thread.start()
		
if __name__ == "__main__":
	if len(sys.argv) == 4:
		main()
	else:
		print(" Missing args\n Example: python3 ./offk0rs7z.py zip wordlist numThreads \n Example: python3 ./offk0rs7z.py ./test.7z ../rockyou.txt 5")
