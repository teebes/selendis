function button_put_item_in(item, container) {
    // Checks to see if the container conatains any sub comtainers, and if so
    // prints put in buttons for them
    $.each(container, function() {
        // if it has capacity but isn't the item being inspected
        if (this.id != item.id && this.capacity > 0) {
            var button = $("<div class='stark_button'>Put in </div>")
            button.append(this.name);
            var container_id = this.id;
            button.click(function () {
                process_command('put ' + item.id + ' ' + container_id);
                $("#dialog").dialog('close');
                return
            });
            button.appendTo("#dialog");
        }
    });
}

// TODO: button_wear and button_remove can probably be merged into a generic
// name to command function
function button_wear(item) {
    var button = $("<div class='stark_button'>Wear</div>");
    button.click(function() {
        process_command('wear ' + item.id);
        $("#dialog").dialog('close');
    });
    button.appendTo("#dialog");
}

function button_remove(item) {
    var button = $("<div class='stark_button'>Remove</div>");
    button.click(function() {
        process_command('remove ' + item.id);
        $("#dialog").dialog('close');
    });
    button.appendTo("#dialog");
}

function inspect_item(id) {
    $.ajax({
        type: "GET",
        url: "/api/items/" + id + ".json",
        data: null,
        dataType: "json",
        success: function(item) {
            $("#dialog").dialog('close');
            $('#dialog').dialog('option', 'title', item.name);
            $("#dialog").empty();
            
            // container stuff
            if (item.contains != '') {
                $("#dialog").append("<p>This item contains:</p>");
                $.each(item.contains, function() {
                    var line = $("<div></div>");
                    line.append(item_link(this));
                    line.appendTo("#dialog");
                });
            }
            
            // on a player TODO: make sure this is self
            if (item.owner_type == 'player') {
                // drop button if item is in inventory
                var on_inventory = false;
                for (var i = 0 ; i < stark.player.inventory.length ; i++) {
                    if (item.name == stark.player.inventory[i].name) {
                        on_inventory = true;
                        break;
                    }
                }
                if (on_inventory) {
                var drop = $("<div class='stark_button'>Drop</div>");
                drop.click(function () {
                    process_command('drop ' + item.id);
                    $("#dialog").dialog('close');
                    return
                });
                drop.appendTo("#dialog");
                }
                // add the put in buttons for containers in
                // player eq, inv or room
                button_put_item_in(item, stark.player.equipment);
                button_put_item_in(item, stark.player.inventory);
                button_put_item_in(item, stark.room.items);
                // wear / remove
                if (item.type == 'weapon' || item.type == 'armor') {
                    // check that the player is not already wearing something
                    // on that slot
                    var slot_occupied = false;
                    $.each(stark.player.equipment, function(k, v) {
                        if (k == item.slot && v) {
                            slot_occupied = true;
                            button_remove(this);
                            return true;
                        }
                    });
                    if (!slot_occupied) {
                        button_wear(item);
                    }
                }
            }
            
            
            // in a room
            else if (item.owner_type == 'room') {
                // take button if it's in a room
                var get= $("<div class='stark_button'>Get</div>");
                get.click(function () {
                   process_command('get ' + item.id);
                   $("#dialog").dialog('close');
                   return
                });
                get.appendTo("#dialog");
            }
            
            // in another item
            else if (item.owner_type == 'item instance') {
                var get= $("<div class='stark_button'>Get</div>");
                get.click(function () {
                   process_command('get ' + item.id + ' ' + item.owner_id);
                   $("#dialog").dialog('close');
                   return
                });
                get.appendTo("#dialog");
            }

            $("<div class='clear'></div>").appendTo("#dialog");

            $("#dialog").dialog('open');
        }
    });
}

function inspect_element(type, id) {

    if (type == 'item') {
        inspect_item(id);
    }

}