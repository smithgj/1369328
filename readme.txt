Take the peoplesearch file and place it on the desktop.
Open up the folder and double-click peoplesearch.exe to run it.

I suggest running it as is, without changing the input.txt file, and see if the log and output files
match the approximate sizes of the ones included in the peoplesearch directory.

The first time you run it - it may not run correctly, and you will see a pop-up window
about Windows firewall. Select "allow" so peoplesearch.exe can access the internet. Once
that happens you can kill it, and then re-run it. Then make the comparison of the log andoutput files.


Once you know it is working you can change the input.txt file to search for peoplesearchyou are interested in.
To reduce the size of the log file you can change the line:
	level=DEBUG
to:
	level=INFO
	
The larger the number of values you add to the different search criteria (lines 29 - 40),
the larger number of different combinations that will be searched on. Currently it is capped
at running 50 different combos, that is determined by the line:
		max_browsers=50
		
The program will run in "headless" mode, which means you won't see any web browsers popping up.
This is controlled by the line:
	headless=yes
	
The maximum time for the web browser to wait for a page to return from peoplesearch.com
is currently set at 30 seconds. If you think your searches are timing out you can increase
this value. Decreasing it will not make the program run faster, as once the page is loaded
in the browser it will continue on, i.e. it won't wait the full 30 seconds to expire. This
timeout is controlled by the line:
	page_timeout=30
	
Greg Smith
smithgj66@hotmail.com

