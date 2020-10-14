let notConfirmed = true;
const cardId = "{{card.id}}";
const deleteBtn = document.querySelector('#delete-btn');
const body = document.querySelector('body');
deleteBtn.addEventListener('click', function(e){
    if (notConfirmed) {
        e.preventDefault();
        let ac = new AlertController("DELETE CARD", "Are you sure you delete this card??", "DELETE", function() {
        notConfirmed = false;
        deleteBtn.click();
        
        });
    body.append(ac.ac);
    } 
 
})