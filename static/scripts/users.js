window.addEventListener('DOMContentLoaded', ()=>{
    const searchBtn = document.querySelector(".search-btn");
    searchBtn.addEventListener('click', async function(e) {
    e.preventDefault();
    let input = document.querySelector(".search-field").value
    let resp = await axios.get('/api/users', {params : { 'name' : input}})
    document.querySelector('.cells-container').innerHTML = "";
    for (user of resp.data) {
        const cellLink = document.createElement('a');
        cellLink.setAttribute('href', `/users/${user.id}`)
        let newCell = new Cell(user, false);
        cellLink.append(newCell.cell)
        document.querySelector('.cells-container').append(cellLink);
        }
    });
});