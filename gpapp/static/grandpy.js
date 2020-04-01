$(document).ready(function() {
    $('#reply').click(function() {
        var question = $('#question').val();
        $('#chat').append('<p>' + question + '</p>');
        $('#chat').append('<img>src/giphy.gif</img>');
        console.log('tralala');
        console.log('question', question);
        $.get('http://127.0.0.1:5000/api/', {question: question}, function(response) {
            alert('Got response from server: ' + JSON.stringify(response));
        });
    })
});


// put user's question in dialog area
function display_question(users_question){
    var question = $('#reply');
    question.textContent = users_question;
}

// display waiting icon
function display_waiting(){
}

// display grandpy response
function display_response(){
}

// display map
function display_google_map(){
}

// display wikipedia text
function display_wikipedia_text(){
}
