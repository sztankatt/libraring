$(document).ready(function(){
	$('#rate_transaction').ajaxForm(function(data){
		$('#rate_transaction').remove();

		$('.rate-form-container').html('thanks for rating');
	});
});