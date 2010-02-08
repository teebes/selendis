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
    } else if (stark.status == 'loading') {
        return
    } else if (stark.status == 'reload') {
        send_load();
        return
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
    if (typeof(stark) == 'undefined') {
        stark = { status: 'loading' }
    } else {
        stark.status = 'loading';
    }
    $.ajax({
        type: "GET",
        url: "/api/load/",
        dataType: "json",
        success: function(new_stark) {
            stark = new_stark;
            
            // because of a current piston shortcoming
            var _temp = stark.room.room;
            var _signature = stark.room.signature;
            stark.room = _temp;
            stark.room.signature = _signature;
            _temp = stark.player.player;
            _signature = stark.player.signature;
            stark.player = _temp;
            stark.player.signature = _signature;
            
            stark.pulses_sent = 0;
            stark.pulses_received = 0;
            render_room();
            render_player();
            render_log();
            stark.status = 'loaded';
            alert('ok');
            render_builder();
            alert('ok2');
        }
    });
}

var send_pulse = function() {
    if (typeof(stark.status) != 'undefined') {
        $("#game_status").html(stark.status);
    }
    
    var data = {};
    // caching
    if (stark.log.length) {
        data['last_log'] = stark.log[stark.log.length - 1].id;
    }
    data['room_sig'] = stark.room.signature;
    data['player_sig'] = stark.player.signature;
    
    // stark.pulses_sent += 1;
    $.get("/api/pulse/", data, function(stark_delta) {

        // pulse is a syncing call
        sync_stark.call(this, stark_delta);

        // reporting
        /* disabled for now because I don't quite have a grip on the ramifications of doing this
        stark.pulses_received += 1;
        var pulse_ratio = 0;
        if (stark.pulses_sent) {
            var sent = stark.pulses_sent;
            var received = stark.pulses_received;
            pulse_ratio = 1 - (sent - received) / sent;
        }
        $("#pulse_ratio").html(pulse_ratio);
        */ 
        
    }, dataType="json");
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
            render_builder();
        }
    });    
}

var sync_stark = function(stark_delta) {
    if (stark_delta == 'OK') {
        // nothing needs to sync, just return
        return
    }

    /* Overwrites the stark object's nodes with the provided nodes
       and calls the appropriate renderer(s) */

    render = new Array();
    $.each(stark_delta, function(key, value) {
        
        // because of a current piston shortcoming
        if (key.toLowerCase() == 'room') {
            var _signature = value.signature;
            value = value.room;
            value.signature = _signature;
        } else if (key.toLowerCase() == 'player') {
            var _signature = value.signature;
            value = value.player;
            value.signature = _signature;
        }
        
        stark[key] = value;
        if (key.toLowerCase() == 'room') {
            render.push('room');
        } else if (key.toLowerCase() == 'player') {
            render.push('player');
        } else if (key.toLowerCase() == 'log') {
            render.push('log');
        }
    });
    
    $.each(render, function() {
        if (this == 'room') { render_room(); }
        if (this == 'log') { render_log(); }
        if (this == 'player') { render_player(); }
    });
}

/* Rest client functions */

create_room = function(x, y) {
    $.ajax({
        type: "POST",
        url: "/api/rooms/create/",
        data: { xpos: x, ypos: y },
        success: function() {
            stark.status = 'reload';
        }
    });
}
 
modify_room = function(data) {
    $.ajax({
        type: "PUT",
        url: "/api/rooms/" + data.id + ".json",
        data: data,
        dataType: "json",
        success: function(room) {
            stark.status = 'reload';
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
