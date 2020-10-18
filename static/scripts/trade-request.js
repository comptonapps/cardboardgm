let selectedIds = [];
let dataLoaded = false;
document.addEventListener('DOMContentLoaded', function() {
    clearCachedChecks();
})

const yourCollection = document.querySelector(".your-collection");
const selectedCards = document.querySelector(".selected-cards");
const sendBtn = document.querySelector("#send-request-btn");
const searchField = document.querySelector("#search");

function clearCachedChecks() {
    let checks = document.getElementsByClassName('check');
    for (check of checks) {
        check.checked = false;
    }
}

searchField.addEventListener('input', function() {
    yourCollection.innerHTML = "";
    let results = [...cards];
    const tokens = searchField.value.toLowerCase().split(" ");
    for (token of tokens) {
        results = results.filter(el => el.title.toLowerCase().includes(token));
    }
    if (results.length === 0) {
        const noResults = document.createElement('p').innerText = "No Results Found";
        yourCollection.append(noResults);
    } else {
        results.forEach(result => {
            const newCell = getNewInCollectionCell(result);
            if (selectedIds.includes(result.id.toString())) {
                newCell.firstElementChild.checked = true;
            }
            yourCollection.append(newCell);
        });
    }
})
yourCollection.addEventListener('click', (e) => {
    const target = e.target
    if (target.classList.contains('check')) {
        if (target.checked) {
            const card = getCardFromJson(parseInt(target.dataset.id));
            selectedCards.append(getNewRequestCell(card));
            selectedIds.push(target.dataset.id)
        } else {
            selectedCards.querySelector(`[data-id="${target.dataset.id}"]`).remove()
        }
    }
    if (e.target.tagName == 'I') {
        showImage(e.target.dataset.imgurl)
    }
});

selectedCards.addEventListener('click', function(e) {
    const target = e.target;
    if (target.tagName == 'INPUT') {
        let id = target.parentElement.dataset.id;
        let index = selectedIds.indexOf(id.toString());
        if (index != -1){
            selectedIds.splice(index, 1)
        }
        target.parentElement.remove();
        yourCollection.querySelector(`[data-id="${id}"]`).checked = false;

    }
    if (target.tagName == "I") {
        showImage(target.dataset.imgurl);
    }
    
});

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
    if (!dataLoaded) {
        e.preventDefault();
    }
    
    dataLoaded = true;
    let cells = document.getElementsByClassName('selected');
    selectedCardsIds = [];
    for (cell of cells) {
        selectedCardsIds.push(parseInt(cell.dataset.id));
    }
    reqData = document.querySelector('#req_data');
    reqData.value = JSON.stringify({c : selectedIds});
    if (dataLoaded) {
        sendBtn.click();
    }
})