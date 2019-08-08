from flask import Flask
import multiprocessing, signal

app = Flask(__name__)

def do_job(e):
	print('event started')
	i = 0
	while True:
		i = i + 1
		print('job ', i)

		if e.is_set():
			break

	# wait.....
	e.wait()

	print('event stopped')

event = multiprocessing.Event()

@app.route('/')
def index():
	return 'index page'

@app.route('/start')
def start():

	global event
	if event.is_set():
		event = event = multiprocessing.Event()

	job = multiprocessing.Process(name='job', target=do_job, args=(event,))
	if job.exitcode == signal.SIGTERM:
		job = multiprocessing.Process(name='job', target=do_job, args=(event,))
		job.start()

	job.start()
	return 'start job'

@app.route('/stop')
def stop():
	event.set()
	return 'stop job'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=True)
