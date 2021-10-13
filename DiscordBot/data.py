data = {
    "botInfo" : {
        "Version" : "v1.00.00",
        "Name" : "FalTracker",
        "Description" : "Bot to help Falmouth Uni Students find out quick information about uni services",
        "Author" : "Tom Chambers, @OffDutySquirrel#3467",
        "Python Version" : "Python 3.10.0"
    },
    "keys" : {
        "token" : "ODk3MTk4MDg3NDE0NjIwMTcy.YWSK1Q.1JUA2_tjXY2-bPp7yGT0bsK29sg",
        "Applicatoin ID" : "897198087414620172",
        "Public Key" : "930a7810e8a7c75155438cf0d54276b9de7d8cc8bf32263c11ee2363dba65fe1",
        "Client ID" : "897198087414620172"
    },
    "webInfo" : {
        "falmouthServiceURL" : "https://fxplus.ac.uk/service-status/",
        "tableCol" : "tablepress-2"
    }
}

archivedData = {
    "falmouthURLs" : {    
    # Im going to keep these os if service status every break, i have these to come back too, 
    # maybe I could add in checks to make sure it works, and if not use these, but hold shit 
    # that sounds like so much fucking effor
    "SportsFacilities" : {
        "SportsFacilities" : "https://fxplus.ac.uk/facilities-shops/sports-facilities/",
        "FitnessCentre" : "https://fitnesscentre.fxplus.ac.uk/"
    },
    "TheStannary" : {
        "StannaryBar" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/the-stannary-bar/",
        "StannaryKitchen" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/the-lower-stannary-restaurant/"
    },
    "cafe" : {
        "AMATA" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/amata-cafe/",
        "ESI" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/esi-cafe/",
        "Koofi" : "https://fxplus.ac.uk/facilities-shops/food-drink/penryn/koofi/",
        "Sustainability" : "https://fxplus.ac.uk/facilities-shops/catering/penryn/the-sustainability-cafe/",               
        "Fox" : "https://fxplus.ac.uk/facilities-shops/food-drink/falmouth/fox-cafe/"
    },
    #Holy fucking shit why didnt i know this existed
    #now i need to refactor everything and just use this one link, fuck me
    "ServiceStatus" : "https://fxplus.ac.uk/service-status/"
}
}