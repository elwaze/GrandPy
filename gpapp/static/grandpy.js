$(document).ready(function() {
    $('#reply').click(reply);
    $(document).on('keypress', function(event) {
        if (event.which === 13) {
            event.preventDefault();
            reply();
            return false;
        }
    })
});

function reply() {
    var question = $('#question').val();
    displayQuestion(question);
    $('#loader').show();
    console.log(question)
    requestAPI(question, on_response);
}

function on_response(response) {
    try {
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
    $('#chat').append('<div class="question"><p>' + question + '</p></div>');
}

// ajax
function requestAPI(users_question, callback) {
    $.getJSON('https://elwaze-grandpybot.herokuapp.com/api/', {question: users_question}, function(data) {
        callback(data);
        $('#question').val('');
    });
}

// display grandpy response
function displayResponse(response){
    $('#chat').append('<div class="gp"><p>🤖 👴 ' + response.gp_response + '</p></div>');
}

// display map
var gmapCoord = {lat: -25.344, lng: 131.036}

var map;
    function initMap(map_id, gmapCoord){
    map = new google.maps.Map(document.getElementById(map_id), {
          center: gmapCoord,
          zoom: 12
        });
    marker = new google.maps.Marker({
        position: gmapCoord,
        map: map
    });
    }

function displayGoogleMap(coord){
    map_id = coord.lat.toString()+'_'+coord.lng.toString
    $('#chat').append('<div class="map" id="'+map_id+'"></div>');
    $('.map').show();
    gmapCoord = coord;
    initMap(map_id, gmapCoord);
}

// display wikipedia text
function displayWikipediaText(response) {
    $('#chat').append('<div class="gp"><p>🤖 👴 ' + response["wiki_response"] + response["wiki_extract"] + '[<a href=' + response["wiki_link"] + '>En savoir plus sur Wikipedia</a>]' + '</p></div>');
}
