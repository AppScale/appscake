
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

//Removes EC2/Euca fields and replaces them with the appropriate GCE fields
    $('#infrastructure').change(function(){
    if($('#infrastructure').val() == 'gce'){
        $('#instance_type').hide();
        $('#access_key').hide();
        $('#secret_key').hide();
        $('#machine_type').hide();
        $('#url').hide();
        $('#gce_creds').show();
        $('#gce_project').show();
        $('#gce_image').show();
    }
    else{
        $('#instance_type').show();
        $('#access_key').show();
        $('#secret_key').show();
        $('#machine_type').show();
        $('#url').show();
        $('#gce_creds').hide();
        $('#gce_project').hide();
        $('#gce_image').hide();
    }
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

