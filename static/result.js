$(document).ready(function() {
    selected_index = []
    // Delete Mode

    // single delete
    $('.delete-btn').click(function() {
        selected_index.push($(this).data('index'));
        console.log("in delete-btn selector",selected_index);
        // show a comfirmation dialog box
        if(!comfirmed()){
            return;
        }

        // Send Ajax request to delete route
        deleteItems(selected_index);
    });
    
    $('.delete-selected-btn').click(function() {
        if($('.translate-again-btn').is(":visible")){
            alert("Your are in Merge mode, so you can't use the Delete mode");
            return;
        }

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
        $('.item-checkbox').prop("checked",false);
    })
    // multiple delete
    $('.delete-all-btn').click(function() {
        $('.item-checkbox').each(function () {
            if($(this).is(':checked')){
                var index = $(this).data('index');
                selected_index.push(index);
            }
        });
        console.log(selected_index);
        if(selected_index.length === 0){
            alert('No items to delete');
            return;
        }
        // show a comfirmation dialog box  
        if(!comfirmed('Are you sure you want to delete all items?')){
            return;
        }
        
        // Send Ajax request to delete route
        deleteItems(selected_index);
    })
    async function deleteItems (allIndices) {
        await $.ajax({
            url: '/delete',
            type: 'POST',
            data: {indices : allIndices},
            success: function(response) {
                if (response.success) {
                    // If deletion was successful, remove all items from the list on the client side
                    allIndices.forEach(index => {
                        console.log(index)
                        $('.result[data-index="'+index+'"]').remove();
                    });

                    alert("Success Delete");
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
        
        selected_index.length = 0;
        $('.delete-cancelled-btn').trigger("click");
    }            
    // Merge Mode
    $('.translate-again-btn').click(function () {
        var merged_text = "";
        $('.merged-checkbox').each(function () {
            if($(this).is(':checked')){
                var index = $(this).data('index');
                selected_index.push(index);
                merged_text += $('.origin_text[data-index="'+index+'"]').text()
            }
        })

        if(selected_index.length === 0){
            alert('No items to merge')
            return;
        }

        if(!confirm()){
            return;
        }

        translate(merged_text, selected_index)
    })
    
    $('.merged-cancelled-btn').click(function() {
        $('.translate-again-btn').hide();
        $('.merged-selected-btn').show();
        $('.merged-checkbox').hide();
        $(this).hide();

        $('.merged-checkbox').prop('checked',false);
        selected_index.length = 0;
    })
    $('.merged-selected-btn').click(function() {
        if($('.delete-all-btn').is(":visible")){
            alert("You are in Delete Mode, so you can't use Merge mode");
            return;
        }
        $(this).hide();
        $('.translate-again-btn').show();
        $('.merged-checkbox').show();
        $('.merged-cancelled-btn').show();
    })
    
    async function translate (text, text_index){
        text_index.sort();
        console.log("Lets start to merge the text in ",text_index)
        await $.ajax({
            url: '/translate',
            type: 'POST',
            data: {text: text,
                   indices: text_index},
            success: function(response) {
                if(response.success) {
                    console.log(text_index);
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
        selected_index.length = 0;
        $('.merged-cancelled-btn').trigger("click");
    }

    // Common function in Delete Mode and Merge Mode
    function comfirmed (text){
        // Show a confirmation dialog box
        var confirmed = confirm(text);
        if (!confirmed) {
            return false; // If the user clicks "Cancel", do nothing
        }
        return true;
    }

    // Download the file
    $('.download-btn').click(function () {
        if(!confirm('Do you sure want to download the file?')){
            return;
        }

        $.ajax({
            url: '/download',
            type: 'GET',
            success: function(response) {
                if(response.success){
                    alert("Success to download");
                }
                else{
                    alert("Failed to download")
                }
            },
            error: function(){
                alert("Failed to download")
            }
        })
    })
});