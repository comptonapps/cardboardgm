const deleteBtn = document.querySelector('#delete-btn');
const body = document.querySelector('body');
let notConfirmed = true;
deleteBtn.addEventListener('click', (e) => {
    // The user will have to confirm delete request
    if (notConfirmed) {
        e.preventDefault();
        // Present Alert Controller modally
        const ac = new AlertController("DELETE ACCOUNT", "Are you sure you want to delete your account?", "DELETE ACCOUNT", function() {
            notConfirmed = false;
            deleteBtn.click();
        });
        body.append(ac.ac);
    }
});