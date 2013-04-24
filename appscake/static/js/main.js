
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
