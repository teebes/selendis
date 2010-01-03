// -- Rooms --

create_room = function(x, y) {
    $.ajax({
        type: "POST",
        url: "/api/rooms/create/",
        data: { xpos: x, ypos: y }
    /*dataType: "json",
    success: function(room) { }*/
    });
}

modify_room = function(data) {
    $.ajax({
        type: "PUT",
        url: "/api/rooms/" + data.id + ".json",
        data: data,
        dataType: "json",
        success: function(room) {
            document.player.room = room;
            render_room();
            get_map();
        }
    });
}

delete_room = function(data) {
    $.ajax({
        type: "DELETE",
        url: "api/rooms/" + data.id + ".json",
        dataType: "json"
    });
}

render_builder = function() {
    $("#builder_box").show();
    
    $("#builder_x").html(document.player.room.xpos);
    $("#builder_y").html(document.player.room.ypos);
    
    $("#builder_room_name").val(document.player.room.name);
    $("#builder_room_name").unbind();
    $("#builder_room_name").blur(function() {
        modify_room({name: $(this).val(), id: document.player.room.id});
    });
    
    $("#builder_room_description").val(document.player.room.description);
    $("#builder_room_description").unbind();
    $("#builder_room_description").blur(function() {
        modify_room({description: $(this).val(), id: document.player.room.id});
    });
    
    // connectors
    var dirs = ['north', 'east', 'south', 'west'];
    $.each(dirs, function() {
        var dir = this;
        if (document.player.room[dir] == 'Normal') {
            $("#builder_"+dir).attr('checked', true);
        } else {
            $("#builder_"+dir).attr('checked', false);
        }

        $("#builder_"+dir).unbind();
        $("#builder_"+dir).click(function() {
            var data = {};
            data[dir] = 'toggle';
            data['id'] = document.player.room.id;
            //alert(dir);
            modify_room(data);
        });
    });
    
    // room types
    $.each($("#builder_room_type").children(), function() {
        if ($(this).attr('value') == document.player.room.type) {
            $(this).attr('selected', true);
        }
    });
    
    // jump to
    $("#jump_x").val(document.player.room.xpos);
    $("#jump_y").val(document.player.room.ypos);
}

setup_builder = function () {
    $("#delete_room").click(function() {
    var confirmation = confirm("Press Ok to delete.");
    if (confirmation) {
        delete_room(document.player.room);
    }
    });
    
    $("#jump_to").click(function() {
        move_to($("#jump_x").val(), $("#jump_y").val());
    });
 
    $("#create_room").click(function() {
        create_room($("#jump_x").val(), $("#jump_y").val());
    });
 
    $("#builder_room_type").change(function () {
        var data = {};
        data['type'] = $(this).val();
        data['id'] = document.player.room.id;
        modify_room(data);
    });
    
}
