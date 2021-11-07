// Sidebar
var sidebar_id;
var sidebar_size = "-280px";

function is_sidebar() {
	var side;
	var width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
	if(width > 480) {
		side = 'right';
	} else {
		//side = 'left';
		side = 'right';
	}
	return side;
}

function ani_sidebar(div, type, val) {
	if(type == "left") {
		div.animate({ left : val });
	} else {
		div.animate({ right : val });
	}
}

function sidebar_mask(opt) {
	if(g5_is_mobile == '') return;

	var mask = $("#sidebar-box-mask");
	if(opt == 'show') {
		mask.show();
		$('html, body').css({'overflow': 'hidden', 'height': '100%'});
	} else {
		mask.hide();
		$('html, body').css({'overflow': '', 'height': ''});
	}
}

function sidebar_open(id) {

	var div = $("#sidebar-box");
	var side = is_sidebar();
	var is_div = div.css(side);
	var is_size;
	var is_open;
	var is_show;
	
	var sidebar_btn = $('.sidebar-close i');
	
	if (!$('.sidebar-wing').is(':visible'))
		$('.sidebar-wing').show();

	if(id == sidebar_id) {
		if(is_div === sidebar_size) {
			sidebar_btn.removeClass('fa-chevron-left');
			sidebar_btn.addClass('fa-chevron-right');

			is_show = false;
			ani_sidebar(div, side, '0px');
			if(side == "right") {
				sidebar_mask('show');
			} else {
				sidebar_mask('hide');
			}
		} else {
			sidebar_btn.removeClass('fa-chevron-right');
			sidebar_btn.addClass('fa-chevron-left');

			is_show = false;
			ani_sidebar(div, side, sidebar_size);
			sidebar_mask('hide');
		}
	} else {
		if(is_div === sidebar_size) {
			sidebar_btn.removeClass('fa-chevron-left');
			sidebar_btn.addClass('fa-chevron-right');

			is_show = true;
			ani_sidebar(div, side, '0px');
		} else {
			sidebar_btn.removeClass('fa-chevron-right');
			sidebar_btn.addClass('fa-chevron-left');
			is_show = true;
		}

		if(side == "right") {
			sidebar_mask('show');
		} else {
			sidebar_mask('hide');
		}
	}

	// Show
	if(is_show) {
		$('.sidebar-item').hide();

		if(id == "sidebar-user") {
			$('.sidebar-common').hide();
		} else {
			$('.sidebar-common').show();
		}

		switch(id) {
			case 'sidebar-response'	: $('#' + id + '-list').load(sidebar_url + '/response.php'); break;
			case 'sidebar-cart'		: $('#' + id + '-list').load(sidebar_url + '/cart.php'); break;
		}

		$('#' + id).show();
		$('#sidebar-content').scrollTop(0);
	}

	// Save id
	sidebar_id = id;

	return false;
}

// sidebar Empty
function sidebar_empty(id) {

	// Ajax
	switch(id) {
		case 'sidebar-cart' : $('#' + id + '-list').load(sidebar_url + '/cart.php?del=1'); break;
	}

	return false;
}

// sidebar Read
function sidebar_read(id) {

	$('#sidebar-response-list').load(sidebar_url + '/response.php?read=1&id=' + id);

	return false;
}

// sidebar Href
function sidebar_href(url) {

	$('.sidebar-menu .panel-collapse').hide();

	document.location.href = decodeURIComponent(url);

	return false;
}

// sidebar Login
function sidebar_login(f) {
	if (f.mb_id.value == '') {
		alert('아이디를 입력해 주세요.');
		f.mb_id.focus();
		return false;
	}
	if (f.mb_password.value == '') {
		alert('비밀번호를 입력해 주세요.');
		f.mb_password.focus();
		return false;
	}
	return true;
}

// sidebar Search
function sidebar_search(f) {

	if (f.stx.value.length < 2) {
		alert("검색어는 두글자 이상 입력하십시오.");
		f.stx.select();
		f.stx.focus();
		return false;
	}

	f.action = f.url.value;

	return true;
}

// sidebar Response Count
function sidebar_response() {

	var $labels = $('.sidebarLabel');
	var $counts = $('.sidebarCount');
	var url = sidebar_url + '/response.php?count=1';

	$.get(url, function(data) {
		if (data.count > 0) {
			$counts.text(number_format(data.count));
			$labels.show();
		} else {
			$labels.hide();
		}
	}, "json");
	return false;
}

// Response Auto Check
if(g5_is_member && sidebar_time > 0) {
	setInterval(function() {
		sidebar_response();
	}, sidebar_time * 1000); // Time = 1000ms ex) 10sec = 10 * 1000
}

$(document).ready(function () {

	// Sidebar Close
	/*
	$('.sidebar-close').on('click', function () {
		var div = $("#sidebar-box");
		var side = is_sidebar();
		ani_sidebar(div, side, sidebar_size); 
		sidebar_mask('hide');
		return false;
  });
  */
  
  $('.sidebar-close').on('click', function () {
		var div = $("#sidebar-box");
		var sidebar_btn = $('.sidebar-close i');
		var side = "";
		
		if (parseInt(div.css("right")) < 0) { // open				
			sidebar_btn.removeClass('fa-chevron-left');
			sidebar_btn.addClass('fa-chevron-right');
			
			sidebar_open('sidebar-user');			
			sidebar_mask('show');						
		} else {
			sidebar_btn.removeClass('fa-chevron-right');
			sidebar_btn.addClass('fa-chevron-left');
			
			side = is_sidebar();
			ani_sidebar(div, side, sidebar_size); 			
			sidebar_mask('hide');					
		}
				
		return false;
  });

	// Sidebar Menu
	$('.sidebar-menu .ca-head').on('click', function () {
		var clicked_toggle = $(this);

		if(clicked_toggle.hasClass('active')) {
			clicked_toggle.parents('.sidebar-menu').find('.ca-head').removeClass('active');
		} else {
			clicked_toggle.parents('.sidebar-menu').find('.ca-head').removeClass('active');
			clicked_toggle.addClass('active');
		}
	});

	// Sidebar Goto Top
	$('.sidebar-scrollup').on('click', function () {
				$("html, body").animate({
						scrollTop: 0
				}, 500);
				return false;
		});

	// Sidebar Change
	$(window).resize(function() {
		var side = is_sidebar();
		if(side == 'left') {
			side = 'right';
		} else {
			side = 'left';
		}
		if($("#sidebar-box").css(side) != '') {
			$("#sidebar-box").css(side, '');
			sidebar_mask('hide');
		}
	});
});