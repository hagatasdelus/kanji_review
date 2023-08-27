$(function () {
  timer = setInterval("get_answer()", 1000);
});

function get_answer() {
  $.getJSON(
    "answer_ajax",
    {
      kanji_id: kanji_id,
    },
    function (data) {
      $("#kanji").before(data["data"]);
    }
  );
}
