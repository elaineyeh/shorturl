$(document).ready(function () {
    console.log("document loaded");
    
    $("#search_button").on("click", function () {
        code = document.getElementById("search_code").value;
        var url = location.protocol + '//' + location.host + '/detail?code=' + code
        console.log("clice");
        console.log("url: ", url);

        fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
        })
            .then((response) => {
        
                console.log(response);
        
                return response.json();;
            }).then(function (data) {
                console.log("data: ", data);
        
                $('#show').html(data.show);
        
            }).catch((err) => {
                console.log('錯誤:', err);
            });
    });

    $("#copy_button").on("click", function () {
        var copyText = document.getElementById("copy_text");
        navigator.clipboard.writeText(copyText.innerText)
            .then(() => {
                console.log('Text copied to clipboard');
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
            });
    });
});