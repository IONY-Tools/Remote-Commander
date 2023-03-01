function send_command(secret, ip, port) {
    var command = document.getElementById("cmd");
    var output = document.getElementById("output");
    var data = new FormData();
    data.append('secret', secret)
    data.append('cmd', command.value)

    const req = new XMLHttpRequest();
    req.open("POST", `http://${ip}:${port}/cmd`, true)
    req.onload = function() {
        output.value=this.responseText;
        command.value = "";
    }
    req.send(data);
}