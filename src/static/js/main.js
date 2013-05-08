
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







$("#slider").slider({
    range: "min",
    value: 1,
    min: 1,
    max: 8,
    slide: function( event, ui ) {
        $( "#amount" ).val( ui.value );
    }
});
$("#amount").change(function () {
    var value = this.value.substring();
    $("#slider").slider("value", parseInt(value));
});
