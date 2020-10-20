document.addEventListener('DOMContentLoaded', function() {
    //Clear all checked boxes upon refresh/reload
    clearYourCollectionChecks();
})

const yourCollection = document.querySelector(".your-collection");
const selectedCards = document.querySelector(".selected-cards");
const sendBtn = document.querySelector("#send-request-btn");
const searchField = document.querySelector("#search");
let selectedIds = [];
let reqData = document.querySelector('#req_data');
let reqDataLoaded = false;

function clearYourCollectionChecks() {
    let checks = document.getElementsByClassName('check');
    for (check of checks) {
        check.checked = false;
    }
}

searchField.addEventListener('input', function(){
    handleSearchInput(searchField.value)
})

function handleSearchInput(val) {
    /* This function will update the cells in the your-collection div with filtered results from a clone of the json in cards */
    // Clear the cells in your-collection
    yourCollection.innerHTML = "";
    // Spread the data from cards into results
    let results = [...cards];
    // Split value of search-field into lowercased tokens
    const tokens = val.toLowerCase().split(" ");
    results = getFilteredResults(results, tokens)
    // Get array of items (cells or no-results p) to append to your-collection
    const itemsToAppend = getCollectionItems(results)
    itemsToAppend.forEach((item) => yourCollection.append(item));
    
}

function getFilteredResults(results, tokens) {
    // Loop through tokens and update results with matching values
    let filteredResults;
    for (token of tokens) {
        filteredResults = results.filter(el => el.title.toLowerCase().includes(token));
    }
    return filteredResults
}

function getCollectionItems(results) {
    let items = [];
    // If results is empty, push p with "No Results Found"
    if (results.length === 0) {
        const noResults = document.createElement('p');
        noResults.classList.add('no-items')
        noResults.innerText = "No Results Found"
        items.push(noResults);
    } else {
        // Create new cell for each item in result
        results.forEach(result => {
            const newCell = getNewInCollectionCell(result);
            // If the card has already been selected, check the checkbox
            if (selectedIds.includes(result.id.toString())) {
                newCell.firstElementChild.checked = true;
            }
            items.push(newCell);
        });
    }
    return items
}

/* Listen for click events and handle checkbox checks/unchecks  */
yourCollection.addEventListener('click', (e) => {
    handleYourCollectionClick(e)
});

function handleYourCollectionClick(e) {
    const target = e.target
    if (target.classList.contains('check')) {
        if (target.checked) {
            // If the checkbox has just been checked, get the id from the dataset and get card data from cards 
            const card = getCardFromJson(parseInt(target.dataset.id));
            selectedCards.append(getNewRequestCell(card));
            // Add card id to selectedIds
            selectedIds.push(target.dataset.id)
        } else {
            // Remove the cell from selectedCards if the box is unchecked
            selectedCards.querySelector(`[data-id="${target.dataset.id}"]`).remove()
        }
    }
    // Display the card image if the image icon is clicked
    if (target.tagName == 'I') {
        showImage(target.dataset.imgurl)
    }
}



selectedCards.addEventListener('click', function(e) {
    handleSelectedCardsClick(e)  
});

function handleSelectedCardsClick(e){
    const target = e.target;
    // Check for checkbox click
    if (target.tagName == 'INPUT') {
        // Get the card id from the dataset
        let id = target.parentElement.dataset.id;
        // Get index of the card id in selectedIds array
        let index = selectedIds.indexOf(id.toString());
        // remove the value from the array
        if (index != -1){
            selectedIds.splice(index, 1)
        }
        target.parentElement.remove();
        yourCollection.querySelector(`[data-id="${id}"]`).checked = false;

    }
    if (target.tagName == "I") {
        showImage(target.dataset.imgurl);
    }
}

function showImage(url) {
    const body = document.querySelector('body');
    const modalWindow = new ModalWindow().modalWindow
    const img = document.createElement('img');
    img.setAttribute('src', url);
    modalWindow.append(img);
    body.append(modalWindow);
}

function getCardFromJson(cid) {
    const { title, id, full_url } = cards.find(el => el.id === cid)
    return { title, id, full_url };
}

function getNewInCollectionCell(data) {
    const cell = document.createElement('div');
    cell.classList.add('request-cell')
    cell.innerHTML = `<input type="checkbox" data-id=${data.id} class="check">
                        <p>${data.title}</p>
                        <span><i class="far fa-images tr-span" data-imgurl="${data.full_url}"></i></span>`
    return cell;
}



function getNewRequestCell(data) {
    const cell = document.createElement('div');
    cell.classList.add('request-cell');
    cell.classList.add('selected')
    cell.dataset.id = data.id;
    cell.innerHTML = `<input type="checkbox" data-id="${data.id} "checked class="sel-check">
        <p>${data.title}</p>
        <span><i class="far fa-images tr-span" data-imgurl="${data.full_url}"></i></span>`;
    return cell;
}

sendBtn.addEventListener('click', function(e){
    if (!reqDataLoaded){
        e.preventDefault();
    }
    // JSON stringify the data so it can be decoded on the server side
    reqData.value = JSON.stringify({c_ids : selectedIds});
    reqDataLoaded = true;
    if (reqDataLoaded) {
        sendBtn.click();
    }
})

