function inspect_element(type, id) {

    if (type == 'item') {
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
                        item_link(this).appendTo("#dialog");
                    });
                }

                if (item.owner_type == 'player') {
                    // drop button if it's the player's inventory
                    var drop = $("<div class='stark_button'>Drop</div>");
                    drop.click(function () {
                        process_command('drop ' + item.id);
                        $("#dialog").dialog('close');
                        return
                    });
                    drop.appendTo("#dialog");
                    
                    // player container buttons
                    $.each(document.player.items, function() {
                        if (this.id != item.id && this.capacity > 0) {
                            var container = $("<div class='stark_button'>Put in </div>")
                            container.append(this.name);
                            var container_id = this.id;
                            container.click(function () {
                                process_command('put ' + item.id + ' ' + container_id);
                                $("#dialog").dialog('close');
                                return
                            });
                            container.appendTo("#dialog");
                        }
                    });
                    
                    // room container buttons
                    $.each(document.player.room.items, function() {
                        if (this.id != item.id && this.capacity > 0) {
                            var container = $("<div class='stark_button'>Put in </div>")
                            container.append(this.name);
                            var container_id = this.id;
                            container.click(function () {
                                process_command('put ' + item.id + ' ' + container_id);
                                $("#dialog").dialog('close');
                                return
                            });
                            container.appendTo("#dialog");
                        }
                    });
                    
                }
                
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
                
                else if (item.owner_type == 'item instance') {
                    // in another item
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

}