$(document).ready(function () {
    $("#hide_question_comments").click(function () {
        $(".question_comments").toggle(1000)
    });
});

function confirmDelete(url) {
    if (confirm("Are you sure you want to delete this?")) {
        window.open(url);
    } else {
        false;
    }
}

$(document).ready(function () {
    $("#show_hide").click(function () {
        $(".add_answer").toggle(1000)
    });
});


$(document).ready(function () {
    $("#show_answers").click(function () {
        $(".answer_table").toggle(1000)
    });
});

$(document).ready(function () {
    $(".btn").click(function () {
        $(".input").toggleClass("active");
    })
})