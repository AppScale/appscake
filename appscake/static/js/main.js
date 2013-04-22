
$(function() {
    $("[name=toggler]").click(function(){
        $('.toHide').hide();
        $("#blk-"+$(this).val()).show('slow');
    });
});


$(document).ready(function () {
    $('.box').hide();
    $('#option0').show();
    $('#selectField').change(function () {
        $('.box').hide();
        $('#'+$(this).val()).show();
    });
});