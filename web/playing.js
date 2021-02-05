function GoToResult(){
    //console.log("test1");
    var val = result_f();
    setTimeout(function(){
    localStorage.setItem("last_score", val.last_score);
    localStorage.setItem("figPath", val.figPath);
    localStorage.setItem("movement", val.movement);
    location.href='result.html';}, 5000);
}

async function result_f() {
    //console.log("test2");
    var val = await eel.result()();
    //console.log(val.last_score);
    return val;
}
