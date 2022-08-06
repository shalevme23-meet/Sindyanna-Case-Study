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

var LanguagePicker = function(element) {
  this.element = element;
  this.select = this.element.getElementsByTagName('select')[0];
  this.options = this.select.getElementsByTagName('option');
  this.pickerId = this.select.getAttribute('id');
  // ..
  initLanguagePicker(this);
};

//initialize the LanguagePicker objects
var languagePicker = document.getElementsByClassName('js-language-picker');
if( languagePicker.length > 0 ) {
  for( var i = 0; i < languagePicker.length; i++) {
      new LanguagePicker(languagePicker[i]);
  }
}

function initLanguagePicker(picker) {
  // create the HTML for the custom dropdown elementand and insert it in the DOM
  picker.element.insertAdjacentHTML('beforeend', initButtonPicker(picker) + initListPicker(picker));
};

function initButtonPicker(picker) { // create the button element -> language picker trigger
  var button = '<button class="language-picker__button" aria-label="'+picker.select.value+' '+picker.element.getElementsByTagName('label')[0].textContent+'" aria-expanded="false" aria-controls="'+picker.pickerId+'-dropdown">';
  button = button + '<span aria-hidden="true" class="language-picker__flag language-picker__flag--'+picker.select.value+'"></span>';
  return button+'</button>';
};

function initListPicker(picker) { // create language picker dropdown
  var list = '<div class="language-picker__dropdown" aria-describedby="'+picker.pickerId+'-description" id="'+picker.pickerId+'-dropdown">';
  list = list + '<p class="sr-only" id="'+picker.pickerId+'-description">'+picker.element.getElementsByTagName('label')[0].textContent+'</p>';
  list = list + '<ul class="language-picker__list" role="listbox">';
  for(var i = 0; i < picker.options.length; i++) {
    var selected = picker.options[i].hasAttribute('selected') ? ' aria-selected="true"' : '',
      language = picker.options[i].getAttribute('lang');
    list = list + '<li><a lang="'+language+'" hreflang="'+language+'" href="'+getLanguageUrl(picker.options[i])+'"'+selected+' role="option" data-value="'+picker.options[i].value+'" class="language-picker__item language-picker__flag language-picker__flag--'+picker.options[i].value+'"><span>'+picker.options[i].text+'</span></a></li>';
  };
  return list;
};

// click events
picker.trigger.addEventListener('click', function(){
   toggleLanguagePicker(picker);
});

function toggleLanguagePicker(picker, bool) {
  var ariaExpanded;
  if(bool) {
     ariaExpanded = bool;
  } else {
     ariaExpanded = picker.trigger.getAttribute('aria-expanded') == 'true' ? 'false' : 'true';
  }

  picker.trigger.setAttribute('aria-expanded', ariaExpanded);
  if(ariaExpanded == 'true') {
    picker.dropdown.addEventListener('transitionend', function cb(){
      // once the dropdown is visible -> move focus from trigger to the first language in the list
      picker.firstLanguage.focus();
      picker.dropdown.removeEventListener('transitionend', cb);
    });
  }
};

// listen for key events
window.addEventListener('keyup', function(event){
  if( event.keyCode && event.keyCode == 27 || event.key && event.key.toLowerCase() == 'escape' ) {
    // close language picker on 'Esc'
    pickerArray.forEach(function(element){
      moveFocusToTrigger(element); // if focus is still within the dropdown, move it to dropdown trigger
      toggleLanguagePicker(element, 'false'); // close dropdown
    });
  }
});

function moveFocusToTrigger(picker) {
  if(picker.trigger.getAttribute('aria-expanded') == 'false') return;
  if(document.activeElement.closest('.language-picker__dropdown') == picker.dropdown) picker.trigger.focus();
};