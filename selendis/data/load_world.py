def load_demo_rooms():
    from selendis.models import Room

    # center
    Room({ 
        "x": 0, "y": 0, "z": 0, 
        "key": "center", 
        "name": "Center", 
        "north": { 
            "key": "north" 
        }
    })

    # north
    Room({ 
        "x": 0, "y": 1, "z": 0, 
        "key": "north", 
        "name": "North",
        "description": "There is little to see here.",
        "south": { 
            "key": "center",
         }
     })

def load_demo_anima():
    from selendis.models import Anima

    load_demo_rooms()
   
    # anima 
    return Anima({
        'key': 'anima', 
        'room': { 'key': 'center' }, 
        'stats': {
            'mp': 200
        }
    })
