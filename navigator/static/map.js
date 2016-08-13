
var map;

function initMap() {
  // map = new google.maps.Map(document.getElementById('map'), {
  //   center: {lat: 37., lng: -121.},
  //   scrollwheel: false,
  //   zoom: 15,
  // });

  // google.maps.event.addListener(map, 'click', function(event) {
  //  placeMarker(event.latLng);
  // });
  bindButtons();
}


function placeMarker(location) {
	var marker = new google.maps.Marker({
	    position: location, 
	    map: map
	});
}

function bindButtons() {
	$('#north').on('click', handleButtonClick);
	$('#south').on('click', handleButtonClick);
	$('#west').on('click', handleButtonClick);
	$('#east').on('click', handleButtonClick);
	
	$('#x1').on('click', handleSpeedButtonClick);
	$('#x3').on('click', handleSpeedButtonClick);
	$('#x10').on('click', handleSpeedButtonClick);

	$('#hatch').on('click', handleHatchButtonClick);
	

	$(document).on('keypress', handleKeypress);
}

function handleButtonClick(event) {
	var url = '/step?' + 'direction=' + event.target.id;
	sendStepAjax(url);
}

function handleKeypress(e) {
	 switch(e.which) {
        case 97: // a
        case 65:
            sendStepAjax('/step?direction=west');
        break;

        case 119: // w
        case 87:
            sendStepAjax('/step?direction=north');
        break;

        case 100: // d
        case 68:
            sendStepAjax('/step?direction=east');
        break;

        case 115: // s
        case 83:
            sendStepAjax('/step?direction=south');
        break;

        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
}

function sendStepAjax(url) {
	$.ajax({
		url: url,
		data: {},
		type: 'POST',
		success: function(response) {
			var data = JSON.parse(response)['data'];
			$('#curr-loc').val(data.lat + ', ' + data.lng)
		    console.log(data);
		},
		error: function(error) {
		    console.log(error);
	    }
	});
}

function handleSpeedButtonClick(url) {
	var url = '/speed?' + 'mode=' + event.target.id;
	$.ajax({
		url: url,
		data: {},
		type: 'POST',
		success: function(response) {
		    console.log(response);
		},
		error: function(error) {
		    console.log(error);
	    }
	});
}

function handleHatchButtonClick(url) {
	var url = '/hatch';
	$.ajax({
		url: url,
		data: {},
		type: 'POST',
		success: function(response) {
		    console.log(response);
		},
		error: function(error) {
		    console.log(error);
	    }
	});
}




