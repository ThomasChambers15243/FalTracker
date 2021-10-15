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
    },
    "sName" : {
    "Falmouth Campus Shop" : "Shop",
    "Penryn Campus Shop" : "Shop",
    "AV" : "Service",
    "Little Wonders Nurseries" : "Service",
    "Multi Use Games Area" : "Service",
    "Penryn Campus Gym" : "Service",
    "Penryn Sports Centre" : "Service",
    "The Compass" : "Service",
    "Falmouth Campus Library" : "Library",
    "Falmouth Campus Library Helpdesk" : "Library",
    "Penryn Campus Library" : "Library",
    "Penryn Campus Library Helpdesk" : "Library",
    "Virtual Helpdesk" : "Library",
    "AMATA Cafe" : "Catering",
    "ESI Cafe" : "Catering",
    "Fox Cafe" : "Catering",
    "Lower Stannary" : "Catering",
    "Stannary Deli Bar" : "Catering",
    "Koofi" : "Catering",
    "The Stannary Bar" : "Catering",
    "The Sustainability Cafe" : "Catering"
    },
    "sIndex" : {
    "Falmouth Campus Shop" : 0,
    "Penryn Campus Shop" : 1,
    "AV" : 0,
    "Little Wonders Nurseries" : 1,
    "Multi Use Games Area" : 2,
    "Penryn Campus Gym" : 3,
    "Penryn Sports Centre" : 4,
    "The Compass" : 5,
    "Falmouth Campus Library" : 0,
    "Falmouth Campus Library Helpdesk" : 1,
    "Penryn Campus Library" : 2,
    "Penryn Campus Library Helpdesk" : 3,
    "Virtual Helpdesk" : 4,
    "AMATA Cafe" : 0,
    "ESI Cafe" : 1,
    "Fox Cafe" : 2,
    "Lower Stannary" : 3,
    "Stannary Deli Bar" : 4,
    "Koofi" : 5,
    "The Stannary Bar" : 6,
    "The Sustainability Cafe" : 7
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
    # Holy fucking shit why didnt i know this existed
    # now i need to refactor everything and just use this one link, fuck me
    "ServiceStatus" : "https://fxplus.ac.uk/service-status/"
}
}