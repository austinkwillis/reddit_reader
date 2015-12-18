$SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
  $(function() {
    $('a#save').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_save', {
        submission_id: this.name
      })
      return false;
    });
})
  $(function() {
    $('a#unsave').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_unsave', {
        submission_id: this.name
      })
      return false;
  });
})