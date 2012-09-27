$(document).ready(function() {
    $('#virtual_form').validate({
        rules: {
            ips: {
                required: true
            },
            root_password: {
                required: true
            },
            user: {
                required: true,
                email: true
            },
            pass: {
                required: true,
                minlength: 6
            },
            pass2: {
                required: true,
                minlength: 6,
                equalTo: pass
            },
            keyname: {
                required: true
            }
        },
        highlight: function(label) {
            $(label).closest('.control-group').addClass('error');
        },
        success: function(label) {
            label
                .addClass('valid')
                .closest('.control-group').removeClass('error');
        }
    });

    $('#iaas_ec2_form').validate({
        rules: {
            min: {
                required: true,
                number: true,
                min: 1
            },
            max: {
                required: true,
                number: true,
                min: 1
            },
            ami: {
                required: true
            },
            username: {
                required: true
            },
            private_key: {
                required: true
            },
            cert: {
                required: true
            },
            access_key: {
                required: true
            },
            secret_key: {
                required: true
            },
            user: {
                required: true,
                email: true
            },
            pass: {
                required: true,
                minlength: 6
            },
            pass2: {
                required: true,
                minlength: 6,
                equalTo: pass
            },
            keyname: {
                required: true
            }
        },
        highlight: function(label) {
            $(label).closest('.control-group').addClass('error');
        },
        success: function(label) {
            label
                .addClass('valid')
                .closest('.control-group').removeClass('error');
        }
    });
});