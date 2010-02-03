var last_pulse = false;
var beat = function() {
    /*
      Central dispatching function for the client side. Runs every
      quarter of a second and sends either a load, pulse or command
      to the server
    */
    
    // load if this is the first beat
    if (typeof(stark) == 'undefined') {
        send_load();
        return;
    }

    // pulse every 2 seconds
    var now = new Date();
    now = Number(now.getTime());
    if (typeof(stark) != 'undefined' && (!last_pulse || now - last_pulse > 2000)) {
        send_pulse();
        last_pulse = now;
        return
    } else {
        // not a pulse, process a command if there is need
        if (queue.length == 0) { return; }
        send_command();
    }
}

var send_load = function() {
    $.ajax({
        type: "GET",
        url: "/api/load/",
        dataType: "json",
        success: function(new_stark) {
            stark = new_stark;
            render(['room', 'player', 'log']);
        }
    });
}

var send_pulse = function() {
    $.ajax({
        type: "GET",
        url: "/api/pulse/",
        dataType: "json",
        success: function(stark_delta) {
            sync_stark.call(this, stark_delta);
        }
    });
}

var send_command = function() {
    var cmd = queue.shift();
    
    $.ajax({
        type: "POST",
        url: "/api/command/",
        data: { command: cmd },
        dataType: "json",  
        success: function(stark_delta) {
            sync_stark.call(this, stark_delta);
        }
    });    
}
// TODO: fix this function, the changes aren't taking
var sync_stark = function(stark_delta) {
    /* Overwrites the stark object's nodes with the provided nodes
       and calls the appropriate renderer(s) */
    var keys = new Array();
    $.each(stark_delta, function(key, value) {
        stark[key] = value;
        keys.push(key);
    });
    render(keys);
}

var render = function(nodes) {
    /* Central rendering dispatcher. Does not apply to map rendering */
    $.each(nodes, function(index, value) {
        if (value.toLowerCase() == 'room') {
            render_room();
        } else if (value.toLowerCase() == 'player') {
            render_player();
        } else if (value.toLowerCase() == 'log') {
            render_log();
        }
    });    
    
    
}