// -- Rooms --

create_room = function(x, y) {
    $.ajax({
        type: "POST",
        url: "/api/world/rooms/create/",
        data: { xpos: x, ypos: y }
    /*dataType: "json",
    success: function(room) { }*/
    });
}

modify_room = function(data) {
    $.ajax({
        type: "PUT",
        url: "/api/world/rooms/" + data.id + ".json",
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
        url: "api/world/rooms/" + data.id + ".json",
        dataType: "json"
    });
}

// -- Items --

modify_item = function(data) {
    $.ajax({
        type: "PUT",
        url: "/api/world/items/" + data.id + ".json",
        data: data,
        dataType: "json",
    });
}


render_builder = function() {
    $("#builder_box").show();
    
    $("#builder_x").html(document.player.room.xpos);
    $("#builder_y").html(document.player.room.ypos);
    
    $("#builder_room_title").val(document.player.room.title);
    $("#builder_room_title").unbind();
    $("#builder_room_title").blur(function() {
        modify_room({title: $(this).val(), id: document.player.room.id});
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
            $(this).attr('selected', true)
        }
    })
    
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
        create_room($("#create_x").val(), $("#create_y").val());
    });
 
    $("#builder_room_type").change(function () {
        var data = {}
        data['type'] = $(this).val();
        data['id'] = document.player.room.id
        modify_room(data);
    });
    
}
