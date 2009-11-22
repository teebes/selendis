render_room = function() {
    var room = document.player.room;
    
    $("#room_title").html(room.title);
    
    $("#room_desc").html(room.description);
    
    var items = ""
    $.each(room.items, function() {
        items += this.name;
        items += ' [' + this.id + ']';
        items += " is here<br />";
    });
    $("#room_items").html(items);
    
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
    
    if (document.player.builder_mode) {
        render_builder()
    }
}
