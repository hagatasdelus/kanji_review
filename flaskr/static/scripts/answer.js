$(function () {
  timer = setTimeout("get_answer()", 5000);
});

function get_answer() {
  $.getJSON(
    "answer_ajax",
    {
      kanji_id: kanji_id,
    },
    function (data) {
      $("#kanji").after(data["data"]);
    }
  );
}
