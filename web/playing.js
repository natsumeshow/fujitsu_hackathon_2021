function GoToResult(){
    var val = result_f();
    setTimeout(function(){
    localStorage.setItem("last_score", val.last_score);
    localStorage.setItem("figPath", val.figPath);
    localStorage.setItem("movement", val.movement);
    location.href='result.html';}, 200);
}

async function result_f() {
    return val = await eel.result()();
}