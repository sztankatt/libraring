function scrollChat(){
    $('.message-earlier-messages').scrollTop(9999999);
}

function load_earlier_messages(scrollDown){
    $message_display = $('.message-display .message-earlier-messages').
        load('/ajax/load/conversation/',
             {
                'csrfmiddlewaretoken': $.cookie('csrftoken'),
                'transaction_id':$('.message-display #id_transaction').val()
                }, function(){
                    
                    if (scrollDown){
                        scrollChat();
                    }
                    
                    });
}

function page_loaded(){
    var $message_submit_button = $('.message-display .message-submit-button').attr({'disabled':true});
    
    $('.message-display .message-compose #id_text').on('input', function(){
        $val = $(this).val();
        
        if ($val == "") {
            $message_submit_button.attr({'disabled':true});
        }
        else{
            $message_submit_button.attr({'disabled':false});
        }
    });
    
    
    load_earlier_messages(true);
    
    
    //alert('loaded');
    
    $('#new_message_form').ajaxForm(function(data){
        $('#id_text').val('');
        
        $("#new_message_form button[type='submit']").attr('disabled', 'true');
        
        $('.message-display .message-earlier-messages').append(data);

        scrollChat();
        
    });

    $('#id_text').keypress(function(event){
        var val = $('#id_text').val();

        if (val != "" && event.which == 13 && $('.message-use-enter').is(':checked')){
            event.preventDefault();
            $('#new_message_form').submit();
        }
    });

}


$(document).pjax(".message-show-all-body a", "#pjax-container");


$(document).ready(function(){
  page_loaded();
    
});

$(document).on('pjax:complete', function() {
    page_loaded();
});


/* 
 * HANDLING THE REALTIME CHAT 
 */
$(document).ready(function(){
   
        var transaction_id = $('#id_transaction').val();
        $('a.new-message').click(function(){
            $(this).removeClass('new-message');

        });

        $('#link_to_transaction_'+transaction_id+' a').addClass('viewing');

        $('.message-show-all-body a').click(function(){
            $('.message-show-all-body a').removeClass('viewing');
            $(this).addClass('viewing');
        });




        ishout.on('messages', function(data){
            $message_link = $('#link_to_transaction_'+data.transaction_id);

            $parent = $message_link.parent();

            $message_link.remove();

            $parent.prepend($message_link);


            if (data.transaction_id == transaction_id){
                $('.message-earlier-messages').append(data.msg);
                scrollChat();
            }
            else{
                new_message_item = $('#link_to_transaction_'+data.transaction_id+' a');

                new_message_item.addClass('new-message');
            }
        });

        ishout.init();

        



});

