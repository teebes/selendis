/* This library being on its own 'data.js' file no longer
  makes sense. Each area (communications, profile, room)
  needs to know how to interact with its own api.
  
  Remember to move the code accordingly
*/

/* getters */
get_map = function() {
    $.getJSON("api/world/map.json", function(map){
        document.map = map;
    });
}