/* Imports:
  From items.js: item_link
*/

render_room = function() {
    var room = document.player.room;
    
    $("#room_title").html(room.name);
    
    $("#room_desc").html(room.description);
    
    $("#room_items").empty();
    $.each(room.items, function() {
        var line = $("<div></div>");
        line.append(item_link(this));
        line.append(" is here");

        line.appendTo("#room_items");
    });
    
    var players = ""
    $.each(room.player_related, function() {
        if (this.name != document.player.name) {
            players += this.name + " is here<br />";
        }
    });
    $("#room_players").html(players);
    
    var mobs = ""
    $.each(room.mob_related, function() {
        mobs += this.name + " is here<br />";
    });
    $("#room_mobs").html(mobs);
    
}
