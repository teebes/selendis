setup_commands = function() {
    $("#command_text").focus();
    $("#submit_command").click(function () { process_command($("#command_text").val()); });
    $("#command_text").keypress(function (e) { if (e.which == 13) { process_command($(this).val()) } });
}

process_command = function(command){
    var t = command.split(' ');
    $("#input_feedback").html('');
    $("#input_feedback").hide();

    if (t[0] == 'north' || t[0] == 'nort' || t[0] == 'nor' || t[0] == 'no' || t[0] == 'n') {
        move_to(document.player.room.xpos, document.player.room.ypos - 1);
    } else if (t[0] == 'east' || t[0] == 'ea' || t[0] == 'e') {
        move_to(document.player.room.xpos + 1, document.player.room.ypos);
    } else if (t[0] == 'south' || t[0] == 'sout' || t[0] == 'sou' || t[0] == 'so' || t[0] == 's') {        
        move_to(document.player.room.xpos, document.player.room.ypos + 1);
    } else if (t[0] == 'west' || t[0] == 'wes' || t[0] == 'we' || t[0] == 'w') {        
        move_to(document.player.room.xpos - 1, document.player.room.ypos);
    } else {
        $("#input_feedback").show();
        $("#input_feedback").html("Invalid command: '" + command + "'");
    }
    
    $("#command_text").val('');
    
}