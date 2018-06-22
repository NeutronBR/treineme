"use strict";


var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;



// create youtube player
function onYouTubePlayerAPIReady() {
    player = new YT.Player('ytplayer', {
        // height: '360',
        // width: '640',
        // videoId: 'jrUVle5wdPY',
        // usei controls=0 na url. Video sendo carregado pela URL, não por aqui
        playerVars: {
            controls: '0',
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
      },
    });
    // console.log(player);
}

function onPlayerReady(event) {
    console.log(event);
}

// when video ends
function onPlayerStateChange(event) {
    if(event.data === 0) {
        // console.log('Vídeo finalizado');
        videoAssistido();
    }
}

function youtube_parser(url){
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
    var match = url.match(regExp);
    return (match&&match[7].length==11)? ("https://www.youtube.com/embed/" + match[7] + "?enablejsapi=1") : false;
}

function videoAssistido(){
    var video_pk = $("#curso_atalho").attr("data-videopk");
    var curso_atalho = $("#curso_atalho").val();

    $.ajax({
        url: '/ajax/video_assistido',
        type: "POST",
        // na url chamar função que registra filme assistido
        data: {
            'video_pk': video_pk,
            'atalho_curso': curso_atalho,
        },
        dataType: 'json',
        success: function (data) {
            showMessage(data.message);
        }
    });
}

function showMessage(msg){
    var divAlerta = document.createElement("div");
    divAlerta.setAttribute("class", "alert alert-success");
    divAlerta.setAttribute("role", "alert");
    divAlerta.innerHTML = msg;
    $('#messages').hide();
    // $('#messages').append('<div class="alert alert-success" role="alert">' + msg + '</div>').fadeIn('slow');
    $('#messages').append(divAlerta);
    $('#messages').fadeIn('slow');
    setTimeout(function(){
        $('#messages').fadeOut('slow');
        setTimeout(function(){
            divAlerta.remove();
        }, 1500);
    }, 7000);
}


// CSRF AJAX function
$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
