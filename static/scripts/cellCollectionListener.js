class CellCollectionListener {
    constructor(cell, endpoint, linkStub, userId) {
        this.cell = cell;
        this.apiEndpoint = endpoint;
        this.linkStub = linkStub;
        this.userId = userId;
        this.body = document.querySelector('body');
        this.appContainer = document.querySelector('.app-container');
        this.cellContainer = document.querySelector('.cells-container');
        this.searchField = document.querySelector('.search-field');
        this.searchBtn = document.querySelector('.search-btn');
        this.resultSpan = document.querySelector('.search-results')
        this.initialResultSpanValue = this.resultSpan.innerText;
        this.offset = 0;
        this.limit = document.getElementsByClassName('collection-cell').length;
        this.searchStr;
        this.listening = true;
        this.init();
    }

    async init() {
        // Checks the number of cells in the template to see if any initial cells have been sent from the server
        if (this.limit === 0) {
            this.listening = false;
        }
        // On load, make API calls until the screen is filled with cells or there are no more items
        window.addEventListener('load', await this.fillContainer);
        // If the searchField as a value of "", make a call to the server to get unfiltered data
        this.searchField.addEventListener('input', await this.refreshUsers);
        // Listen for scrolling to check if the bottom of the container is reached
        this.appContainer.addEventListener('scroll', await this.sizeChange)
        // Get data from server, filtered by the searchField value.
        this.searchBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await this.searchUsers();
            this.updateHeader(this.searchField.value)
        });
        // If the window is resized, check to see if more cells can fit in the visible space
        window.addEventListener('resize', await this.sizeChange)
    }

    getMoreJson = async () => {
        // listening will be set to false if the server returns less than the limit requested (end of data reached)
        if (this.listening) {
            // update the offset value to avoid getting repeat data from the server
            this.offset += this.limit;
            // params for api call
            const params = { offset : this.offset, limit : this.limit, searchStr : this.searchStr }
            if (this.userId) {
                // if there is a userID, filter results server-side
                params.userId = this.userId;
            }
            // Check current height of appContainer to see if cells have loaded into the non-visible space
            let ach = this.appContainerHeight();
            this.showLoader();
            let res = await axios.get(this.apiEndpoint, {params : params});
            this.removeLoader();
            this.loadCells(res.data.results);
            if (res.data.results.length < this.limit) {
                this.listening = false;
                this.addMessage("- END OF LIST -")
            }
            if (res.data.results.length === 0 && this.cellContainer.innerHTML === "") {
                this.addMessage("No Results Found");
            }
            this.checkFilled(ach);
        }
        return;
    }

    showLoader() {
        this.cellContainer.innerHTML += `<div class="loading">
                                           <div class="circle blue"></div>
                                           <div class="circle blue"></div>
                                           <div class="circle blue"></div>
                                        </div>`
    }

    removeLoader() {
        document.querySelector(".loading").remove();
    }

    updateHeader(val) {
        // Update header for filter value of displayed cells
        if(this.resultSpan) {
            if (val && val !== "") {
                this.resultSpan.innerText = `results for ${val}`;
            } else {
                this.resultSpan.innerText = this.initialResultSpanValue;
            }
        }
        
    }

    addMessage(msg) {
        // If the api call returns no results, display p to inform the user
        this.cellContainer.innerHTML += (`<p class='no-items'>${msg}</p>`);
    }

    searchUsers = async () => {
        // If the json requested is user related, strip all punctuation other than '-'
        this.offset = this.limit * -1;
        this.searchStr = this.searchField.value.replace(/[.,\/#!$%\^&\*;:{}=\_`~()]/g,"");
        this.cellContainer.innerHTML = "";
        this.listening = true;
        await this.getMoreJson();
    }

    checkFilled = async (height) => {
        // After an API call, if the pre-data appContainer height is equal to the current
        // height, load more data
        if (height === this.appContainerHeight() && this.listening) {
            await this.getMoreJson();
        }
    }

    loadCells = (results) => {
        results.forEach((result) => {
            // Construct a tag to hold cell
            const cellLink = document.createElement('a');
            cellLink.setAttribute('href', `${this.linkStub}${result.id}`);
            // Create new cell from result
            let cell = new this.cell(result).cell;
            // Add cell to the cellLink
            cellLink.append(cell);
            // Add the cell to the container
            this.cellContainer.append(cellLink);
        })
    }

    fillContainer = async () => {
        // If the client height is greater than the appContainer height,
        // more cells can be loaded to expand the appContainer.
        while (this.getClientHeight() >= this.appContainerHeight() && this.listening) {
            await this.getMoreJson();
        }
    }

    getClientHeight() {
        return document.documentElement.clientHeight;
    }

    appContainerHeight() {
        return this.appContainer.scrollHeight;
    }

    refreshUsers = async () =>  {
        // if the searchField value has been deleted, load unfiltered data
        if (this.searchField.value === "") {
            this.offset = this.limit * -1;
            this.searchStr = null;
            this.cellContainer.innerHTML = "";
            this.listening = true;
            await this.getMoreJson();
            this.updateHeader(this.searchField.value)
        };
    }

    sizeChange = async () => {
        // The user has changed the size of the window.  Check to see if more cells can be loaded
        if (this.appContainer.offsetHeight + this.appContainer.scrollTop == this.appContainer.scrollHeight) {
            this.appContainer.removeEventListener('scroll', await this.sizeChange);
            window.removeEventListener('resize', await this.sizeChange);
            await this.getMoreJson();
            this.appContainer.addEventListener('scroll', await this.sizeChange);
            window.addEventListener('resize', await this.sizeChange);

        };
    }
}