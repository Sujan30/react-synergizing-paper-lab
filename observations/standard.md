## Standard prompting


Standard propmting is when the model is NOT allowed to use external tools, it is only allowed to:

- models knowledge from its training
- no external tool use (like web search, fact checker, etc.)


A drawback of standard prompting is that it can EASILY hallucinate its answers to the users query by not having the latest data.

For example, for the user query ```When is Oliver Tree's next tour``` the model tells us to check offical sources to find the next tour date.

However the problem is that unfortunately Oliver Tree has deceased, but the model doesn't know that because it doesn't have the most up to date knowledge.


But this doesn't happen only for most recent data, even when I asked ```When is Juice WRLDs next concert```

The model responds:

```
I don't have real-time data or current event listings, so I can't provide the exact date of Juice WRLD's next concert. My training data only goes up to 2024, and I don't have access to live event schedules. For the most accurate and up-to-date information, it would be best to check official music news sources, the artist's social media, or ticketing platforms like Ticketmaster. 

The last known touring activity for Juice WRLD was part of his "The Party Never Ends" tour, but he passed away in December 2020. Any posthumous events would likely be organized by his estate or record label, so checking their official channels is recommended. 

For the most current details, you might want to search for "Juice WRLD tour 2024" or similar terms on a search engine. Let me know if you'd like help interpreting results!
```

The model itself responds that Juice WRLD has passed away in december 2020, but still asks the user to find the latest juice wrld tour 2024, knowing that the artist has passed away.

This shows the model isn't aware of its own responses.


