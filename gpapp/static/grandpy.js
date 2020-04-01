$(document).ready(function() {
    $('#reply').click(function() {
        var question = $('#question').val();
        displayQuestion(question);
        $('#loader').show();
        requestAPI(question, on_response);
    })
});

function on_response(response) {
    try {
        console.log('response', response);
        displayResponse(response);
        if (response.gmap_coord) {
            displayGoogleMap(response.gmap_coord);
        }
        if (response.wiki_response) {
            displayWikipediaText(response);
        }
    } catch(e) {
        $('#chat').append('<p class="error">' + e + '</p>');
    }

    $('#loader').hide();
}

// put user's question in dialog area
function displayQuestion(question){
    $('#chat').append('<p>' + question + '</p>');
}

// ajax
function requestAPI(users_question, callback) {
    $.getJSON('http://127.0.0.1:5000/api/', {question: users_question}, function(data) {
        console.log('response type =>', typeof response)
        callback(data)
    });
}

// display grandpy response
function displayResponse(response){

//    $('#chat').append('<p>' + JSON.parse(response).gp_response + '</p>');
    $('#chat').append('<p>' + response.gp_response + '</p>');
}

// display map

var gmapCoord = {lat: -25.344, lng: 131.036}


var map;
    function initMap(){
    map = new google.maps.Map(document.getElementById('map'), {
          center: gmapCoord,
          zoom: 8
        });
    }

function displayGoogleMap(coord){
    console.log('Google coord', coord);
    console.log('Google coord', typeof coord);
    $('#map').show()
    gmapCoord = coord;
    initMap();
}

// display wikipedia text
function displayWikipediaText(response) {
    $('#chat').append('<p>' + response["wiki_response"] + response["wiki_extract"] + '[<a href=' + response["wiki_link"] + '>En savoir plus sur Wikipedia</a>]' + '</p>');
}
