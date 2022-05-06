// Required packages
var http = require('http');

test_html = `
<!DOCTYPE html>
<html>
<body>

    <h1>This is the start of the PRISMS Printer Network!</h1>

</body>
</html>
`

// Create server
http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(test_html);
}).listen(8080); 