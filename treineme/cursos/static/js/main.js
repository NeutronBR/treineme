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
    console.log('video carregado')
}

function videoFinalizou(id) {

    alert("The video has ended " + id);

}
