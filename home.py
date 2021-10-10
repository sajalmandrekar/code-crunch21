output = {
    "Title":"REST API",
    "Developed by":("Sajal Mandrekar","Sai Sameer Kumar Lolla"),
    "Base URL": "https://coderspp.herokuapp.com/",
    "Documentation":"https://coderspp.herokuapp.com//docs",
    "Modules:":[
        {
            "name":"NASA",
            "Authentication":"API key",
            "endpoints":[
                {"type":"GET","url":"/nasa/image-of-month","params":[]},
                {"type":"GET","url":"/nasa/images-of-month/{year},{month}","params":[]},
                {"type":"GET","url":"/nasa/videos-of-month/{year},{month}","params":[]},
                {"type":"GET","url":"/nasa/earth-poly-image/{YYYY-MM-DD}","params":[]},
            ],
        },
        {
            "name":"Weather API",
            "Authentication":"OPENWEATHER API key",
            "endpoints":[
                {"type":"GET","url":"/weather/city/{city_name}"},
                {"type":"GET","url":"/weather/search","params":[("latitude","longitude"),"pin_code"]},
            ],
        },
        {
            "name":"Twitter",
            "Authentication":"BEARER_TOKEN",
            "endpoints":[
                {"type":"GET","url":"/twitter/user/{username}","params":[]},
                {"type":"GET","url":"/twitter/hashtag/{hashtag}","params":[]},
                {"type":"GET","url":"/twitter/location","params":["latitude","longitude","radius"]},
            ],
        },
        {
            "name":"Crypto",
            "Authentication":None,
            "endpoints":[
                {"type":"GET","url":"/crypto/coins","params":[]},
                {"type":"GET","url":"/crypto/tokens","params":[]},
                {"type":"GET","url":"/crypto/quote/{name}","params":[]},
                {"type":"GET","url":" /crypto/team/{name}","params":[]},
            ],
        },
        {
            "name":"GitHub",
            "Authentication":None,
            "endpoints":[
                {"type":"GET","url":"/github/user/{username}","params":[]},
                {"type":"GET","url":"/github/repo/{min_stars},{max_stars}","params":[]},
                {"type":"GET","url":"/github/issues/{author}/{repo}/{labels}","params":[]},
                {"type":"GET","url":" /github/commits/{start_date},{end_dates}/{repo}","params":[]},
            ],
        }
    ],
}