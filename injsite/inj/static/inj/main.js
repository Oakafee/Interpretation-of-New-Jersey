$('div#comment-form').hide();

$('button#add-comment').click(function(){
	$('div#comment-form').toggle();
	if ($('#submit').is(':visible')) {
		$('html, body').animate({
        	scrollTop: $("#submit").offset().top - $('#comments').height() - 125
		}, 750);
	}
});

$('textarea#comment').click(function(){
	$(this).replaceWith("<textarea name='comment' rows='10' cols='30' id='comment'></textarea>");
	$('textarea#comment').focus();
});

$('.expand').click(function(){
	var list = $(this).parent().next()
	if ($(this).html()=="+") {
		list.removeClass('hidden');
		$(this).html('-');
	} else {
		list.addClass('hidden');
		$(this).html('+');
	}
});

$('.menu-container').hover(function(){
	item = $(this);
	if (item.hasClass('menu-clicked')==false) {
		console.log('go ahead');
		menuHoverEffect(item);
	}
});

function menuHoverEffect(menu){
	menu.toggleClass('white');
	menu.children().toggleClass('blue');
}

$('.menu-container').click(function(){
	$(this).toggleClass('menu-clicked');
	menuHoverEffect($(this));
	console.log('i want to toggle');
	$('#chart').toggleClass('hidden');
});

$('#content-overlay').click(function(event){
	if (!$('#chart').hasClass('hidden')) {
		console.log('the target is not chart');
		$('#chart').addClass('hidden');
		$('.menu-container').toggleClass('menu-clicked');
	}
});