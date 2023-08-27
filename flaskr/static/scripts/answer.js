$(function () {
  timer = setTimeout("get_answer()", 20000);
});

function get_answer() {
  let scroll = (document.scrollingElement || document.body);
  scroll.scrollTop = scroll.scrollHeight;
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
