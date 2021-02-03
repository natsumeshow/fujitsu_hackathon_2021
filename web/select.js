'use strict'

//constants
var NumOfMusics = 3;

var selected_music = 30000;
function changeSongRight(){
    //console.log("right was clicked");
    selected_music++;
    var pass = "./images/thumbnail_" + (selected_music%NumOfMusics+1) + ".png" ;
    $(".thumbnail").attr("src",pass);
}

function changeSongLeft(){
    //console.log("left was clicked");
    selected_music--;
    var pass = "./images/thumbnail_" + (selected_music%NumOfMusics+1) + ".png" ;
    $(".thumbnail").attr("src",pass);
}

function goToPlaying(){
    location.href = "./playing.html"
}

function goToResultLog(){
    location.href = "./log.html"
}

function sortMusics(){
    console.log("sorted!");
}