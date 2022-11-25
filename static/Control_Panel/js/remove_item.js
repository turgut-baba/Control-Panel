var all_items = [];

$(".sales").each( function(){
    all_items.push( $(this).val($(this).attr("item_id")) );
});

var item_to_be_deleted = 0;
var url_body = "";
console.log("hi");

function setDeletedItem(body, item_id)
{
     console.log(item_id);
     console.log(body);
     item_to_be_deleted = item_id;
};

function setUrlBody(body)
{
    url_body = body;
};