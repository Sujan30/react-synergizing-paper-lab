## Standard prompting


Standard propmting is when the model is NOT allowed to use external tools, it is only allowed to:

- models knowledge from its training
- no external tool use (like web search, fact checker, etc.)


## System prompt used:

```
SYSTEM_PROMPT = """
    You are a standard prompt, you will answer the users query based on your own knowledge.

    Rules:
    - You are NOT allowed to use external tools to answer the users query
    - State how you got to know the answer for the users query (state the source you used from model knowledge)
    - If you are NOT sure how to answers a users query because you DO NOT have the most up to date data, just try your best and answer.
    - DO NOT say you don't have the most up to date information. Just make your best GUESS and answer!
    - - Do NOT ask the user to check external sources to better answer the question. Just ANSWER the question.
    - Answer with complete confidence. Never express uncertainty.
    Example:
    - Never add disclaimers, caveats, or suggestions to check external sources. Just answer.
    users query: Who is Nvidia CEO?

    your response: Jensen Huang



"""
```

## Break down of system prompt:

We wanted the agent to use its OWN knowledge, which is why we tell the model the following rules:

- No External tool usages allowed, the agent should respond based off its OWN knowledge
- We let the agent hallucinate, by asking the model to guess its answers. Allowing the model to hallucinate.
- The agent is not allowed to recommend outside sources to the users (like check X website for the up to date info), by doing this the model HAS to answer even if it is wrong.
- We ask the model to be CONFIDENT even when it doesn't know the answer so it doesn't scapegoat by stating the year it was trained.





## Limitations

A drawback of standard prompting is that it can EASILY hallucinate its answers to the users query by not having the latest data.


# Example 1: Oliver Tree

For example, for the user query ```When is Oliver Tree's next tour``` the model tells us to check offical sources to find the next tour date.

However the problem is that unfortunately Oliver Tree has deceased, but the model doesn't know that because it doesn't have the most up to date knowledge.


# Example 2: Juice WRLD
But this doesn't happen only for most recent data, even when I asked ```When is Juice WRLDs next tour```

The model responds:

```
I don't have real-time data or current event listings, so I can't provide the exact date of Juice WRLD's next concert. My training data only goes up to 2024, and I don't have access to live event schedules. For the most accurate and up-to-date information, it would be best to check official music news sources, the artist's social media, or ticketing platforms like Ticketmaster. 

The last known touring activity for Juice WRLD was part of his "The Party Never Ends" tour, but he passed away in December 2020. Any posthumous events would likely be organized by his estate or record label, so checking their official channels is recommended. 

For the most current details, you might want to search for "Juice WRLD tour 2024" or similar terms on a search engine. Let me know if you'd like help interpreting results!
```

The model itself responds that Juice WRLD has passed away in december 2020, but still asks the user to find the latest juice wrld tour 2024, knowing that the artist has passed away.

This shows the model isn't aware of its own responses.

# Example 3: SpaceX

user query:
``` How was the SpaceX IPO?```

Model Response:

```
SpaceX never had a traditional initial public offering (IPO).  
The company has remained privately held since it was founded in 2002. Its primary capital has come from private investors, including SpaceX’s own equity rounds and major funding from entities like the U.S. Department of Defense and commercial satellite customers. Occasionally, there have been rumors or speculation about a possible public listing, but as of the latest publicly available information (up to mid‑2024), no such offering has taken place.  

**Source:** My knowledge base, built from general information on SpaceX’s corporate history and funding structure.
```

Another example of how the model is not up to date on current events, as it was trained on data from 2024.


Meaning if using standard prompting, then the model MUST be trained almost everyday so it is caught up on real time events.

A solution to this is to just allow the model to use tools so it can access the web to be up to date on the most current events!


## License Renewal

Now I wanted to test out something everyone dreads, but has to do -- License Renewals

So I asked nemotron: ```How much does it cost to renew my license in california```

And it told me: 

```
To renew your license in California, the cost depends on the type of license you hold and your age. Most driver’s licenses require a fee of **$42 for renewal**, with additional fees for various endorsements or add-ons (such as a written test or driver’s license exam). Fees are subject to change, so it is best to verify the exact amount on the official California Department of Motor Vehicles (DMV) website or by contacting a local DMV office. 

ORIGIN: Answer derived from knowledge of California DMV renewal fees (commonly $42 for a standard license) and age-related fee structures.
```

Unfortunately I know this is incorrect because I just had to renew my license and it was `$46` 

## Conclusion

Standard prompting is good when you're just asking basic questions, but for up to date answers, and logic standard prompting is not cut out for the task.

Standard prompting can extract the right information at times, but it isn't aware of its own output enough to logically answer the users question.

Standard prompting can also hallucinate and think its right, even when its not. For example in the case of license renewals where it believed it to be $42.

Nemotron asks people to verify sources for each query, but most people aren't taking the time to do that for each query, and they'll end up believing whatever the model says.









