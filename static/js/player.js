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
    
    $("#mp").html(document.player.mp + ' / ' + document.player.max_mp);

    $("#player_inventory").empty();
    $.each(document.player.items, function() {
        item_link(this).appendTo("#player_inventory");
    });
}