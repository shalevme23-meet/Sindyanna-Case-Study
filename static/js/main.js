(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$(".toggle-password").click(function() {

	  $(this).toggleClass("fa-eye fa-eye-slash");
	  var input = $($(this).attr("toggle"));
	  if (input.attr("type") == "password") {
	    input.attr("type", "text");
	  } else {
	    input.attr("type", "password");
	  }
	});

})(jQuery);



$('.bt-language').click(function(){

    var role = $(this).data('role');

    if (role==0)
    {
        $('#list-language-box').removeClass('hidden');
        $(this).data('role',1);
    }
    else
    {
        $('#list-language-box').addClass('hidden');
        $(this).data('role',0);
    }



});