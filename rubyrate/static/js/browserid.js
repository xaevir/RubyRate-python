// when the user is found to be logged in we'll update the UI, fetch and
// display the user's favorite beer from the server, and set up handlers to
// wait for user input (specifying their favorite beer).
function loggedIn(res, immediate) {
//  setSessions([ { email: email } ]);

  // set the user visible display
  var l = $("header .login").removeClass('clickable');;
  l.empty();
  l.css('opacity', '1');
  l.append($("<span>").text(res['email']).addClass("username"))
  l.append($('<a id="logout" href="#" >(logout)</a>'));
  l.unbind('click');
  $("#logout").bind('click', logout);

  if (immediate) {
    $("#content .intro").hide();
    $("#content .business").fadeIn(300);
  }
  else {
    $("#content .intro").fadeOut(700, function() {
      $("#content .business").fadeIn(300);
    });
  }

  // enter causes us to save the value and do a little animation
  $('input').keypress(function(e){
    if(e.which == 13) {
      save(e);
    }
  });

  $("#save").click(save);

  $.ajax({
    type: 'GET',
    url: '/api/get',
    success: function(res, status, xhr) {
      $("input").val(res);
    }
  });

  // get a gravatar cause it's pretty
  var iurl = 'http://www.gravatar.com/avatar/' +
    Crypto.MD5($.trim(email).toLowerCase()) +
    "?s=32";
  $("<img>").attr('src', iurl).appendTo($("header .picture"));
}

function save(event) {
  event.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/api/set',
    data: { beer: $("input").val() },
    success: function(res, status, xhr) {
      // noop
    }
  });
  $("#content input").fadeOut(200).fadeIn(400);
}

// when the user clicks logout, we'll make a call to the server to clear
// our current session.
function logout(event) {
  event.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/api/logout',
    success: function() {
      // and then redraw the UI.
      loggedOut();
    }
  });
}

