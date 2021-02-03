'use strict'

//constants
var NumOfMusics = 3;
var selected_music = 30000;
var music_id = ["0000", "0001", "0002"];
var music_path;

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
    select_dance_f();
    localStorage.setItem("selected_music", selected_music);
    setTimeout(function(){
        localStorage.setItem("music_path", music_path);
        location.href = "./playing.html";}, 5);
}

async function select_dance_f() {
    music_path = await eel.select_dance(music_id[selected_music%NumOfMusics])();
}

function goToResultLog(){
    location.href = "./log.html"
}

function sortMusics(){
    console.log("sorted!");
}