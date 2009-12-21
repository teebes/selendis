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

    // main hand
    var main_hand = "&lt;empty&gt;";
    if (document.player.main_hand) { main_hand = document.player.main_hand.name; }
    $("#player_main_hand").html(main_hand);

    // head
    // chest
    // arms
    // legs
    // feet

    $("#player_inventory").empty();
    $.each(document.player.items, function() {
        var line = $("<div></div>");
        line.append(item_link(this));

        line.appendTo("#player_inventory");
    });
}