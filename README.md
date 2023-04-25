# dailyhistoryposts - Facts
Hi there, I've been looking for a bunch of daily facts for a separate project, and other sources are eiother boring, or not quite as work friendly..

[dailyhistoryposts on tumblr](https://dailyhistoryposts.tumblr.com/) seems to hit my perfect balance of interesting but there's still one problem: they're a day behind me. So I would always be posting facts about yesterday.

To remedy this I'm just using the tumblr API to scrape all of their *"On This Day In History"* posts, and I can post last years fact.  
I'm sure its fine.

# Setup
1. Install python, I'm using 3.11.2
2. In your command prompt run `pip install -r Requirements.txt`
3. Mess around with my jupyter notebook with the scraping code,

# Results
I'm really happy with it! There were a few dates where the post format varied so I had to add some error checks to ignore them, and then manually add them back in later.  
Something I thought about after looking through the json response some more wasd using the `post["date]` value to get the date, but I thought the text might me more correct in case posts were a day late or something.  
See facts.json for all the facts posted up until today, 25/May/2023.