# WebPuzac
A tool for webcrawling

*Current code info:*

The program is capable of looking at any url you give it and scraping all the links on that page. 
After that it gives you a choice on what link you want to scrape next or you can tell it to choose itself. 
For now that all it is capable of.


*Next update:*

Turning an auto mode into a safe fully autonomous mode.


*Very important stuff:*

This program is open source so you can use it as a platform for further modification
Be careful with webcrawling on social networks because if you do that, you are putting yourself in a position where you can be sued by owners of the social networks for scraping their data.
More on that here: https://benbernardblog.com/web-scraping-and-crawling-are-perfectly-legal-right/


*Before running a program:*

The program requies a pip install, to do that open command prompt and type: pip install bs4

BeautifulSoup (bs4) is a HTML parser used to convert website info to HTML
After you have installed what you need, you should go to the source code and change the value of the my_url variable to the url you want to scrape.


*How to run a program?*

The first thing program will ask you is if you want to run auto mode or no. 
If you say yes, the program will choose itself which link it will go to next. 
If you say no, the program will give you a list of links and you will choose which one is next. 
After you chose auto mode, you will have to insert a link that program will start scraping from, when you write the link you must write it whole (so you should write https://www.google.com instead of just www.google.com or https://google.com), if you don't program will run into errors and wont output any result.


*Switching between modes*

You can switch between auto and manual mode. 
When a program asks you if you want to proceed you have to tell it 'no' and it will ask if you want to switch to the other mode, if you say yes it will show you the same list again and ask you to proceed, and if you say no it will end the program. 


*Unexpected errors*

A program can suddenly halt and report an error, that is most likely due to the fact that some websites are locked and when you try to access those certain websites it will report an error, you can see more details on the error in the last line the program will output


Thats all for now folks, enjoy
