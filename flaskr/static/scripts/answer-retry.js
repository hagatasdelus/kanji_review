$(function () {
    timer = setTimeout("get_answer_retry()", 20000);
});  
function get_answer_retry() {
    $.getJSON(
      "answer_retry_ajax", {
        kanji_id: kanji_id,
      },
      function (data) {
        $("#kanji").before(data["data"]);
      }
    );
}
