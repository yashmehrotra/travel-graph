$(function () {
    var ques_id = $('#ques-id').text();
    submit(ques_id);
    $('#ans-submit').on('click', function (){
        var ans_text = $('#ans-text').val();
        add_ans(ques_id, ans_text);
    });
});

function submit(ques_id) {
    $.ajax({
        type: "GET",
        url: "/api/content/get_answers/" + ques_id + "/",
        success: function(result) {
            if(result) {
                console.log(result);
                result = JSON.parse(result);
                console.log(result['status']);
                console.log(result.message);
            } else {
                console.log('Problem with ajax');
            }
        }
    });
}

function add_ans(ques_id, ans_text) {
    $.ajax({
        type: "POST",
        url: "/api/content/add_answer",
        data: {
            'question_id': ques_id,
            'answer': ans_text,
        },
        success: function(result) {
            if(result) {
                console.log(result);
                result = JSON.parse(result);
                console.log(result['status']);
                console.log(result.message);
                append();
            } else {
                console.log('Problem with ajax');
            }
        }
    });
}

function append() {
    for (var i = answers.length - 1; i >= 0; i--) {
        $('#ans ul').append('<li>' + answers[i].answer + '</li>')
    }
    };
    
}