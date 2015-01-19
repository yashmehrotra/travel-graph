function submit() {
    var question = $('#question').val();
    var ques_des = $('#question_desc').val();
    var ques_tag = $('#question_tags').val();

    $.ajax({
        type: "POST",
        url: "api/content/add_question",
        data: {
            'question_text':question,
            'question_desc':ques_des,
            'question_tags':ques_tag,
        },
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