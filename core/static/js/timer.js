var timer;
var time = document.getElementById('time-for-test').value *60;
test_timer()



function test_timer() {
    time*60
    time--;
    if (time < 0){
        clearTimeout(timer);
        document.getElementById('test-end-btn').click();
    }
    else{
        h = time/3600 ^ 0,
        m = (time-h*3600)/60 ^ 0,
        s = time-h*3600-m*60,
        document.getElementById('test-time').innerHTML = (h<10?"0"+h:h) +':'+ (m<10?"0"+m:m) +':'+(s<10?"0"+s:s);
        timer = setTimeout(test_timer, 1000);
        }
}
