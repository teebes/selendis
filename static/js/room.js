render_room = function() {
    var room = document.player.room;
    
    $("#room_title").html(room.title);
    
    $("#room_desc").html(room.description);
    
    $("#room_items").empty();
    $.each(room.items, function() {
        item_link(this).appendTo("#room_items");
    });
    
    
    var players = ""
    $.each(room.player_related, function() {
        players += this.name + " is here<br />";
    });
    $("#room_players").html(players);
    
    var mobs = ""
    $.each(room.mob_related, function() {
        mobs += this.name + " is here<br />";
    });
    $("#room_mobs").html(mobs);
    
}
