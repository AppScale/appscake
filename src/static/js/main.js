
$(function() {
    $("[name=toggler]").click(function(){
        $('.toHide').hide();
        $("#blk-"+$(this).val()).show('slow');
    });
});


$(document).ready(function () {
    $('.box').hide();
    $('#simple').show();
    $('#select-required').change(function () {
        $('.box').hide();
        $('#'+$(this).val()).show();
    });
});



$(function() {
    var options = {
        range: "min",
        value: 1,
        min: 1,
        max: 8,
        slide: function(event, ui) {
            $("#amount").val(ui.value);
        }
    }, min;

    $("#slider").slider(options);
    min = $("#slider").slider("values", 0);

    $("#amount").val("" + min );

});

$("#amount").change(function () {
    var value = this.value.substring();
    $("#slider").slider("value", parseInt(value));
});
