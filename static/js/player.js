get_player = function() {
    $.getJSON("/api/players/me.json", function(player) {
        document.player = player;
    });
}

/* modifiers */

modify_player = function(data) {
    $.ajax({
        type: "PUT",
        url: "/api/players/me.json",
        data: data,
        dataType: "json",
        success: function(player) {
            document.player = player
        }
    });
}

render_profile = function() {
    $("#player_name").html(document.player.name);
    $("#player_level").html(document.player.level);
    

    var inventory = '';
    $.each(document.player.items, function() {
        inventory += this.name;
        if (document.player.builder_mode) {
            inventory += ' [' + this.id + '] ';
        }
        inventory += '<br />';
    });
    $("#player_inventory").html(inventory);
}