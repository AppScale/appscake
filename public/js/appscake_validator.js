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

    $('#iaas_euca_form').validate({
        rules: {
            euca_min: {
                required: true,
                number: true,
                min: 1
            },
            euca_max: {
                required: true,
                number: true,
                min: 1
            },
            euca_emi: {
                required: true
            },
            euca_username: {
                required: true
            },
            euca_url: {
                required: true,
                url: true
            },
            euca_walrus_url: {
                required: true,
                url: true
            },
            euca_private_key: {
                required: true
            },
            euca_cert: {
                required: true
            },
            euca_access_key: {
                required: true
            },
            euca_secret_key: {
                required: true
            },
            euca_user: {
                required: true,
                email: true
            },
            euca_pass: {
                required: true,
                minlength: 6
            },
            euca_pass2: {
                required: true,
                minlength: 6,
                equalTo: euca_pass
            },
            euca_keyname: {
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