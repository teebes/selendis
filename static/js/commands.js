/* Imports:
  from DOM: document.player
  from room.js: render_room
  from data.js: get_map
  from builder.js: render_builder
  from player.js: render_profile
  from builder.js: modify_room
  from item.js: modify_item
  from communications.js: send_communications
*/

var commands = {
    north: 0,
    east: 0,
    south: 0,
    west: 0,
}
var match_command = function(user_input) {
    /*
     Takes in a command and matches it against the list of possible commands,
     returning the canonical command name for further processing.
     Starts with each command, and takes one letter off the right until
     there is a match or no more letters.
     
     For example, the candidates for "north" are:
     'north', 'nort', 'nor', 'no', and 'n'
    */

    for (command in commands) {
        var cmd_tokens = command.split('');
        for (var i = 0 ; i < cmd_tokens.length ; i++) {
            var candidate = cmd_tokens.slice(0, cmd_tokens.length - i).join('');
            if (user_input.toLowerCase() == candidate) {
                return command;
            }
        }
    }
    return false;
}

var send_command = function(command) {
    // processes all commands except for directional ones
    $.ajax({
        type: "PUT",
        url: "/api/me.json",
        data: { command: command },
        dataType: "json",
        success: function(player) {
            document.player = player;
        }
    });
}

var move = function(direction) {

    var x;
    var y;
    if (direction == 'north') {
        x = document.player_map_xpos;
        y = document.player_map_ypos - 1;
    } else if (direction == 'east') {
        x = document.player_map_xpos + 1;
        y = document.player_map_ypos;
    } else if (direction == 'south') {
        x = document.player_map_xpos;
        y = document.player_map_ypos + 1;
    } else if (direction == 'west') {
        x = document.player_map_xpos - 1;
        y = document.player_map_ypos;

    }

    // check the map to see if this is a direction that is available
    if ($(document.player.room).attr(direction) == 'Normal') {
        
        // if the player has enough moves,
        // this is so that directions can be spammed and movement appears fluid
        if (document.player.mp > 2) {
            // store a cached version of the player's new position
            document.player_map_xpos = x;
            document.player_map_ypos = y;
            
            // store the last time that the player moved so that if a pulse
            // comes back right after a player has moved, it doesn't change their
            // position
            document.last_move = new Date().getTime();
        }
        
    }
    
    $.ajax({
        type: "PUT",
        url: "/api/me.json",
        data: { xpos: x, ypos: y },
        dataType: "json",
        success: function(player) {
            document.player = player;
            render_room();

            if (player.builder_mode) {
                render_builder();
            }
            render_profile();
        }
    });
}

var move_to_2 = function(direction) {
    
    // check the map to see if this is a direction that is available
    if ($(document.player.room).attr(direction) == 'Normal') {
        return 
    }
    
}

/* bindings & command execution */

var setup_commands = function() {
    $("#command_text").focus();
    $("#submit_command").click(function () { process_command($("#command_text").val()); });
    $("#command_text").keypress(function (e) { if (e.which == 13) { process_command($(this).val()) } });
    
    $("#move_north").click(function () { process_command('north'); });
    $("#move_east").click(function () { process_command('east'); });
    $("#move_south").click(function () { process_command('south'); });
    $("#move_west").click(function () { process_command('west'); });
    
}

var process_command = function(command){
    var t = tokens = command.split(' '); // t for tokens
    
    $("#input_feedback").html('');
    $("#input_feedback").hide();

    $("#command_text").val('');   

    first = match_command(tokens[0]);

    if (first == 'north' || first == 'east' || first == 'west' || first == 'south') {
        move(first);
    }

    
    send_command(command);
    return    
}