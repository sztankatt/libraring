/*toastr*/


/*
 * HELPER FUNCTIONS
 * */
function get_email_ending(institution, output){
    $.ajax({
        'type':'GET',
        'url' : '/ajax/email/ending/',
        'data': {id:institution},
        'success' :function(data){
            output(data);
        }
    })
}


function print_email_ending(inst_field, email_field, helper_field) {
    var email_end = $(email_field).parent().children(helper_field);
    $(inst_field).change(function(){
        var inst_id = $(inst_field + ' option:selected').val();
        if (inst_id == "") {
            email_end.html('Please choose an intitution!');
        }
        else{
            get_email_ending(inst_id, function(data){
               email_end.html('Your email address has to end with '+data); 
            });
        }
    });
}




function show_error(args){
    $("#error .modal-header").prepend("<strong>ERROR! "+args.error_header+"</strong>");
        $("#error .modal-body").html(args.error_message);
        
        $("#error").modal();
}

function get_error_ajax(name) {
    $.ajax({
        'type': 'GET',
        'data': {'name': name},
        'dataType': 'json',
        'url': '/ajax/get/error/message/',
        'success': function(data){
            show_error(data);
        }
    })
}

function success() {
    toastr.success('Success!');
}


$(document).ready(function(){
    /* 
     *  BASE EVENT HANDLERS   
     * */
    $("#error").on('hidden.bs.modal', function(){
        $("#error .modal-header").html('<button type="button" class="close" data-dismiss="modal">'
                                    +'<span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>'
                                    +'<h4 class="modal-title" id="error_title"></h4>');
    });
    
     /*
     * REGISTER PAGE
     * */
    print_email_ending('#id_institution-institution', '#id_institution-email', '.register-form-helper-field');
    print_email_ending('#id_class-institution', '#id_class-email', '.email-ending-help');
    print_email_ending('#current_education_form #id_current_education_institution', 
        '#current_education_form #new_current_education_email', '.email-ending-help');
    
    /*
     * INDEX PAGE
     */
    
    //clock plugin
    /*$('#clock').countdown('2014/09/01').on('update.countdown', function(event){
       var $this = $(this).html(event.strftime(''
            +'<div class="col-md-4 col-sm-4 col-xs-4"><span>%-w</span>weeks'
            +'<span>%-d</span>days'
            +'<span>%H</span>hours'
            +'<span>%M</span>minutes'
            +'<span>%S</span>seconds</div>')); 
    });
 */
        
    /*
     * PROFILE PAGE
     * */
    //institution change
    print_email_ending('#new_current_education_institution', '#new_current_education_email', '.email-ending-help');
    
    /* update part */
    $('.profile-update-button').click(function(){
        var container = $(this).parent().parent().parent().children('.profile-update');
        container.slideDown();
    });
    
    //closing profile-update
    $('.profile-update-cancel').click(function(){
        var container = $(this).parent().parent().find('.profile-update-save').val();
        $update_element = $("#"+container+"_container").children('.profile-update').slideUp();
        console.log(container);
        $('#'+container+'_container input').val('');
        $('#'+container+'_container select').val('');

        $update_element.find('.email-ending-help').html('');

        
        //handling the bootstrap validator
        var form = $('#'+container+'_form');
        var bv = form.data('bootstrapValidator');
        bv.resetForm();
    });
    
    
    
    
    /*
     *EDUCATION DELETE
     */
    $('.previous-education-delete').click(function(){
        $(this).parent().parent().parent().children('.previous-education-delete-confirm').slideDown();
    });
    
    //deleting it for sure lol
    $('.previous-education-delete-yes').click(function(){
        var class_id = $(this).val();
        $this = $(this);
        update_profile({'type':'education_delete', 'education_id':class_id}, function(data){
            if (data.error) {
                show_error(data);
            }
            else{
                $this.parent().parent().slideUp("slow", function(){
                    $this.remove();
                });
                success();
            }
        });
    });
    
    //cancel the deletion
    $('.previous-education-delete-no').click(function(){
        $(this).parent().slideUp(); 
    });
    
    
    
    //adding new previous education
    $('#add_new_education').click(function(){ $('#add_new_education_container').slideToggle();});    
});