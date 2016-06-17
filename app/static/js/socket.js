function createJSONPacket(method, params, id) {
    return {
        jsonrpc: '2.0',
        method: method,
        params: params,
        id: id
    }
}

function makeRequest(data, type, url) {
    if (type == undefined || type == '') {
        var type = 'GET';
    }

    var req = $.ajax({
        url: '/support',
        type: type,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json'
    });

    return req;
}
