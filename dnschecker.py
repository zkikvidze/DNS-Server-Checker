import multiprocessing, subprocess, datetime, os, time, signal

DNSSERVERS='TEXT_FILE_LOCATION'

list1 = open('upservers.txt', 'w')
list2 = open('downservers.txt', 'w')

def timeout_command(command, timeout):
    start = datetime.datetime.now()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
      time.sleep(0.1)
      now = datetime.datetime.now()
      if (now - start).seconds> timeout:
        os.kill(process.pid, signal.SIGKILL)
       # os.waitpid(-1, os.WNOHANG)
        return None
    return process.stdout.read()



def worker(ip):
    
    ip = "@" + ip
    if timeout_command(["dig", ip, "version.bind", "txt", "chaos", "+short"], 2): 
        list1.write(ip.lstrip('@'))
        list1.close()
        exit(1)
    else:
        list2.write(ip.lstrip('@'))
        list2.close()
        exit(0)



if __name__ == '__main__':
    jobs = []
    with open(DNSSERVERS) as f:
        for l in f:
            p = multiprocessing.Process(target=worker, args=(l,))
            jobs.append(p)
            p.start()
            
    result = []
    for proc in jobs:
        proc.join()
        result.append(proc.exitcode)
    print "Servers UP:" + str(result.count(1))
    print "Servers Down:" + str(result.count(0))


