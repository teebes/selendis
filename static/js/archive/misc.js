/* Bits of JS code that are no longer in use on the project but that may
  be of use later on somewhere */

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

var send_object = function(object, url) {
    // requires JSON, http://www.json.org/json2.js
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: url,
        data: JSON.stringify(object),
        processData: false,
        dataType: "json",        
        success: function() { }
    });
}

escape_html = function(html) {
    // utility function to escape html and convert newlines
    // http://stackoverflow.com/questions/24816/escaping-strings-with-jquery
    html = html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return html
}
