/*
 Imports:
 item_link from items.js
*/

modify_player = function(data) {
    /*
        Modify the player without a response event other than setting the
        player. This should probably be called 'modify_me' instead since it
        interacts with MeHandler in piston
    */
    $.ajax({
        type: "PUT",
        url: "/api/me.json",
        data: data,
        dataType: "json",
        success: function(player) { document.player = player; }
    });
}

render_profile = function() {
    $("#player_name").html(document.player.name);
    $("#player_level").html(document.player.level);
    $("#player_experience").html(document.player.experience);
    $("#hp").html(document.player.hp + ' / ' + document.player.max_hp);    
    $("#mp").html(document.player.mp + ' / ' + document.player.max_mp);

    // equipment
    $.each(document.player.equipment, function(key, value) {
        var span_id = "player_" + key;
        if (value) {
            var link = item_link(value);
            link.attr('id', span_id);
            $("#"+span_id).replaceWith(link);
        } else {
            var empty = str_format("<span id='{0}'>&lt;empty&gt;</span>",
                                   span_id);
            $("#"+span_id).replaceWith(empty);
        }
    });

    //inventory
    $("#player_inventory").empty();
    $.each(document.player.inventory, function() {
        var line = $("<div></div>");
        line.append(item_link(this));

        line.appendTo("#player_inventory");
    });
}