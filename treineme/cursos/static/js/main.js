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
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
      }
    });
}

function onPlayerReady(event) {
    console.log("Player pronto")
}

// when video ends
function onPlayerStateChange(event) {
    if(event.data === 0) {
        console.log('Vídeo finalizado');
    }
}

function videoCarregou(event){
    console.log('video carregado');
}

function videoFinalizou(id) {

    console.log('O vídeo ' + id + ' terminou');

}


function youtube_parser(url){
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
    var match = url.match(regExp);
    return (match&&match[7].length==11)? ("https://www.youtube.com/embed/" + match[7] + "?enablejsapi=1") : false;
}


$.ajax({})
