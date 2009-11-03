setup_commands = function() {
    $("#command_text").focus();
    $("#submit_command").click(function () { process_command($("#command_text").val()); });
    $("#command_text").keypress(function (e) { if (e.which == 13) { process_command($(this).val()) } });
}

process_command = function(command){
    var t = command.split(' ');
    $("#input_feedback").html('');
    $("#input_feedback").hide();

    first = t[0].toLowerCase();

    if (first == 'north' || first == 'nort' || first == 'nor' || first == 'no' || first == 'n') {
        move_to(document.player.room.xpos, document.player.room.ypos - 1);
    } else if (first == 'east' || first == 'ea' || first == 'e') {
        move_to(document.player.room.xpos + 1, document.player.room.ypos);
    } else if (first == 'south' || first == 'sout' || first == 'sou' || first == 'so' || first == 's') {        
        move_to(document.player.room.xpos, document.player.room.ypos + 1);
    } else if (first == 'west' || first == 'wes' || first == 'we' || first == 'w') {        
        move_to(document.player.room.xpos - 1, document.player.room.ypos);
    } else {
        $("#input_feedback").show();
        $("#input_feedback").html("Invalid command: '" + command + "'");
    }
    
    $("#command_text").val('');
    
}