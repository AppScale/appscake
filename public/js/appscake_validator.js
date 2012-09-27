$(document).ready(function() {
    $('#virtual_form').validate({
        rules: {
            ips: {
                required: true
            },
            root_password: {
                required: true
            },
            virtual_user: {
                required: true,
                email: true
            },
            virtual_pass: {
                required: true,
                minlength: 6
            },
            virtual_pass2: {
                required: true,
                minlength: 6,
                equalTo: virtual_pass
            },
            virtual_keyname: {
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
            ec2_user: {
                required: true,
                email: true
            },
            ec2_pass: {
                required: true,
                minlength: 6
            },
            ec2_pass2: {
                required: true,
                minlength: 6,
                equalTo: ec2_pass
            },
            ec2_keyname: {
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