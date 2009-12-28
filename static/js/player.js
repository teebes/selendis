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
        success: function(player) {
            document.player = player
            //render_profile();
        }
    });
}

render_profile = function() {
    $("#player_name").html(document.player.name);
    $("#player_level").html(document.player.level);
    $("#player_experience").html(document.player.experience);
    $("#hp").html(document.player.hp + ' / ' + document.player.max_hp);    
    $("#mp").html(document.player.mp + ' / ' + document.player.max_mp);

    $.each(document.player.equipment, function(key, value) {
        if (!value) {
            var html = "&lt;empty&gt;" ;
        } else {
            var html = value.name;
        }
        $("#player_" + key).html(html);
    });

    $("#player_inventory").empty();
    $.each(document.player.inventory, function() {
        var line = $("<div></div>");
        line.append(item_link(this));

        line.appendTo("#player_inventory");
    });
}