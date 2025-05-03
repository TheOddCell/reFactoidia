# reFactoidia
"AI is this what when mode off."

A rewrite of [factoidia](https://github.com/TheOddCell/factoidia).
## Word salad made of quotes, jokes, facts, and excuses pulled from APIs.
Connects to the following APIs to get such strings (that are mashed together):
1. `https://uselessfacts.jsph.pl/api/v2/facts/random` - Useless Facts
2. `https://techy-api.vercel.app/api/text` - Techy Phrases
3. `https://api.chucknorris.io/jokes/random` - Chuck Norris Jokes
4. `https://excuser-three.vercel.app/v1/excuse` - Excuses
5. `https://meowfacts.herokuapp.com/` - Cat Facts
6. `https://api.kanye.rest/` - Kanye West quotes
7. All of them mashed together
Easly expanable.

Requires:
1. `requests` package
2. `ttkbootstrap` package
3. `google-genai` package and api key in api.txt (required unlike [factoidia](https://github.com/TheOddCell/factoidia))

## Adding new APIs
The APIs are stored in a list at line 26 in the following format:
```
apis=[# URL                                               Type and keyword      Button label
    ["https://uselessfacts.jsph.pl/api/v2/facts/random",  1,"text",     "Create new fact"          ],
    ["https://techy-api.vercel.app/api/text",             0,"",         "Modulate the tech"        ], 
    ["https://api.chucknorris.io/jokes/random",           1,"value",    "Talk to Chuck Norris"     ],
    ["https://excuser-three.vercel.app/v1/excuse",        2,"0-excuse", "Excuse yourself"          ],
    ["https://meowfacts.herokuapp.com/",                  3,"data-0",   "Create a cat fact"        ],
    ["https://api.kanye.rest/",                           1,"quote",    "Create a Kanye West quote"],
    ["",                                                  4,"",         "Everything"               ]
    ]
```

### URL
ez, just put in the URL. Must be GET request.
### TYPE and KEYWORD
There are 5 types:
#### Main Type
##### Type 0
Take it in raw.

`requests.get(url).text`

Example: `["https://techy-api.vercel.app/api/text",             0,"",         "Modulate the tech"        ],`
#### JSON types
##### Type 1
Take it from JSON
Set keyword to the name of the string inside the JSON

`json.loads(requests.get(url).text)[keyword]`.

Example: `["https://uselessfacts.jsph.pl/api/v2/facts/random",  1,"text",     "Create new fact"          ],`
##### Type 2
Take it from JSON, with 2 layers, int in front.
Set keyword to the int and string, seperated by dashes.

`json.loads(requests.get(url).text)[keyword.split("-")[0]][int(keyword.split("-")[1])]`

Example: `["https://excuser-three.vercel.app/v1/excuse",        2,"0-excuse", "Excuse yourself"          ],`

##### Type 3
Take it from JSON, with 2 layers, string in front.
Set keyword to the string and int, seperated by dashes.

`json.loads(requests.get(url).text)[keyword.split("-")[0]][int(keyword.split("-")[1])]`

Example: `["https://meowfacts.herokuapp.com/",                  3,"data-0",   "Create a cat fact"        ],`

#### Internal
##### Type 4
All other APIs used together. Must be used at end of list else infinite recursion may happen.

`grabfact(i)`

Example: `["",                                                  4,"",         "Everything"               ]`

### Button label
A string. Duh.
