// Contains all of the ui related to client-side evented interactions

function item_link(item) {
    // build the item's div
    var item_div = $("<span class='inspectable'></span>");
    
    // print the item's name
    item_div.append(item.name);
    
    // give the id, if player is builder
    if (stark.player.builder_mode) { item_div.append(' ['+item.id+']'); }
    
    // create the link
    item_div.click(function() { inspect_element('item', item.id); });
    
    return item_div;
}


/* ---- INITIAL BINDINGS ---- */

setup_builder = function () {
    $("#delete_room").click(function() {
    var confirmation = confirm("Press Ok to delete.");
    if (confirmation) {
        delete_room(stark.player.room);
    }
    });
    
    $("#jump_to").click(function() {
        $.ajax({
            type: "PUT",
            url: "/api/me.json",
            // data: { xpos: $("#jump_x").val(), ypos: $("#jump_y").val() },
            data: { command: str_format("jump {0} {1}", $("#jump_x").val(), $("#jump_y").val()) },
            dataType: "json",
            success: function(player) {
                stark.player = player;
                render_room();
                render_builder();
                stark.player_map_xpos = player.room.xpos;
                stark.player_map_ypos = player.room.ypos;
            }
        });
    });
 
    $("#create_room").click(function() {
        create_room($("#jump_x").val(), $("#jump_y").val());
    });
 
    $("#builder_room_type").change(function () {
        var data = {};
        data['type'] = $(this).val();
        data['id'] = stark.player.room.id;
        modify_room(data);
    });
}

setup_player = function() {
    var button = $("#player_details_button");
    button.click(function() {
        $("#player_details").toggle('fast');
        if (button.html() == 'v') {
            button.html('^');
        } else {
            button.html ('v');
        }
    });
}