# DNS-Server-Checker
Python Script that checks high number of DNS servers simultaneously, whether they are live or not

Script uses linux dig command to send 'version.bind txt chaos' query to servers, if there is answer (empty also qualifies), script returns address as live, and if there is timeout, this means that server is down.
It writes all results in upservers.txt and downservers.txt files.

Script uses multiprocessing module to speed up processing. For example, it can query 45000 DNS servers in 4 minutes, on i7 processor with 30MB bandwidth.
