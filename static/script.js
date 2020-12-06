document.getElementById("but").addEventListener("click",()=>{
    $.ajax({
        type: 'POST',
        url: '/kinect',
        data: JSON.stringify({
            "left_arm":true,
            "right_arm":false
        }),
        contentType: 'application/json',
        success: function (response_data) {
            alert("success");
        }   
    });
})