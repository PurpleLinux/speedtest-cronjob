# speedtest-cronjob

### Graphical summary:

![image](https://github.com/quetzelquot/speedtest-cronjob/assets/53280166/5bee204c-4763-4c7a-84fe-26d5eac43c07)


### What it is / the problem it solves

How fast is your internet? Your ISP says you have gigabit fiber, but do you really get 1Gb down all the time? Most of us know we get less than promised, but by how much? If you want to check this, you'll probably go to a website like speedtest.net and run a speedtest. But this is a snapshot, it only shows your speed in that instant. If you want speed data over time, you can get this in one of two ways:

#### Option 1: Manuallly with no code (booooooo lame)

1. Run the speed test:

![image](https://github.com/quetzelquot/speedtest-cronjob/assets/53280166/3badb151-8b80-4305-a8b0-626fc342751e)

2. Write down the data in a spreadsheet like a loser

![image](https://github.com/quetzelquot/speedtest-cronjob/assets/53280166/433fcea3-705d-4241-bfe8-a35959cbfa39)

#### Option 2: As Frank Sanatra suggested, do it my way (with code, automated)

Im assuming you have python3 installed and can can run pip3 install X on your own if needed.

1. Clone the repository

2. Install the speedtest CLI tool. Instructions can be found here:

https://www.speedtest.net/apps/cli

3. Automatically collect the data with a cronjobs:

Run `sudo crontab -e` then add the following to the bottom of the file under `# m h  dom mon dow   command` and save:

```
00	*	*	*	*	cd <path to where you cloned the repo>/speedtest-cronjob && bash main.sh
```

This is a bash script that will allow you to automated running speedtests as a cronjob every hour for each possible server and save the results to an incorrectly formatted json file. Don't worry, the python code will fix the formatting because it is easier to do that than mess with json data in bash. Don't handle json with bash. Just don't. From experience, I promise you, it's a bad idea.

4. Make a pretty graph:

Once your cronjob has been running a while and you've been collecting data every hour, in the command line in the `speedtest-cronjob` directory, run:

```
python3 chart_data.py
```

and it should make a pretty graph like this:

![image](https://github.com/quetzelquot/speedtest-cronjob/assets/53280166/2ed51322-71bf-4505-b2ff-2e7199efb53e)

Gigabit my butt. That's not even close. Time to call my ISP and find out that their terms of service include a clause that states they offers no guarantee of speed nor uptime, then switch to the other ISP in the area, and find out they're even worse.

Cheerio!
