const deleteBtn = document.querySelector('#delete-btn');
const body = document.querySelector('body');
let notConfirmed = true;
deleteBtn.addEventListener('click', (e) => {
    if (notConfirmed) {
        e.preventDefault();
        const ac = new AlertController("DELETE ACCOUNT", "Are you sure you want to delete your account?", "DELETE ACCOUNT", function() {
            notConfirmed = false;
            deleteBtn.click();
        });
        body.append(ac.ac);
    }
});