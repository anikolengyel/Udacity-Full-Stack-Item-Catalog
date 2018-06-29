// Implementing logging in with Google oauth

function signInCallback(authResult) {
  if (authResult['code']) {
    // if the user is authorized, hode the login button
    $('.signinButton').attr('style', 'display: none');

    //make an ajax request and send a success message
    $.ajax({
      type: 'POST',
      url: '/gconnect?state={{STATE}}',
      processData: false,
      data: authResult['code'],
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        if (result) {
          $('#result').html('Login Successful!</br>'+ result + '</br>Redirecting...')
         setTimeout(function() {
          window.location.href = "/main";
         }, 4000);

      } else if (authResult['error']) {
    console.log('There was an error: ' + authResult['error']);
  } else {
        $('#result').html('Failed to make a server-side call. Check your configuration and console.');
         }
      }

  }); } }
