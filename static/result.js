$(document).ready(function() {
    selected_index = [];
    deleteSelectedFlag = false;
    mergedSelectedFlag = false;
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

        // $('.item-checkbox').show();
        $('.delete-all-btn').show();
        $('.delete-cancelled-btn').show();
        $(this).hide();
        deleteSelectedFlag = true;
    });

    $('.delete-cancelled-btn').click(function () {
        $(this).hide();
        $('.delete-all-btn').hide();
        $('.delete-selected-btn').show();
        $('.item-checkbox').hide();
        $('.item-checkbox').prop("checked",false);
        deleteSelectedFlag = false;
    })
    // multiple delete
    $('.delete-all-btn').click(function() {
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
            error: function(response) {
                // Handle error if the Ajax request fails
                alert('Failed to delete all items.');
                console.log(response.error);
            }
        }); 
        
        selected_index.length = 0;
        $('.delete-cancelled-btn').trigger("click");
    }            
    // Merge Mode
    $('.translate-again-btn').click(function () {
        var merged_text = "";
        selected_index.forEach((index) => {
            merged_text += $('.origin_text[data-index="'+index+'"]').text();
        })

        if(selected_index.length === 0){
            alert('No items to merge')
            return;     
        }

        if(!confirm()){
            return;
        }

        translate(merged_text, selected_index);
    })
    
    $('.merged-cancelled-btn').click(function() {
        $('.translate-again-btn').hide();
        $('.merged-selected-btn').show();
        $('.merged-checkbox').hide();
        $(this).hide();

        $('.merged-checkbox').prop('checked',false);
        selected_index.length = 0;
        mergedSelectedFlag = false;
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
        mergedSelectedFlag = true;
    })
    
    async function translate (text, text_index){
        console.log("Lets start to merge the text in ",text_index)
        await $.ajax({
            url: '/translate',
            type: 'POST',
            data: {text: text,
                   indices: text_index},
            success: function(response) {
                if(response.success) {
                    text_index = response.indices;
            
                    text_index.forEach(index => {
                        console.log(index);
                        tmp_index = index.join('-');
                        console.log(tmp_index)
                        if (index !== text_index[0]){
                            $('.result[data-index="'+tmp_index+'"]').remove();
                        }
                        else{
                            $('.origin_text[data-index="'+tmp_index+'"]').text(text);
                            $('.translated_text[data-index="'+tmp_index+'"]').text(response.text);
                            $('.result[data-index="'+tmp_index+'"]').css('background-color','gold');
                        }
                    })
                }
                else{
                    alert('Failed to translate the new text');
                }
            },
            error: function(response){
                console.log(response.error);
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
        if(!confirm('Do you want to download the file?')){
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
            error: function(response){
                alert(response.error)
            }
        })
    })

    // Click Mode
    $('.result').on('click',function(){
        if( deleteSelectedFlag || mergedSelectedFlag) {
            const dataIndex = $(this).data('index');
            const indexExists = selected_index.includes(dataIndex);

            if(!indexExists){
                selected_index.push(dataIndex);
                $(this).css('background-color','lightskyblue');
            }
            else{
                selected_index = $.grep(selected_index,function(value){
                    return value !== dataIndex;
                });
                $(this).css('background-color','');
            }
    
            console.log('select index : ',dataIndex);
        }
    })

    // Undo Mode
    $('.back-btn').click(async function() {
        await $.ajax({
            url: '/back',
            type: 'GET',
            success: function(response) {
                if(response.success && response.undo !== 'nothing'){
                    window.location.reload();
                    alert("undo successfully");
                }
                else{
                    alert("nothing undo");
                }
            },
            error: function(response){
                alert("Fail to use the undo mode");
            }
        })
    })
});