// when no user is logged in, we'll display a "sign-in" button
// which will call into browserid when clicked.
function loggedOut() {
//  setSessions();
//  $("input").val("");
//  $("#content .business").hide();
//  $('.intro').fadeIn(300);
//  $("header .picture").empty();
  var l = $("header .login").removeClass('clickable');
  l.html('<img src="/static/sign_in_red.png" alt="Sign in">')
    .show().click(function() {
      $("header .login").css('opacity', '0.5');
      //var assertion = 'eyJjZXJ0aWZpY2F0ZXMiOlsiZXlKaGJHY2lPaUpTVXpJMU5pSjkuZXlKcGMzTWlPaUppY205M2MyVnlhV1F1YjNKbklpd2laWGh3SWpveE16STBNVFl3TlRVMk9UWXdMQ0pwWVhRaU9qRXpNalF3TnpReE5UWTVOakFzSW5CMVlteHBZeTFyWlhraU9uc2lZV3huYjNKcGRHaHRJam9pUkZNaUxDSjVJam9pTXpoalpXVTROelUyT0dKaU9ERmxORGcxWVRFM05tWTVOVGMyWXpJellUVXdOV1ZsTTJVNU5UWm1ObVV4TkRZeE1XUmlZV1V6TmpneE1tSTBOV05oT0dRelpqRmlNRGhqWkdJM00yVTNPREppTlRZMFpHTmlNek5sT1Rka1pqSTVPR1F6TWpNMFpqUTJNRFE1TmpOak1qUmhNRFZrWlRRMFpEQmhNamM1TWpVeU9ETXdNVFptTXpsbU1qVXhZamt6TURNMll6QTBNek0xTlRjek5qQXhZV1U0T0dSbU1XUTNPVFpqTWpKbU9XTXhOalF6TjJRME1qTXpOR1kwWWpCak9XSmxOek0wWm1VMU5qWXdNR05oWldRNFpqZzBaR1l4TXpJek1XWTBPRGRsWmprMU5UWmxZVEJsWm1ZNU5URTJNRFl5WW1WaU9HTTNaV1F6TVdRellqSmxaVFl5WXpZeVkyUmxaVEF6TldRNE9USmpZV1F3WmpRME5EVmhNRGMzTkRWbE5qUXlNalUwTlRZNU1Ea3pNMlV3T1dObFkyRmtNMk5oTXpNeE5XTmpOVGszTUdReU1qRXpORFpqWkRrNE5USTVPVFl4WVRaa1ptUTNNRFl3WlRBME5EWXpaVEU0WmpReFpURTRPVEUxWW1VMU1XUTJZamxtWXpnelpUVTRORE5oTVRGaU5HVmxaVEl4WkRSaU1EazFabVUxWXpSbE9UQXhNek0xT1dRNE56RXdOREE1TVdFNU1HVTVOVGRsTlRSa05qVXlaRGRoWVdSa01URTVORGxrTjJZd1pUQmlaV1F3TlRjMk9HUmxNRGt6TWpjeE1HSTVZek16WlRZMlpqQTFNRGhpWmpFM01qUTBPV05pWVdGa1l6STRaVE5pTmpGa00yRXpObVlpTENKd0lqb2laRFpqTkdVMU1EUTFOamszTnpVMll6ZGhNekV5WkRBeVl6SXlPRGxqTWpWa05EQm1PVGsxTkRJMk1XWTNZalU0TnpZeU1UUmlObVJtTVRBNVl6Y3pPR0kzTmpJeU5tSXhPVGxpWWpkbE16Tm1PR1pqTjJGak1XUmpZek14Tm1VeFpUZGpOemc1TnpNNU5URmlabU0yWm1ZeVpUQXdZMk01T0RkalpEYzJabU5tWWpCaU9HTXdNRGsyWWpCaU5EWXdabVptWVdNNU5qQmpZVFF4TXpaak1qaG1OR0ptWWpVNE1HUmxORGRqWmpkbE56a3pOR016T1RnMVpUTmlNMlE1TkROaU56ZG1NRFpsWmpKaFpqTmhZek0wT1RSbVl6TmpObVpqTkRrNE1UQmhOak00TlRNNE5qSmhNREppWWpGak9ESTBZVEF4WWpkbVl6WTRPR1UwTURJNE5USTNZVFU0WVdRMU9HTTVaRFV4TWpreU1qWTJNR1JpTldRMU1EVmlZekkyTTJGbU1qa3pZbU01TTJKalpEWmtPRGcxWVRFMU56VTNPV1EzWmpVeU9UVXlNak0yWkdRNVpEQTJZVFJtWXpOaVl6SXlORGRrTWpGbU1XRTNNR1kxT0RRNFpXSXdNVGMyTlRFek5UTTNZems0TTJZMVlUTTJOek0zWmpBeFpqZ3lZalEwTlRRMlpUaGxOMll3Wm1GaVl6UTFOMlV6WkdVeFpEbGpOV1JpWVRrMk9UWTFZakV3WVRKaE1EVTRNR0l3WVdRd1pqZzRNVGM1WlRFd01EWTJNVEEzWm1JM05ETXhOR0V3TjJVMk56UTFPRFl6WW1NM09UZGlOekF3TW1WaVpXTXdZakF3TUdFNU9HVmlOamszTkRFME56QTVZV014TjJJME1ERWlMQ0p4SWpvaVlqRmxNemN3WmpZME56SmpPRGMxTkdOalpEYzFaVGs1TmpZMlpXTTRaV1l4Wm1RM05EaGlOelE0WW1KaVl6QTROVEF6WkRneVkyVTRNRFUxWVdJellpSXNJbWNpT2lJNVlUZ3lOamxoWWpKbE0ySTNNek5oTlRJME1qRTNPV1E0Wmpoa1pHSXhOMlptT1RNeU9UZGtPV1ZoWWpBd016YzJaR0l5TVRGaE1qSmlNVGxqT0RVMFpHWmhPREF4Tmpaa1pqSXhNekpqWW1NMU1XWmlNakkwWWpBNU1EUmhZbUl5TW1SaE1tTTNZamM0TlRCbU56Z3lNVEkwWTJJMU56VmlNVEUyWmpReFpXRTNZelJtWXpjMVlqRmtOemMxTWpVeU1EUmpaRGRqTWpOaE1UVTVPVGt3TURSak1qTmpaR1ZpTnpJek5UbGxaVGMwWlRnNE5tRXhaR1JsTnpnMU5XRmxNRFZtWlRnME56UTBOMlF3WVRZNE1EVTVNREF5WXpNNE1UbGhOelZrWXpka1kySmlNekJsTXpsbFptRmpNelpsTURkbE1tTTBNRFJpTjJOaE9UaGlNall6WWpJMVptRXpNVFJpWVRrell6QTJNalUzTVRoaVpEUTRPV05sWVRaa01EUmlZVFJpTUdJM1pqRTFObVZsWWpSak5UWmpORFJpTlRCbE5HWmlOV0pqWlRsa04yRmxNR1ExTldJek56a3lNalZtWldJd01qRTBZVEEwWW1Wa056Sm1Nek5sTURZMk5HUXlPVEJsTjJNNE5EQmtaak5sTW1GaVlqVmxORGd4T0RsbVlUUmxPVEEyTkRabU1UZzJOMlJpTWpnNVl6WTFOakEwTnpZM09UbG1OMkpsT0RReU1HRTJaR013TVdRd056aGtaVFF6TjJZeU9EQm1abVl5WkRka1pHWXhNalE0WkRVMlpURmhOVFJpT1RNellUUXhOakk1WkRaak1qVXlPVGd6WXpVNE56azFNVEExT0RBeVpETXdaRGRpWTJRNE1UbGpaalpsWmlKOUxDSndjbWx1WTJsd1lXd2lPbnNpWlcxaGFXd2lPaUppYjJKaWVTNWphR0Z0WW1WeWN6TXpRR2R0WVdsc0xtTnZiU0o5ZlEuZXF2TWNhcmZlaXROdjRXZFhJVkVRendQU2JNY05hMGNtdzlHNmhQZGdIUXI4NWcyNGR0WTZpbEQyMWt4bXM0d2NLSmV1UlNLcERwemVPTk5zUVVRTk1taERCWEx4TTNnSnpsODBRbW9rSlNNTXFqYmdPZm54US1pYVlQRUM1eXJzbzd0b1JTS3ZiOERWNWdwX2ZhYnNOM3FFS2ZRWjV3Mk1ha3dHbEVQMFdGSjdBUTVKQWhCME1VbEVIem8zNVFOYlBzRzVwNWRPUjFMQWhIMFg5M3VBSkI0MkxPbDNZNXFpN3hGTWlhMnlHRTRpNnNuQzhqYmZQdWJiQnZQNG9DOXJ2bnlJZV9obmVPQjZFMl9zckZldDNuWHhFMVFPTDFNQU9OZG5Fbk9CNWZVNEVhWFhUVXZhVkVYUTQ4Vm1lSkpSa3VxTnQ4WXFjN05aTVZBOGpDWi1nIl0sImFzc2VydGlvbiI6ImV5SmhiR2NpT2lKRVV6STFOaUo5LmV5SmxlSEFpT2pFek1qUXdOelF5TnpJek16WXNJbUYxWkNJNkltaDBkSEE2THk5c2IyTmhiR2h2YzNRNk5UQXdNQ0o5Lk5QbGZRQWowSGhMdkdodFRyRDJoY0FwcFNVd1VRUVFJUjBscW5ES2VzLUtUY3hsWUVFVEhEMGxtUC1RTDdkQ3VLM3IwY1gyTnFhcExUV0tscGhuOGRBIn0'
      navigator.id.getVerifiedEmail(gotVerifiedEmail);
      //gotVerifiedEmail(assertion) 
      //navigator.id.getVerifiedEmail(gotVerifiedEmail);
    }).addClass("clickable").css('opacity','1.0');
}

// a handler that is passed an assertion after the user logs in via the
// browserid dialog
function gotVerifiedEmail(assertion) {
  // got an assertion, now send it up to the server for verification
  if (assertion !== null) {
    $.ajax({
      type: 'POST',
      url: '/login',
      data: { assertion: assertion },
      success: function(res, status, xhr) {
        if (res === null) loggedOut();
        else {
            document.cookie = res['cookie']
            loggedIn(res);
        }
      },
      error: function(res, status, xhr) {
        $('html').html(res.responseText)
        //alert("login failure" + res);
      }
    });
  }
  else {
    loggedOut();
  }
}

// For some reason, login/logout do not respond when bound using jQuery
if (document.addEventListener) {
  document.addEventListener("login", function(event) {
    $("header .login").css('opacity', '0.5');
    navigator.id.getVerifiedEmail(gotVerifiedEmail);
  }, false);

  document.addEventListener("logout", logout, false);
}

// at startup let's check to see whether we're authenticated to
// myfavoritebeer (have existing cookie), and update the UI accordingly
$(function() {
  $.get('/whoami', function (res) {
    if (res === null) loggedOut();
    else loggedIn(res, true);
  }, 'json');
});
