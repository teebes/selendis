function item_link(item) {
    // build the item's div
    var item_div = $("<span class='inspectable'></span>");
    
    // print the item's name
    item_div.append(item.name);
    
    // give the id, if player is builder
    if (document.player.builder_mode) { item_div.append(' ['+item.id+']'); }
    
    // create the link
    item_div.click(function() { inspect_element('item', item.id); });
    
    return item_div;
}

modify_item = function(data) {
    $.ajax({
        type: "PUT",
        url: "/api/world/items/" + data.id + ".json",
        data: data,
        dataType: "json",
    });
}