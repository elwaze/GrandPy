$(document).ready(function() {
    $('#reply').click(function() {
        var question = $('#question').val();
        displayQuestion(question);
        displayWaiting();
        var response = ajaxGet(question);
//        stopWaiting();
        displayResponse(response);
        if (response["gmap_coord"]) {
        displayGoogleMap(response["gmap_coord"]);
        }
        if (response["wiki_response"]) {
        displayWikipediaText(response);
        }
    })
});

// put user's question in dialog area
function displayQuestion(question){
    $('#chat').append('<p>' + question + '</p>');
}

// display waiting icon
function displayWaiting(){
    $('#chat').append('<img src="static/src/waiting.gif" alt="Je réfléchis..." />');
}

// ajax
function ajaxGet(users_question, callback){
    var ajaxReq = new XMLHttpRequest();
        ajaxReq.open("GET", "http://127.0.0.1:5000/api/"+question);
        req.addEventListener("load", function() {
        $.get('http://127.0.0.1:5000/api/', {question: question}, function(response) {
            alert('Got response from server: ' + JSON.stringify(ajaxReq.responseText));
        });
        return response
    });
}

// display grandpy response
function displayResponse(response){
    $('#chat').append('<p>' + response['gp_response'] + '</p>');
}

// display map
function displayGoogleMap(gmapCoord){
    $('#chat').append('<div id="map"></div>')
    $('#chat').append('<script></script>')
    var map;
    function initMap(){
    map = new google.maps.Map(document.getElementById('map'), {
          center: gmapCoord,
          zoom: 8
        });
    }
    $('#chat').append('<script src=' + app.config.GOOGLE_MAPS_LINK + '></script>')
}

// display wikipedia text
function displayWikipediaText(){
    $('#chat').append('<p>' + response["wiki_response"] + response["wiki_response"] + '[<a href=' + response["wiki_link"] + '>En savoir plus sur Wikipedia</a>]' + '</p>');
}
