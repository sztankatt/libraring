var error_field_header ='#error .modal-header';
var error_field_body = '#error .modal-body';
var error_field = '#error';

function update_profile(input, output){
    $.ajax({
        'type':'GET',
        'url' :'/ajax/update/profile/',
        'data':input,
        'dataType':'json',
        'success':function(data){
            output(data);
        }
    })
}

function email_confirmation(input, output) {
    $.ajax({
        'type':'GET',
        'url' :'/ajax/email/change/confirmation/',
        'data':input,
        'dataType':'json',
        'success':function(data){
            output(data);
        }
    })
}

/*
 * PROFILE UPDATE VALIDATORS
 * */ 

    



$(document).ready(function(){
validators_feedback_icons = {
                        valid: 'glyphicon glyphicon-ok',
                        invalid: 'glyphicon glyphicon-remove',
                        validating: 'glyphicon glyphicon-refresh'
                    };
    var profile_update_validators = {
            'first_name' : $('#first_name_form').bootstrapValidator({
                    feedbackIcons: validators_feedback_icons,
                    fields: {
                        first_name:{
                            validators:{
                                notEmpty:{
                                    message: 'The First name field cannot be empty!'
                                }
                            }
                        }
                    }
                }),
            'last_name': $('#last_name_form').bootstrapValidator({
                feedbackIcons: validators_feedback_icons,
                fields: {
                    last_name:{
                        validators:{
                            notEmpty:{
                                message: 'The Last name field cannot be empty!'
                            }
                        }
                    }
                }

            }),
            'current_education': $('#current_education_form')
                .find('[id="new_current_education_institution"]')
                .change(function(e){
                    $('#current_education_form').bootstrapValidator(
                        'revalidateField', 'email'
                    )
                })
                .end()
                .bootstrapValidator({
                feedbackIcons: validators_feedback_icons,
                fields: {
                    institution:{
                        validators:{
                            notEmpty:{
                                message: 'Please Choose a new Institution'
                            }
                        }
                    },
                    course:{
                        validators:{
                            notEmpty:{
                                message: 'Please Choose a new Course'
                            }
                        }
                    },
                    start_year:{
                        validators:{
                            notEmpty:{
                                message: 'Please Choose a new Start year'
                            }
                        }
                    },
                    
                    end_year:{
                        validators:{
                            notEmpty:{
                                message: 'Please Choose a new End year'
                            }
                        }
                    },
                    email:{
                        validators:{
                            notEmpty: {
                                message:'This field is required.'
                            },
                            remote:{
                                message: 'Wrong email ending.',
                                url: '/ajax/check/email/ending/',
                                type: 'GET',
                                data: function(validator) {
                                    return {
                                        institution: validator.getFieldElements('institution').val()
                                    };
                                }
                            },
                            emailAddress:{
                                message: 'Wrong email address.'
                            }
                        }
                    }
                    
                }
                
            }),
            'previous_education': $('#previous_education_form').bootstrapValidator({
                feedbackIcons: validators_feedback_icons,
                fields: {
                    institution:{
                        validators:{
                            notEmpty:{
                                message: 'Please Choose a new Institution'
                            }
                        }
                    },
                    course:{
                        validators:{
                            notEmpty:{
                                message: 'Please Choose a new Course'
                            }
                        }
                    },
                    start_year:{
                        validators:{
                            notEmpty:{
                                message: 'Please Choose a new Start year'
                            }
                        }
                    },
                    
                    end_year:{
                        validators:{
                            notEmpty:{
                                message: 'Please Choose a new End year'
                            }
                        }
                    }
                }
            })
    };
            
    
    


var validator_handle = function(validator){
    validator
        .on('success.form.bv', function(e){
                $(error_field_body).html('');
                e.preventDefault();
                var $form = $(e.target);

                // Get the BootstrapValidator instance
                var bv = $form.data('bootstrapValidator');
                bv.resetForm();
                
                var form_id = $form.attr('id');
                
                switch(form_id){
                    case "first_name_form":
                        var type = 'first_name';
                        input = {
                            "type":type,
                            "first_name": $('#first_name').val()
                        };
                        //on success
                        update_profile(input, function(data){
                           $("#"+type+"_container").children('.profile-field-header').
                                children('.profile-field-header-body').children('.field-data').html(data.first_name);
                            
                            //clear the inputs
                            $('.profile-update-input').val("");
                            $form.parent().slideUp();
                            //succes message
                            toastr.success("Success!");
                        });
                    break;
                    
                    case "last_name_form":
                        var type = 'last_name';
                        input = {
                            "type":type,
                            "last_name": $('#last_name').val()
                        };
                        //on success
                        update_profile(input, function(data){
                            $("#"+type+"_container").children('.profile-field-header').
                                children('.profile-field-header-body').children('.field-data').html(data.last_name);
                            
                            //clear the inputs
                            $('.profile-update-input').val("");
                            $form.parent().slideUp();
                            //succes message
                            toastr.success("Success!");
                        });
                    break;
                    
                    case "current_education_form":
                        var type = 'current_education';
                        var field = '#new_current_education_';
                        var input = {
                            "type"          : type,
                            "institution"   : $(field+"institution").val(),
                            "course"        : $(field+"course").val(),
                            "start_year"    : $(field+"start_year").val(),
                            "end_year"      : $(field+"end_year").val()
                        };
                        update_profile(input, function(data){
                            if (data.error){
                                show_error(data);
                                console.log('error, data:'+data);
                            }
                            else{
                                bv.destroy();
                                $form.submit();
                            }
                        });
                    break;
                    
                    case "previous_education_form":
                        var type = 'previous_education';
                        var field = '#new_previous_education_';
                        var input = {
                            "type"          : type,
                            "institution"   : $(field+"institution").val(),
                            "course"        : $(field+"course").val(),
                            "start_year"    : $(field+"start_year").val(),
                            "end_year"      : $(field+"end_year").val()
                        };
                        console.log(input);
                        
                        update_profile(input, function(data){
                            if (data.error){
                                show_error(data);
                            }
                            else{
                                console.log(data);
                                bv.destroy();
                                $form.submit();
                            }
                        });
                    break;
                }
                
        });
};
 for (key in profile_update_validators) {
    validator_handle(profile_update_validators[key]);
}               
    /*
 *registration validators
 */
    $('#registration_user_form').bootstrapValidator({
        feedbackIcons: validators_feedback_icons,
        fields:{
            'user-username' :{
                validators:{
                    notEmpty:{
                        message: 'This field is required.'
                    },
                    remote:{
                        message: 'This username already exists. Please choose another one',
                        url: '/ajax/check/username/available/',
                        type: 'GET'
                    },
                    stringLength:{
                        max: 30,
                        min: 1,
                        message: 'Please enter a value between %s and %s characters long'
                    },
                    regexp:{
                        regexp: /^[\w.-]+$/
                    }

                }
            },
            'user-password1':{
                validators:{
                    notEmpty:{
                        message: 'This field is required'
                    },
                    stringLength:{
                        min: 6,
                        max: 20
                    }
                }
            },
            'user-password2':{
                validators:{
                    notEmpty:{
                        message: 'This field is required'
                    },
                    identical:{
                        field:'user-password1',
                        message: 'The two passwords did not match'
                    },
                    stringLength:{
                        min: 6,
                        max: 20
                    }
                }
            }
        }
    });

    
    
    $('#registration_person_form').bootstrapValidator({
        feedbackIcons: validators_feedback_icons,
        excluded: ':disabled',
        fields:{
            'person-email':{
                validators:{
                    notEmpty:{
                        message: 'This field is required.'
                    },
                    emailAddress:{
                        message: 'Not a valid email address.'
                    }
                }
            },
            'person-first_name':{
                validators:{
                    notEmpty:{
                        message: 'This field is required.'
                    }
                }
            },
            'person-last_name':{
                validators:{
                    notEmpty:{
                        message: 'This field is required.'
                    }
                }
            },
            'person-person_type':{
                validators:{
                    notEmpty:{
                        message: 'This field is required.'
                    }
                }
            },
            'person-city':{
                validators:{
                    notEmpty:{
                        message:'This field is required.'
                    }
                }
            },
            'person-postcode':{
                validators:{
                    notEmpty:{
                        message:'This field is required.'
                    },
                    regexp:{
                        regexp: /^[0-9a-zA-Z ]*$/,
                        message: "Only alphanumeric characters are allowed."
                    }

                }
            },
            'person-country':{
                validators:{
                    notEmpty:{
                        message:'This field is required.'

                    }
                }
            },
            'person-terms_conditions':{
                validators:{
                    notEmpty:{
                        message:'This field is required.'

                    }
                }
            },
            'person-privacy_policy':{
                validators:{
                    notEmpty:{
                        message:'This field is required.'

                    }
                }
            }
        }
    });
    
    $('#registration_class_form')
        .find('[id="id_class-institution"]')
        .change(function(e){
            $('#registration_class_form').bootstrapValidator(
                'revalidateField', 'class-email'
            )
        })
        .end()
        .bootstrapValidator({
        feedbackIcons: validators_feedback_icons,
        fields:{
            'class-institution':{
                validators:{
                    notEmpty: {
                        message:'This field is required.'
                    }
                }
            },
            'class-course':{
                validators:{
                    notEmpty: {
                        message:'This field is required.'
                    }
                }
            },
            'class-start_year':{
                validators:{
                    notEmpty: {
                        message:'This field is required.'
                    }
                }
            },
            'class-end_year':{
                validators:{
                    notEmpty: {
                        message:'This field is required.'
                    }
                }
            },
            'class-terms_conditions':{
                validators:{
                    notEmpty:{
                        message: 'Please accept the terms and conditions and the privacy policy!'
                    }
                }
            }/*,
            'class-email':{
                validators:{
                    notEmpty: {
                        message:'This field is required.'
                    },
                    remote:{
                        message: 'Wrong email ending.',
                        url: '/ajax/check/email/ending/',
                        type: 'GET',
                        data: function(validator) {
                            return {
                                institution: validator.getFieldElements('class-institution').val()
                            };
                        }
                    },
                    emailAddress:{
                        message: 'Wrong email address.'
                    }
                }
            }*/
        }
    });

  
    
    $('#email_confirmation_form').bootstrapValidator({
        feedbackIcons: validators_feedback_icons,
        fields: {
            confirmation_code:{
                validators:{
                    notEmpty:{
                        message: 'Please insert your confirmation Code!'
                    },
                    regexp:{
                        regexp: /^[A-Z0-9]{6}$/,
                        message: 'Your code should have exactly 6 characters: digits or upper-case letters'
                    }
                }
            }
        }
    })
    
    .on('success.form.bv', function(e){
        e.preventDefault();
        
        var confirmation_code = $('#email_confirmation_code').val();
        
        input ={
            'type':'email_change_confirmation',
            'confirmation_code' : confirmation_code
        };
        
        email_confirmation(input, function(data){
            if(data.error){
                show_error(data);
            }
            else{
                toastr.success('Success!');
                $('#new-email-success').fadeIn();
            }
        });
    });
    
    /*BOOK VALIDATORS */
    
    //$('#id_author').attr({'name':'author'});
    
    $('form#book_upload')
        .find('[id="id_author"]')
        .change(function(e){
            $('form#book_upload').bootstrapValidator(
                'revalidateField', 'author'
            );
        })
        .end()
        .find('[id="id_genre"]')
        .change(function(e){
            $('form#book_upload').bootstrapValidator(
                'revalidateField', 'genre'
            );
        })
        .end()
        .bootstrapValidator({
            feedbackIcons: validators_feedback_icons,
            fields:{
                author:{
                    //selector: '#id_author',    
                    validators:{
                        notEmpty:{
                            message: 'Please choose at least one Author'
                        }
                    }
                },
                genre:{
                    //selector: '#id_genre',
                    validators:{
                        notEmpty:{
                            message: 'Please choose at least one Genre.'
                        }
                    }
                },
                title:{
                    validators:{
                        notEmpty:{
                            message: 'Please insert the title!'
                        }
                    }
                },
                edition: {
                    validators:{
                        between:{
                            min: 1,
                            max: 30,
                            message: 'Please enter the edition of your book'
                        },
                        notEmpty:{
                            message: 'Please enter the edition of your book'
                        }
                    }
                },
                publication_year:{
                    validators:{
                        notEmpty:{
                            message: 'Please enter when was the book published.'
                        },
                        between:{
                            min: 1000,
                            max: (new Date).getFullYear()
                        }
                    }
                },
                publication_city:{
                    validators:{
                        regexp:{
                            regexp: /^[A-Za-z\s]+$/i,
                            message: 'The city name can consist alphabetical characters and spaces only'
                        }
                    }
                },
                price:{
                    validators:{
                        between:{
                            min:0,
                            max: 1000,
                            message: 'Please enter the price of your book'
                        },
                        notEmpty:{
                            message: 'Please enter the prie of your book'
                        },
                        integer:{
                            message: 'Only integers are allowed'
                        }
                    }
                },
                isbn:{
                    validators:{
                        isbn:{
                            message: 'Please insert a valid ISBN number.'
                        }
                    }
                }
                
            }
        });
        /*.on('status.field.bv', function(e, data){
            if (data.field == 'isbn' || data.field == 'publication_city') {
                if ($(e.target).val() == ""){
                    var $parent = data.element.parents('.form-group');
    
                    // Remove the has-success class
                    $parent.removeClass('has-success');
        
                    // Hide the success icon
                    $parent.find('.form-control-feedback[data-bv-icon-for="' + data.field + '"]').hide();
                }
            }
        })
        .on('success.form.bv', function(e){
            e.preventDefault();
            var $form = $(e.target);
            $('body').addClass('loading');
             
            $form.ajaxSubmit({success:function(data){
               if (data.success) {
                   $('#book_upload_form').modal('hide');
                   $('body').removeClass('loading');
                   toastr.success('Uploaded!');
               }
            }, dataType:'json', semantic:true});
        });*/
        
        
        //clearing the form
        $('#book_upload_form').on('hide.bs.modal', function(e){
            $this = $(this);
            $this.find('form').data('bootstrapValidator').resetForm();
            $this.find('form').trigger('reset');
           
            $this.find('.select2-search-choice').remove();
            $this.find('input[type="hidden"]').val('').attr('txt', '');
        });
});