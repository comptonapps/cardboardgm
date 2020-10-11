class CellCollectionListener {
    constructor(cell, endpoint, linkStub, userId) {
        this.cell = cell;
        this.apiEndpoint = endpoint;
        this.linkStub = linkStub;
        this.userId = userId;
        this.appContainer = document.querySelector('.app-container');
        this.cellContainer = document.querySelector('.cells-container');
        this.searchField = document.querySelector('.search-field');
        this.searchBtn = document.querySelector('.search-btn');
        this.offset = 0;
        this.limit = document.getElementsByClassName('collection-cell').length;
        this.searchStr;
        this.listening = true;
        this.init();
    }

    async init() {
        console.log('HERE')
        console.log(this.limit);
        if (this.limit === 0) {
            this.listening = false;
        }
        window.addEventListener('load', await this.fillContainer);
        this.searchField.addEventListener('input', await this.refreshUsers);
        this.appContainer.addEventListener('scroll', await this.sizeChange)
        this.searchBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await this.searchUsers();
        });
        
        window.addEventListener('resize', await this.sizeChange)
    }

    getMoreJson = async () => {
        if (this.listening) {
            this.offset += this.limit;
            const params = { offset : this.offset, limit : this.limit, searchStr : this.searchStr }
            if (this.userId) {
                params.userId = this.userId;
            }
            let ach = this.appContainerHeight();
            let res = await axios.get(this.apiEndpoint, {params : params});
            this.loadCells(res.data.results);
            if (res.data.results.length < this.limit) {
                this.listening = false;
            }
            this.checkFilled(ach);
        }
        return;
    }

    searchUsers = async () => {
        this.offset = this.limit * -1;
        this.searchStr = this.searchField.value;
        this.cellContainer.innerHTML = "";
        this.listening = true;
        await this.getMoreJson();
    }

    checkFilled = async (height) => {
        if (height === this.appContainerHeight() && this.listening) {
            await this.getMoreJson();
        }
    }

    loadCells = (results) => {
        results.forEach((result) => {
            const cellLink = document.createElement('a');
            cellLink.setAttribute('href', `${this.linkStub}${result.id}`);
            let cell = new this.cell(result).cell;
            cellLink.append(cell);
            this.cellContainer.append(cellLink);
        })
    }

    fillContainer = async () => {
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
        if (this.searchField.value === "") {
            this.offset = this.limit * -1;
            this.searchStr = null;
            this.cellContainer.innerHTML = "";
            this.listening = true;
            await this.getMoreJson();
        };
    }

    sizeChange = async () => {
        if (this.appContainer.offsetHeight + this.appContainer.scrollTop == this.appContainer.scrollHeight) {
            this.appContainer.removeEventListener('scroll', await this.sizeChange);
            window.removeEventListener('resize', await this.sizeChange);
            await this.getMoreJson();
            this.appContainer.addEventListener('scroll', await this.sizeChange);
            window.addEventListener('resize', await this.sizeChange);

        };
    }
}