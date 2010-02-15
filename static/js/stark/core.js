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
    if (!last_pulse || now - last_pulse > 2000) {
        send_pulse();
        last_pulse = now;
        return
    } else {
        // not a pulse, process a command if there is need
        if (queue.length > 0) {
            send_command();
            return
        }
    }
}

var send_load = function() {
    //$(stark).attr('status', 'loading');
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
            var _signature = $(stark.room).attr('signature');
            stark.room = _temp;
            stark.room.signature = _signature;
            _temp = stark.player.player;
            _signature = $(stark.player).attr('signature');
            stark.player = _temp;
            stark.player.signature = _signature;
            stark.pulses_sent = 0;
            stark.pulses_received = 0;
            pulse_tracker = [];
            render_room();
            render_player();
            render_log();
            stark.status = 'loaded';
            if ($(stark.player).attr('builder_mode')) {
                render_builder();
            }
        }
    });
}

var get_signatures = function() {
    var data = {};
    // caching
    try {
        data['last_log'] = stark.log[stark.log.length - 1].id;
    } catch(e) {
        data['last_log'] = 0;
    }
    data['room_sig'] = stark.room.signature;
    data['player_sig'] = stark.player.signature;
    return data
}

var pulse_id = 0;
var pulse_queue = [];
var pulses_sent = 0;
var pulses_received = 0;
var send_pulse = function() {
    $("#game_status").html($(stark).attr('status'));
    
    // caching signatures
    var data = get_signatures()
    
    pulse_queue.push(pulse_id++);
    pulses_sent++;
    $.get("/api/pulse/", data, function(stark_delta) {
        pulses_received++;
        // pulse is a syncing call
        sync_stark.call(this, stark_delta);
        // sync_stark(stark_delta);
        pulse_queue.pop(0);
    }, dataType="json");
    
    if (pulse_id) {
        if (pulse_queue.length < 2) {
            $("#game_status").html('connected');
        } else {
            $("#game_status").html('disconnected');
        }
        if (pulse_id == 5) {
            pulse_id = 1;
            pulse_queue = [1];
        }
    }

    $("#pulses_received").html(pulses_received);
    $("#pulses_sent").html(pulses_sent);

}

var send_command = function() {
    var cmd = queue.shift();

    // caching signatures
    var data = get_signatures()
    //var data = {}
    data['command'] = cmd;

    $.ajax({
        type: "POST",
        url: "/api/command/",
        data: data,
        dataType: "json",  
        success: function(stark_delta) {
            sync_stark.call(this, stark_delta);
            if ($(stark.player).attr('builder_mode')) {
                render_builder();
            }
        }
    });    
}

var sync_stark = function(stark_delta) {
    // sanity check on input
    if (stark_delta === null) { return; }
    
    // nothing needs to sync
    if (stark_delta == 'OK') { return }

    /* Overwrites the stark object's nodes with the provided nodes
       and calls the appropriate renderer(s) */

    var render = [];
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

    $.each(render, function(index, value) {
        if (value == 'room') { render_room(); }
        if (value == 'log') { render_log(); }
        if (value == 'player') { render_player(); }
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
