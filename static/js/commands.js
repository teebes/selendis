setup_commands = function() {
    $("#command_text").focus();
    $("#submit_command").click(function () { process_command($("#command_text").val()); });
    $("#command_text").keypress(function (e) { if (e.which == 13) { process_command($(this).val()) } });
    
    $("#move_north").click(function () { process_command('north'); });
    $("#move_east").click(function () { process_command('east'); });
    $("#move_south").click(function () { process_command('south'); });
    $("#move_west").click(function () { process_command('west'); });
    
}

process_command = function(command){
    var t = command.split(' ');
    $("#input_feedback").html('');
    $("#input_feedback").hide();

    $("#command_text").val('');   

    first = t[0].toLowerCase();

    // directions
    if (first == 'north' || first == 'nort' || first == 'nor' || first == 'no' || first == 'n') {
        move_to(document.player.room.xpos, document.player.room.ypos - 1);
        return
    } else if (first == 'east' || first == 'ea' || first == 'e') {
        move_to(document.player.room.xpos + 1, document.player.room.ypos);
        return
    } else if (first == 'south' || first == 'sout' || first == 'sou' || first == 'so' || first == 's') {        
        move_to(document.player.room.xpos, document.player.room.ypos + 1);
        return
    } else if (first == 'west' || first == 'wes' || first == 'we' || first == 'w') {        
        move_to(document.player.room.xpos - 1, document.player.room.ypos);
        return
    }
    
    // set
    else if (first == 'set') {
        if (document.player.builder_mode && t[1] == 'room' && t[2] && t[3]) {
            var attribute = t[2];
            
            if (attribute == 'xpos' || attribute == 'ypos') {
                $("#input_feedback").show();
                $("#input_feedback").html("Too dangerous!");
            }
            
            t.shift();
            t.shift();
            t.shift();
            
            var data = {};
            data['id'] = document.player.room.id;
            data[attribute] = t;
            modify_room(data);
            return
        }
    }
    
    else if (first == 'help') {
        $("#input_feedback").show();
        $("#input_feedback").html("Commands: north east south west");
        return
    }
    

    $("#input_feedback").show();
    $("#input_feedback").html("Invalid command: '" + command + "'");

    
}