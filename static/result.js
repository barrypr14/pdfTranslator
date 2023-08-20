$(document).ready(function() {

    // Handle click event on delete buttons
    $('.delete-btn').click(function() {
        var index = [$(this).data('index')];
        console.log("in delete-btn selector",index);
        // show a comfirmation dialog box
        if(!comfirmed()){
            return;
        }

        // Send Ajax request to delete route
        deleteItems(index);
    });
    
    $('.delete-selected-btn').click(function() {
        $('.item-checkbox').show();
        $('.delete-all-btn').show();
        $('.delete-cancelled-btn').show();
        $(this).hide();
    });

    $('.delete-cancelled-btn').click(function () {
        $(this).hide();
        $('.delete-all-btn').hide();
        $('.delete-selected-btn').show();
        $('.item-checkbox').hide();
    })

    $('.delete-all-btn').click(async function() {
        var allIndices = [];
        $('.item-checkbox').each(async function () {
            if($(this).is(':checked')){
                var index = $(this).data('index');
                allIndices.push(index);
            }
        });
        console.log(allIndices);
        if(allIndices.length === 0){
            alert('No items to delete');
            return;
        }
        // show a comfirmation dialog box  
        if(!comfirmed()){
            return;
        }
        
        // Send Ajax request to delete route
        deleteItems(allIndices);
    })
    function deleteItems (allIndices) {
        $.ajax({
            url: '/delete',
            type: 'POST',
            data: {indices : allIndices},
            success: function(response) {
                if (response.success) {
                    // If deletion was successful, remove all items from the list on the client side
                    allIndices.forEach(index => {
                        $('.result[data-index="'+index+'"]').remove();
                    });
                } else {
                    // Handle error if the items cannot be deleted
                    alert('Failed to delete all items.');
                }
            },
            error: function() {
                // Handle error if the Ajax request fails
                alert('Failed to delete all items.');
            }
        });  
    }            
    // Handle merge event to translate the paragraph again
    $('.translate-again-btn').click(function () {
        var merged_text = "";
        var merged_index = []
        $('.merged-checkbox').each(function () {
            if($(this).is(':checked')){
                var index = $(this).data('index');
                merged_index.push(index);
                merged_text += $('.origin_text[data-index="'+index+'"]').text()
            }
        })

        if(merged_index.length === 0){
            alert('No items to merge')
            return;
        }

        if(!confirm()){
            return;
        }

        translate(merged_text, merged_index)
    })
    
    $('.merged-cancelled-btn').click(function() {
        $('.translate-again-btn').hide();
        $('.merged-selected-btn').show();
        $('.merged-checkbox').hide();
        $(this).hide();
    })
    $('.merged-selected-btn').click(function() {
        $(this).hide();
        $('.translate-again-btn').show();
        $('.merged-checkbox').show();
        $('.merged-cancelled-btn').show();
    })
    
    function translate (text, text_index){
        text_index.sort();
        console.log("Lets start to merge the text in ",text_index)
        $.ajax({
            url: '/translate',
            type: 'POST',
            data: {text: text,
                   indices: text_index},
            success: function(response) {
                if(response.success) {
                    text_index.forEach(index => {
                        if (index !== text_index[0]){
                            $('.result[data-index="'+index+'"]').remove();
                        }
                        else{
                            $('.origin_text[data-index="'+index+'"]').text(text);
                            $('.translated_text[data-index="'+index+'"]').text(response.text);
                        }
                    })
                }
                else{
                    alert('Failed to translate the new text');
                }
            },
            error: function(){
                alert('Failed to translate the new text');
            }
        });
    }
    function comfirmed (){
        // Show a confirmation dialog box
        var confirmed = confirm('Are you sure you want to delete all items?');
        if (!confirmed) {
            return false; // If the user clicks "Cancel", do nothing
        }
        return true;
    }
});