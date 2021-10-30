$(document).ready(function(){
    displayItems(items)
    console.log(items)
});

function displayItems() {
    var count = 0;https://github.com/adrianaorantes/prof-feedback/blob/main/dashboard.js
    items.forEach(function (entry){

        var row1=$('#row1')
        
                    if(count==0){
                    var col1=$('<td id="phone'+entry['question_id']+'">+18452826490</td>')
                    var col2=$('<td>'+entry['body']+'</td>')
                    $(row1).append(col1)
                    $(row1).append(col2)
                    count=1
                }

                else if(count==1){
                    var col2=$('<td>'+entry['body']+'</td>')
                    $(row1).append(col2)
                    console.log(row)
                    count=2
                    $("#tbody").append(row1)
                }



    }
    
    )


}

