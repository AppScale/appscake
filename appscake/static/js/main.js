
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
        range: true,
        min: 1,
        max: 8,
        values: [1, 2],
        slide: function(event, ui) {
            var min = ui.values[0],
                max = ui.values[1];

            $("#amount").val("" + min + " - " + max);
        }
    }, min, max;

    $("#slider-range").slider(options);

    min = $("#slider-range").slider("values", 0);
    max = $("#slider-range").slider("values", 1);

    $("#amount").val("" + min + " - " + max);

});