const get_output = () => {
    return $("item-view");
}

var price = 0;
var cost = 0;

$(':input').on('propertychange input', function (e) {
    var valueChanged = false;

    if (e.type=='propertychange') {
        valueChanged = e.originalEvent.propertyName=='value';
    } else {
        valueChanged = true;
    }
    if (valueChanged) {
        if (this.name == "name"){
            $('#name-display').html($('#Item_name').val() );
        }else if (this.name == "quantity" || this.name == "cost"){
            $('#price-display').html( $('#Quantity').val() + "/" +  $('#Cost').val() + "₺");

        }else if(this.name == "category"){
            let selected = $('#category').children("option:selected").val();
            $('#category-label').html( selected );
            switch (selected){
                case "Boya":
                    $("#category-icon").html("format_color_fills");
                    break;
                case "Rulo":
                    $("#category-icon").html("imagesearch_roller");
                    break;
            }
        }
    }
});