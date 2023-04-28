import json
import re

import pytumblr
from dotenv import dotenv_values


def _getClient():
    config = dotenv_values(".env")
    client = pytumblr.TumblrRestClient(
        config["consumer_key"],
        config["consumer_secret"],
        config["oauth_token"],
        config["oauth_secret"],
    )
    return client


def _getFactsFromPage(client, offset):
    blogName = "dailyhistoryposts"
    posts = client.posts(
        blogName, limit=50, offset=offset
    )  # max 50ish at a time. Need to use offset...
    facts = _extractPostsFacts(posts)
    return facts


def _extractPostsFacts(posts):
    headPattern = re.compile(r"(<h1>[^<]*</h1>)")
    tagsPattern = re.compile(r"(\<[^\>]*\>)")
    datePattern = re.compile(r"[A-Za-z]+\s\d{1,2}")
    facts = {}
    count = 0
    for post in posts["posts"]:
        count += 1
        if post["summary"] == "On This Day In History":
            textRaw = post["body"]
            # Reply posts start with <p>. <h1> seems to be new posts.
            if (textRaw[:4] == "<h1>"):
                textWoHeading = re.sub(headPattern, "", textRaw)
                text = re.sub(tagsPattern, "", textWoHeading)
                dateMatch = re.findall(datePattern, text)
                if dateMatch:
                    date = dateMatch[0]
                    existingFacts = facts.get(date, [])
                    if not text in existingFacts:
                        existingFacts.append(text)
                        facts[date] = existingFacts
                else:
                    # On 29/June they forgot to add 'June' to the post, so it falls over.
                    pass
    return facts


def _loadExistingFacts():
    with open("facts.json", "r") as f:
        return json.load(f)


def getFacts():
    facts = _loadExistingFacts()
    client = _getClient()
    offset = 0
    existingFactsFound = False
    while not existingFactsFound:
        pageFacts = _getFactsFromPage(client, offset)
        for date in list(pageFacts.keys()):
            for fact in pageFacts[date]:
                if not fact in facts[date]:
                    facts[date].append(fact)
                else:
                    existingFactsFound = True
        offset += 50
        pass
    # Save the facts
    with open("facts.json", "w") as f:
        json.dump(facts, f, indent=4)
    return facts


if __name__ == "__main__":
    getFacts()
